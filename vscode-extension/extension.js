// KiroPet for VS Code / Kiro: a buddy in the Explorer that teaches Thai,
// runs countdown timers / alarms, and nudges you to take breaks.
// Sprites and words are exported from the Python app by tools/export_web.py.
const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const DATA = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'media', 'data.json'), 'utf8'));
const LEVEL_NAMES = Object.fromEntries(DATA.levels.map(l => [l.id, l.name]));
const MASCOT_IDS = DATA.mascots.map(m => m.id);
const SVGS = Object.fromEntries(MASCOT_IDS.map(id => [id,
  fs.readFileSync(path.join(__dirname, 'media', 'cartoon', `${id}.svg`), 'utf8')]));
const MIN = 60 * 1000;

function cfg() {
  return vscode.workspace.getConfiguration('kiropet');
}

// Falls back to MuvMuv if the setting names a buddy that was removed.
function mascot() {
  const m = cfg().get('mascot');
  return MASCOT_IDS.includes(m) ? m : MASCOT_IDS[0];
}

function style() {
  return cfg().get('style') === 'pixel' ? 'pixel' : 'cartoon';
}

function wordsFor(level) {
  const levels = level === 'all' ? DATA.levels : DATA.levels.filter(l => l.id === level);
  return levels.flatMap(l => l.words.map(([thai, rom, eng]) => ({ thai, rom, eng, level: l.id })));
}

function fmt(ms) {
  const s = Math.max(0, Math.round(ms / 1000));
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
  const mm = String(m).padStart(2, '0'), ss = String(sec).padStart(2, '0');
  return h ? `${h}:${mm}:${ss}` : `${m}:${ss}`;
}

// "15:30", "3:30pm", "3pm", "9.05 am" -> next Date at that time (today or tomorrow).
function parseClock(text) {
  const m = /^\s*(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm)?\s*$/i.exec(text || '');
  if (!m) return undefined;
  let h = Number(m[1]);
  const min = Number(m[2] || 0);
  const ap = (m[3] || '').toLowerCase();
  if (min > 59 || h > 23 || (ap && (h < 1 || h > 12))) return undefined;
  if (ap === 'pm' && h < 12) h += 12;
  if (ap === 'am' && h === 12) h = 0;
  const d = new Date();
  d.setHours(h, min, 0, 0);
  if (d.getTime() <= Date.now()) d.setDate(d.getDate() + 1);
  return d;
}

// Shuffle bag: every word once, in random order, before any repeats.
class Shuffler {
  constructor(words) { this.words = words; this.bag = []; }
  next() {
    if (!this.bag.length) {
      this.bag = this.words.slice();
      for (let i = this.bag.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [this.bag[i], this.bag[j]] = [this.bag[j], this.bag[i]];
      }
    }
    return this.bag.pop();
  }
}

class PetView {
  constructor(context) {
    this.context = context;
    this.view = undefined;
    this.word = undefined;
    this.level = cfg().get('thaiLevel');
    this.deck = new Shuffler(wordsFor(this.level));
    this.focusedMinutes = 0;

    // work / break tracking (like the desktop buddy, with "away from the
    // editor for a while" standing in for a screen lock)
    this.workStart = Date.now();
    this.snoozeMs = 0;
    this.breakNotified = false;
    this.blurredAt = vscode.window.state.focused ? undefined : Date.now();

    // countdown timer / alarm, persisted so a reload doesn't lose it
    this.timer = context.globalState.get('kiropet.timer');

    this.status = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    this.status.command = 'kiropet.nextWord';
    this.timerStatus = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 101);
    this.timerStatus.command = 'kiropet.timer';
    context.subscriptions.push(this.status, this.timerStatus);

    // Count only minutes the editor is focused, like the desktop app only
    // talking while you're coding.
    const words = setInterval(() => {
      if (!vscode.window.state.focused) return;
      this.focusedMinutes += 1;
      if (this.focusedMinutes >= cfg().get('wordIntervalMinutes')) this.nextWord();
    }, MIN);
    const clock = setInterval(() => this.clockTick(), 1000);
    context.subscriptions.push({ dispose: () => { clearInterval(words); clearInterval(clock); } });

