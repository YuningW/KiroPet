// Webview side: walks the buddy along the panel, plays activities and
// gestures, shows the Thai word card and the timer / work-time footer.
// Word choice and timers live in extension.js; this file only renders.
// Two art styles: "pixel" swaps PNG frames, "cartoon" inlines an SVG and
// animates its #eyes-* / #foot-* parts. Activity props are overlay images.
(function () {
  const vscode = acquireVsCodeApi();
  const $ = id => document.getElementById(id);
  const stage = $('stage'), pet = $('pet'), actor = $('actor');
  const pix = $('pix'), vec = $('vec'), prop = $('prop');
  const bubble = $('bubble'), zzz = $('zzz'), tip = $('tip');

  const FPS = 30;
  const SLEEP_AFTER = 45 * FPS;    // nap after the editor loses focus this long
  const BUBBLE_HOLD = 15 * FPS;
  const GESTURES = ['wiggle', 'dance', 'spin', 'stretch', 'nod'];
  const ALARM_MAX = 60 * FPS;      // stop ringing on its own after a minute

  const st = {
    mascot: '', style: 'cartoon', quiz: false, levelName: '', actions: [],
    x: 20, dir: 1, walk: 0, pause: 0, sprint: 0, hop: 0,
    blink: 0, nextBlink: 60, focused: true, unfocused: 0, sleeping: false,
    bubbleHold: 0, revealed: true,
    action: null, actT: 0, alarm: 0, hovering: false,
    clock: {},
  };

  const cache = {};
  function frame(blink, foot) {
    const src = `${window.SPRITES}/${st.mascot}_${blink}${foot}.png?v=${window.STAMP}`;
    if (!cache[src]) { const i = new Image(); i.src = src; cache[src] = i; }
    return src;
  }

  function setArt(mascot, style, svg) {
    st.mascot = mascot;
    st.style = style;
    pet.className = style;
    if (style === 'cartoon') {
      vec.innerHTML = svg || '';
    } else {
      vec.innerHTML = '';
      for (const b of [0, 1]) for (const f of [0, 1]) frame(b, f);
    }
    showProp();
  }

  // ---- activities & gestures
  function showProp() {
    if (!st.action) { prop.hidden = true; return; }
    prop.src = `${window.PROPS}/${st.action}.${st.style === 'cartoon' ? 'svg' : 'png'}?v=${window.STAMP}`;
    prop.hidden = false;
  }

  function startAction(id, seconds) {
    st.action = id;
    st.actT = seconds * FPS;
    st.pause = 0;
    // turn away from a nearby wall so side props aren't cut off
    const room = stage.clientWidth - pet.offsetWidth;
    if (st.dir > 0 && st.x > room - 40) st.dir = -1;
    if (st.dir < 0 && st.x < 40) st.dir = 1;
    showProp();
  }

  function stopAction() {
    st.action = null;
    st.actT = 0;
    showProp();
  }

  function gesture(name) {
    name = name || GESTURES[Math.floor(Math.random() * GESTURES.length)];
    actor.className = '';
    void actor.offsetWidth;                      // restart the CSS animation
    actor.className = `g-${name}`;
  }
  actor.addEventListener('animationend', () => { if (!st.alarm) actor.className = ''; });

  function heartPop() {
    const h = document.createElement('div');
    h.className = 'heart';
    h.textContent = '♥';
    h.style.left = `${Math.round(st.x + pet.offsetWidth / 2 - 5)}px`;
    stage.appendChild(h);
    setTimeout(() => h.remove(), 1100);
  }

  function label() {
    if (st.alarm) return "⏰ time's up!";
    if (st.sleeping) return 'having a nap · click to wake me';
    if (st.action) return (st.actions.find(a => a.id === st.action) || {}).label || '';
    return 'strolling around · click for a Thai word';
  }

  // ---- word card
  function showWord(w) {
    if (!w) return;
    $('thai').textContent = w.thai;
    $('rom').textContent = w.rom;
    $('eng').textContent = w.eng;
    $('level').textContent = st.levelName.split(' — ')[0];
    st.revealed = !st.quiz;
    bubble.classList.toggle('quiz', !st.revealed);
    bubble.hidden = false;
    st.bubbleHold = st.quiz ? Infinity : BUBBLE_HOLD;
    st.hop = 14;
  }

  // ---- footer: countdown + worked time
  function fmt(ms) {
    const s = Math.max(0, Math.round(ms / 1000));
    const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
    const mm = String(m).padStart(2, '0'), ss = String(sec).padStart(2, '0');
    return h ? `${h}:${mm}:${ss}` : `${m}:${ss}`;
  }
  function short(ms) {
    const m = Math.max(0, Math.floor(ms / 60000));
    return m >= 60 ? `${Math.floor(m / 60)}h${String(m % 60).padStart(2, '0')}` : `${m}m`;
  }
  let lastFooter = 0;
  function renderFooter() {
    const now = Date.now();
    if (now - lastFooter < 500) return;
    lastFooter = now;
    const c = st.clock, t = $('timer'), w = $('work');
    if (st.alarm) {
      t.textContent = `⏰ ${st.alarmLabel || 'Timer'} — time's up!`;
      t.className = 'due';
    } else if (c.timer) {
      const icon = c.timer.kind === 'alarm' ? '🔔' : '⏱';
      t.textContent = `${icon} ${fmt(c.timer.end - now)} ${c.timer.label}`;
      t.className = '';
    } else {
      t.textContent = '';
    }
    if (!c.workStart) { w.textContent = ''; return; }
    const worked = `💼 ${short(now - c.workStart)}`;
    if (!c.breakAt) {
      w.textContent = worked;
      w.className = '';
    } else if (now >= c.breakAt) {
      w.textContent = `${worked} · break time!`;
      w.className = 'due';
    } else {
      w.textContent = `${worked} · break in ${short(c.breakAt - now + 59999)}`;
      w.className = '';
    }
  }

  // ---- messages from the extension
  window.addEventListener('message', e => {
    const m = e.data;
    if (m.type === 'state') {
      st.actions = m.actions || [];
      if (st.action && !st.actions.some(a => a.id === st.action) && !st.alarm) stopAction();
      if (m.mascot !== st.mascot || m.style !== st.style) setArt(m.mascot, m.style, m.svg);
      st.quiz = m.quiz;
      st.levelName = m.levelName;
      setFocus(m.focused);
      if (m.word) { showWord(m.word); }
    } else if (m.type === 'word') {
      showWord(m.word);
    } else if (m.type === 'focus') {
      setFocus(m.focused);
    } else if (m.type === 'clock') {
      st.clock = m;
      lastFooter = 0;
    } else if (m.type === 'gesture') {
      gesture(m.name);
    } else if (m.type === 'activity') {
      if (!st.alarm) {
        if (st.sleeping) setFocus(true);
        startAction(m.id, 12);
        gesture('nod');
      }
    } else if (m.type === 'alarm') {
      if (m.on) {
        st.alarm = ALARM_MAX;
        st.alarmLabel = m.label;
        if (st.sleeping) setFocus(true);
        startAction('alarm', 3600);
        actor.className = 'g-shake';
      } else if (st.alarm) {
        st.alarm = 0;
        actor.className = '';
        stopAction();
        gesture('dance');
      }
      lastFooter = 0;
    }
  });

  function setFocus(f) {
    if (f && st.sleeping) {
      st.sleeping = false;
      st.hop = 14;
      zzz.hidden = true;
      if (st.action === 'sleep') stopAction();
    }
    st.focused = f;
    st.unfocused = 0;
  }

  pet.addEventListener('click', () => {
    st.hop = 14;
    heartPop();
    if (st.sleeping) { setFocus(true); return; }
    if (st.alarm) { vscode.postMessage({ type: 'poke' }); return; }
    if (st.action && Math.random() < 0.5) stopAction();
    else if (!st.action && st.actions.length && Math.random() < 0.4) {
      startAction(st.actions[Math.floor(Math.random() * st.actions.length)].id, 8 + Math.random() * 7);
    }
    gesture();
    vscode.postMessage({ type: 'poke' });
  });
  pet.addEventListener('mouseenter', () => { st.hovering = true; });
  pet.addEventListener('mouseleave', () => { st.hovering = false; tip.hidden = true; });
  bubble.addEventListener('click', () => {
    if (!st.revealed) {                          // quiz: reveal the meaning
      st.revealed = true;
      bubble.classList.remove('quiz');
      st.bubbleHold = 8 * FPS;
    } else {
      bubble.hidden = true;
    }
  });

  function tick() {
    const width = stage.clientWidth;
    const petW = pet.offsetWidth;
    // blink
    if (st.blink > 0) st.blink--;
    else if (--st.nextBlink <= 0) { st.blink = 6; st.nextBlink = 45 + Math.random() * 105; }
    if (st.hop > 0) st.hop--;

    // alarm rings for a while, then the buddy gives up
    if (st.alarm > 0 && --st.alarm === 0) {
      actor.className = '';
      stopAction();
      lastFooter = 0;
    }

    // nap when the editor isn't focused
    if (!st.focused && !st.sleeping && !st.alarm && ++st.unfocused > SLEEP_AFTER) {
      st.sleeping = true;
      zzz.hidden = false;
      stopAction();
    }

    const due = st.clock.breakAt && Date.now() >= st.clock.breakAt;
    if (st.sleeping || st.alarm) {
      // stay put
    } else if (st.action) {
      if (--st.actT <= 0) stopAction();
      else if (Math.random() < 0.003) gesture();
    } else if (st.pause > 0) {
      st.pause--;
      if (Math.random() < 0.004) gesture();
    } else {
      if (st.sprint > 0) st.sprint--;
      else if (Math.random() < 0.0015) st.sprint = 45 + Math.random() * 45;
      const speed = st.sprint > 0 ? 2.2 : 0.8;
      st.x += st.dir * speed;
      st.walk += st.sprint > 0 ? 0.25 : 0.12;
      const max = Math.max(0, width - petW);
      if (st.x <= 0) { st.x = 0; st.dir = 1; }
      if (st.x >= max) { st.x = max; st.dir = -1; }
      if (!st.sprint && Math.random() < 0.004) st.pause = 20 + Math.random() * 70;
      if (!st.sprint && Math.random() < 0.002) st.dir *= -1;
      // now and then stop for an activity (coffee when a break is due)
      if (!st.sprint && st.actions.length && Math.random() < (due ? 0.01 : 0.004)) {
        const pick = due && st.actions.some(a => a.id === 'coffee') ? 'coffee'
          : st.actions[Math.floor(Math.random() * st.actions.length)].id;
        startAction(pick, 8 + Math.random() * 8);
      }
    }

    const moving = !st.action && st.pause === 0 && !st.sleeping && !st.alarm;
    const foot = moving ? Math.floor(st.walk) % 2 : 0;
    const closed = st.blink > 0 || st.sleeping || st.action === 'sleep' ? 1 : 0;
    let bob = 0;
    if (st.style === 'cartoon') {
      vec.classList.toggle('blink', !!closed);
      vec.classList.toggle('step-l', moving && foot === 0);
      vec.classList.toggle('step-r', moving && foot === 1);
      bob = moving ? foot : 0;                   // gentle bounce per step
    } else {
      const src = frame(closed, foot);
      if (pix.getAttribute('src') !== src) pix.setAttribute('src', src);
    }

    const hopY = st.hop > 0 ? Math.round(12 * (1 - ((st.hop - 7) / 7) ** 2)) : 0;
    pet.style.transform =
      `translate(${Math.round(st.x)}px, ${-hopY - bob}px) scaleX(${st.dir < 0 ? -1 : 1})`;
    zzz.style.left = `${Math.round(st.x + petW - 10)}px`;

    if (st.hovering) {
      tip.textContent = label();
      tip.hidden = false;
      const tw = tip.offsetWidth;
      tip.style.left = `${Math.round(Math.min(Math.max(2, st.x + petW / 2 - tw / 2), width - tw - 2))}px`;
    }

    if (!bubble.hidden) {
      if (st.bubbleHold !== Infinity && --st.bubbleHold <= 0) bubble.hidden = true;
    }
    renderFooter();
  }

  setInterval(tick, 1000 / FPS);
  vscode.postMessage({ type: 'ready' });
})();