    context.subscriptions.push(
      vscode.window.onDidChangeWindowState(s => {
        if (!s.focused) {
          this.blurredAt = Date.now();
        } else if (this.blurredAt) {
          const away = Date.now() - this.blurredAt;
          this.blurredAt = undefined;
          if (away >= cfg().get('breakResetMinutes') * MIN) this.resetWork();
        }
        this.post({ type: 'focus', focused: s.focused });
      }),
      vscode.workspace.onDidChangeConfiguration(e => {
        if (!e.affectsConfiguration('kiropet')) return;
        if (cfg().get('thaiLevel') !== this.level) {
          this.level = cfg().get('thaiLevel');
          this.deck = new Shuffler(wordsFor(this.level));
          this.nextWord();
        }
        this.sendState();
        this.renderStatus();
      }));
    this.nextWord(false);
    this.clockTick();
  }

  resolveWebviewView(view) {
    this.view = view;
    view.onDidDispose(() => { if (this.view === view) this.view = undefined; });
    const media = vscode.Uri.joinPath(this.context.extensionUri, 'media');
    view.webview.options = { enableScripts: true, localResourceRoots: [media] };
    view.webview.html = this.html(view.webview, media);
    view.webview.onDidReceiveMessage(msg => {
      if (msg.type === 'ready') this.sendState(true);
      if (msg.type === 'poke') this.nextWord();
    });
    view.onDidChangeVisibility(() => view.visible && this.sendState(true));
  }

  post(msg) {
    if (this.view) this.view.webview.postMessage(msg);
  }

  sendState(withWord = false) {
    this.post({
      type: 'state',
      mascot: mascot(),
      style: style(),
      svg: style() === 'cartoon' ? SVGS[mascot()] : undefined,
      actions: cfg().get('activities') ? DATA.actions : [],
      quiz: cfg().get('quizMode'),
      levelName: LEVEL_NAMES[this.level] || 'All levels',
      focused: vscode.window.state.focused,
      word: withWord ? this.word : undefined,
    });
    this.sendClock();
  }

  // The webview renders the countdowns itself from these timestamps.
  sendClock() {
    const every = cfg().get('breakReminderMinutes');
    this.post({
      type: 'clock',
      workStart: this.workStart,
      breakAt: every > 0 ? this.workStart + every * MIN + this.snoozeMs : undefined,
      timer: this.timer,
    });
  }

  // ---- Thai words
  nextWord(announce = true) {
    this.focusedMinutes = 0;
    this.word = this.deck.next();
    this.renderStatus();
    if (announce) this.post({ type: 'word', word: this.word });
  }

  renderStatus() {
    if (!cfg().get('showInStatusBar') || !this.word) {
      this.status.hide();
      return;
    }
    const w = this.word;
    this.status.text = `$(comment) ${w.thai}  ${w.rom}`;
    this.status.tooltip = new vscode.MarkdownString(
      `### ${w.thai}\n\n*${w.rom}*\n\n**${w.eng}**\n\n` +
      `${LEVEL_NAMES[w.level]} · click for the next word`);
    this.status.show();
  }

  // ---- timers, alarms, breaks
  clockTick() {
    const now = Date.now();
    if (this.timer && now >= this.timer.end) this.ring();

    const every = cfg().get('breakReminderMinutes');
    const breakAt = this.workStart + every * MIN + this.snoozeMs;
    if (every > 0 && !this.breakNotified && vscode.window.state.focused && now >= breakAt) {
      this.breakNotified = true;
      this.post({ type: 'gesture', name: 'stretch' });
      const worked = Math.round((now - this.workStart) / MIN);
      vscode.window.showInformationMessage(
        `🐾 You've been working for ${worked} min — time for a little break!`,
        'Taking a break', 'Snooze 10 min').then(pick => {
        if (pick === 'Taking a break') this.resetWork();
        if (pick === 'Snooze 10 min') this.snoozeBreak(10);
      });
    }

    if (this.timer) {
      const icon = this.timer.kind === 'alarm' ? '$(bell)' : '$(watch)';
      this.timerStatus.text = `${icon} ${fmt(this.timer.end - now)} ${this.timer.label}`;
      this.timerStatus.tooltip = 'KiroPet timer · click to add time or cancel';
      this.timerStatus.show();
    } else {
      this.timerStatus.hide();
    }
  }

  resetWork() {
    this.workStart = Date.now();
    this.snoozeMs = 0;
    this.breakNotified = false;
    this.sendClock();
  }

  snoozeBreak(minutes) {
    this.snoozeMs = Date.now() - this.workStart - cfg().get('breakReminderMinutes') * MIN
      + minutes * MIN;
    this.breakNotified = false;
    this.sendClock();
  }

  setTimer(timer) {
    this.timer = timer;
    this.context.globalState.update('kiropet.timer', timer);
    this.sendClock();
    this.clockTick();
  }

  ring() {
    const t = this.timer;
    this.setTimer(undefined);
    this.post({ type: 'alarm', on: true, label: t.label });
    const what = t.kind === 'alarm' ? `Alarm: ${t.label}` : `${t.label} — time's up!`;
    vscode.window.showWarningMessage(`⏰ ${what}`, 'Snooze 5 min', 'Done').then(pick => {
      this.post({ type: 'alarm', on: false });
      if (pick === 'Snooze 5 min') this.setTimer({ ...t, end: Date.now() + 5 * MIN });
    });
  }

  async timerCommand() {
    if (this.timer) {
      const pick = await vscode.window.showQuickPick([
        { label: '$(add) Add 5 minutes', id: 'add' },
        { label: '$(debug-restart) Start a new timer instead', id: 'new' },
        { label: '$(close) Cancel timer', id: 'cancel' },
      ], { placeHolder: `${this.timer.label}: ${fmt(this.timer.end - Date.now())} left` });
      if (!pick) return;
      if (pick.id === 'add') return this.setTimer({ ...this.timer, end: this.timer.end + 5 * MIN });
      if (pick.id === 'cancel') return this.setTimer(undefined);
    }
    const presets = [5, 10, 15, 25, 45, 60].map(n => ({
      label: `$(watch) ${n} min${n === 25 ? '  (Pomodoro)' : ''}`, minutes: n,
    }));
    const pick = await vscode.window.showQuickPick([
      ...presets,
      { label: '$(edit) Custom minutes…', id: 'custom' },
      { label: '$(bell) Alarm at a time…', id: 'alarm' },
    ], { placeHolder: 'Start a countdown or set an alarm' });
    if (!pick) return;

    let end, kind = 'timer';
    if (pick.minutes) {
      end = Date.now() + pick.minutes * MIN;
    } else if (pick.id === 'custom') {
      const v = await vscode.window.showInputBox({
        prompt: 'Countdown length in minutes', placeHolder: 'e.g. 20',
        validateInput: s => (Number(s) > 0 && Number(s) <= 24 * 60 ? undefined : 'Enter 1–1440 minutes'),
      });
      if (!v) return;
      end = Date.now() + Number(v) * MIN;
    } else {
      const v = await vscode.window.showInputBox({
        prompt: 'Alarm time', placeHolder: 'e.g. 15:30 or 3:30pm',
        validateInput: s => (parseClock(s) ? undefined : 'Try 15:30, 3:30pm or 3pm'),
      });
      if (!v) return;
      end = parseClock(v).getTime();
      kind = 'alarm';
    }
    const label = await vscode.window.showInputBox({
      prompt: 'What is it for? (optional — press Enter to skip)',
      placeHolder: kind === 'alarm' ? 'e.g. Stand-up meeting' : 'e.g. Focus',
    });
    if (label === undefined) return;
    this.setTimer({ end, kind, label: label.trim() || (kind === 'alarm' ? 'Alarm' : 'Timer') });
    this.post({ type: 'gesture', name: 'nod' });
  }

  async breakCommand() {
    const every = cfg().get('breakReminderMinutes');
    const opts = [30, 45, 60, 90].map(n => ({
      label: `${n === every ? '$(check)' : '$(blank)'} Remind me every ${n} min`, minutes: n,
    }));
    const pick = await vscode.window.showQuickPick([
      { label: '$(coffee) I just took a break — reset the work timer', id: 'reset' },
      ...opts,
      { label: `${every === 0 ? '$(check)' : '$(blank)'} No break reminders`, minutes: 0 },
    ], { placeHolder: `Worked ${fmt(Date.now() - this.workStart)} so far` });
    if (!pick) return;
    if (pick.id === 'reset') return this.resetWork();
    await cfg().update('breakReminderMinutes', pick.minutes, vscode.ConfigurationTarget.Global);
    this.breakNotified = false;
    this.sendClock();
  }

  html(webview, media) {
    // Build stamp on every URL: webviews cache resources by URL, so without
    // it a reinstall can mix a new pet.js with an old pet.css.
    const stamp = `${this.context.extension.packageJSON.version}-${
      Math.round(fs.statSync(path.join(__dirname, 'media', 'pet.js')).mtimeMs)}`;
    const uri = p => webview.asWebviewUri(vscode.Uri.joinPath(media, p));
    const nonce = Math.random().toString(36).slice(2) + Date.now().toString(36);
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${webview.cspSource}; style-src ${webview.cspSource}; script-src 'nonce-${nonce}';">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="${uri('pet.css')}?v=${stamp}">
</head>
<body data-vscode-context='{"preventDefaultContextMenuItems": true}'>
<div id="stage">
  <div id="bubble" hidden>
    <div><span id="thai"></span><span id="rom"></span></div>
    <div><span id="eng"></span><span id="level"></span></div>
  </div>
  <div id="zzz" hidden>z z z</div>
  <div id="tip" hidden></div>
  <div id="pet"><div id="actor">
    <img id="pix" alt="pet" draggable="false"><div id="vec"></div>
    <img id="prop" alt="" draggable="false" hidden>
  </div></div>
  <div id="ground"></div>
  <div id="info"><span id="timer"></span><span id="work"></span></div>
</div>
<script nonce="${nonce}">window.SPRITES = "${uri('sprites')}"; window.PROPS = "${uri('props')}"; window.STAMP = "${stamp}";</script>
<script nonce="${nonce}" src="${uri('pet.js')}?v=${stamp}"></script>
</body>
</html>`;
  }
}

// The original window-edge walker (kiro_pet.py). The extension starts it only
// when you pick it, passes along your buddy / style / level, and stops it
// when the editor closes, so it never lingers in the background.
class ScreenPet {
  constructor() { this.proc = undefined; }

  get running() { return !!this.proc; }

  async findScript() {
    const configured = cfg().get('screenPet.script');
    if (configured && fs.existsSync(configured)) return configured;
    for (const f of vscode.workspace.workspaceFolders || []) {
      const p = path.join(f.uri.fsPath, 'kiro_pet.py');
      if (fs.existsSync(p)) return p;
    }
    const pick = await vscode.window.showOpenDialog({
      title: 'Where is kiro_pet.py? (the KiroPet folder)',
      canSelectMany: false, filters: { 'Python': ['py'] },
    });
    if (!pick) return undefined;
    const p = pick[0].fsPath;
    await cfg().update('screenPet.script', p, vscode.ConfigurationTarget.Global);
    return p;
  }

  async start(candidates) {
    if (this.proc) return;
    if (process.platform !== 'win32') {
      vscode.window.showWarningMessage(
        'The screen pet (walking around the window) uses Windows features, so it only runs on Windows for now. The panel pet works everywhere.');
      return false;
    }
    const script = await this.findScript();
    if (!script) return false;
    // the configured Python, else pythonw on PATH, else the "pyw" launcher
    candidates = candidates || (cfg().get('screenPet.python') ? [cfg().get('screenPet.python')]
      : ['pythonw', 'pyw']);
    const python = candidates[0];
    const target = /kiro/i.test(vscode.env.appName) ? 'kiro' : 'code';
    const args = [script, '--target', target, '--mascot', mascot(), '--style', style(),
      '--level', cfg().get('thaiLevel')];
    const startedAt = Date.now();
    let err = '';
    const proc = spawn(python, args, {
      cwd: path.dirname(script), windowsHide: true, stdio: ['ignore', 'ignore', 'pipe'],
    });
    this.proc = proc;
    proc.stderr.on('data', d => { err = (err + d).slice(-600); });
    proc.on('error', e => {
      this.proc = undefined;
      if (e.code === 'ENOENT' && candidates.length > 1) return this.start(candidates.slice(1));
      vscode.window.showErrorMessage(
        `Couldn't start the screen pet with "${python}": ${e.message}. Set kiropet.screenPet.python to your Python (e.g. C:\\...\\pythonw.exe).`);
    });
    proc.on('exit', code => {
      if (this.proc === proc) this.proc = undefined;
      if (Date.now() - startedAt > 5000) return;
      if (code === 0) {
        vscode.window.showInformationMessage(
          'A screen pet was already running (probably started at Windows login). Remove that startup shortcut so KiroPet controls it.');
      } else if (code !== null) {
        vscode.window.showErrorMessage(`The screen pet stopped right away (code ${code}). ${err.trim().split('\n').pop() || ''}`);
      }
    });
    return true;
  }

  stop() {
    if (this.proc) { this.proc.kill(); this.proc = undefined; }
  }
}

const MODES = {
  panel: { label: '$(layout-sidebar-left) Panel pet', detail: 'Walks inside the KiroPet panel in the Explorer' },
  screen: { label: '$(screen-full) Screen pet', detail: 'Walks around the edge of the editor window (Windows)' },
  both: { label: '$(heart) Both', detail: 'Panel pet and screen pet together' },
  none: { label: '$(circle-slash) Neither', detail: 'No pet for now (timers and Thai words keep working)' },
};

function activate(context) {
  const pet = new PetView(context);
  const screen = new ScreenPet();
  context.subscriptions.push({ dispose: () => screen.stop() });

  const paw = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 102);
  paw.text = '🐾';
  paw.tooltip = 'KiroPet: choose which pet runs';
  paw.command = 'kiropet.choosePet';
  paw.show();
  context.subscriptions.push(paw);

  async function applyMode(mode) {
    const panel = mode === 'panel' || mode === 'both';
    await vscode.commands.executeCommand('setContext', 'kiropet.panelOn', panel);
    if (mode === 'screen' || mode === 'both') await screen.start(); else screen.stop();
    if (panel) vscode.commands.executeCommand('kiropet.view.focus');
  }

  // Nothing starts behind your back: the startup setting decides, and
  // "ask" (the default) offers a choice each time the editor opens.
  const startup = cfg().get('startup');
  if (startup === 'ask') {
    vscode.commands.executeCommand('setContext', 'kiropet.panelOn', false);
    vscode.window.showInformationMessage('🐾 Which KiroPet today?',
      'Panel pet', 'Screen pet', 'Both', 'Not today').then(pick => {
      const mode = { 'Panel pet': 'panel', 'Screen pet': 'screen', 'Both': 'both' }[pick] || 'none';
      applyMode(mode);
    });
  } else {
    applyMode(startup);
  }
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider('kiropet.view', pet,
      { webviewOptions: { retainContextWhenHidden: true } }),
    vscode.commands.registerCommand('kiropet.nextWord', () => pet.nextWord()),
    vscode.commands.registerCommand('kiropet.choosePet', async () => {
      const items = Object.entries(MODES).map(([id, m]) => ({ ...m, id }));
      items.push({ label: '', kind: vscode.QuickPickItemKind.Separator },
        { label: '$(gear) What to do when the editor opens…', id: 'startup' });
      const pick = await vscode.window.showQuickPick(items, {
        placeHolder: `Which pet? (screen pet is ${screen.running ? 'running' : 'off'})`,
      });
      if (!pick) return;
      if (pick.id !== 'startup') return applyMode(pick.id);
      const opts = [
        { label: 'Ask me each time', id: 'ask' },
        ...Object.entries(MODES).map(([id, m]) => ({ label: `Always: ${m.label}`, id })),
      ];
      opts.forEach(o => { if (o.id === cfg().get('startup')) o.label = `$(check) ${o.label}`; });
      const s = await vscode.window.showQuickPick(opts, { placeHolder: 'When the editor opens…' });
      if (s) await cfg().update('startup', s.id, vscode.ConfigurationTarget.Global);
    }),
    vscode.commands.registerCommand('kiropet.startScreenPet', () => screen.start()),
    vscode.commands.registerCommand('kiropet.stopScreenPet', () => screen.stop()),
    vscode.commands.registerCommand('kiropet.timer', () => pet.timerCommand()),
    vscode.commands.registerCommand('kiropet.breakReminder', () => pet.breakCommand()),
    vscode.commands.registerCommand('kiropet.activity', async () => {
      const gestures = ['wiggle', 'dance', 'spin', 'stretch', 'nod'];
      const pick = await vscode.window.showQuickPick([
        { label: 'Activities', kind: vscode.QuickPickItemKind.Separator },
        ...DATA.actions.map(a => ({ label: a.label, action: a.id })),
        { label: 'Gestures', kind: vscode.QuickPickItemKind.Separator },
        ...gestures.map(g => ({ label: g, gesture: g })),
      ], { placeHolder: 'What should your buddy do?' });
      if (!pick) return;
      await vscode.commands.executeCommand('kiropet.view.focus');
      pet.post(pick.action ? { type: 'activity', id: pick.action } : { type: 'gesture', name: pick.gesture });
    }),
    vscode.commands.registerCommand('kiropet.show', async () => {
      await vscode.commands.executeCommand('setContext', 'kiropet.panelOn', true);
      vscode.commands.executeCommand('kiropet.view.focus');
    }),
    // keep a running screen pet in step with buddy / style / level changes
    vscode.workspace.onDidChangeConfiguration(e => {
      if (screen.running && ['mascot', 'style', 'thaiLevel'].some(k =>
        e.affectsConfiguration(`kiropet.${k}`))) {
        screen.stop();
        setTimeout(() => screen.start(), 500);
      }
    }),
    vscode.commands.registerCommand('kiropet.toggleStyle', () =>
      cfg().update('style', style() === 'cartoon' ? 'pixel' : 'cartoon',
        vscode.ConfigurationTarget.Global)),
    vscode.commands.registerCommand('kiropet.chooseLevel', async () => {
      const items = DATA.levels.map(l => ({
        label: l.name, description: `${l.words.length} words`, id: l.id,
      }));
      items.push({ label: 'All levels', description: 'mixed', id: 'all' });
      const current = cfg().get('thaiLevel');
      items.forEach(i => { if (i.id === current) i.label = `$(check) ${i.label}`; });
      const pick = await vscode.window.showQuickPick(items, { placeHolder: 'Which Thai level?' });
      if (pick) await cfg().update('thaiLevel', pick.id, vscode.ConfigurationTarget.Global);
    }),
    vscode.commands.registerCommand('kiropet.changeBuddy', async () => {
      const items = [];
      let group;
      for (const m of DATA.mascots) {
        if (m.group !== group) {
          group = m.group;
          items.push({ label: group, kind: vscode.QuickPickItemKind.Separator });
        }
        items.push({ label: m.label, id: m.id });
      }
      const pick = await vscode.window.showQuickPick(items, { placeHolder: 'Pick your buddy' });
      if (pick) await cfg().update('mascot', pick.id, vscode.ConfigurationTarget.Global);
    }));
}

function deactivate() {}

module.exports = { activate, deactivate };
