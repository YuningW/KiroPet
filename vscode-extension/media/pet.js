// Webview side: draws the background scene, walks the buddy along the panel,
// plays activities and gestures, runs the stage / party choreography for
// group scenes, and shows the Thai word card and the timer footer.
// Word choice, scenes and timers are decided in extension.js; this file only
// renders. Two art styles: "pixel" swaps PNG frames, "cartoon" inlines an SVG
// and animates its #eyes-* / #foot-* parts. Activity props are overlay images.
(function () {
  const vscode = acquireVsCodeApi();
  const $ = id => document.getElementById(id);
  const stage = $('stage'), scene = $('scene');
  const bubble = $('bubble'), zzz = $('zzz'), tip = $('tip');

  const FPS = 30;
  const SLEEP_AFTER = 45 * FPS;    // nap after the editor loses focus this long
  const GESTURES = ['wiggle', 'dance', 'spin', 'stretch', 'nod'];
  const ALARM_MAX = 60 * FPS;      // stop ringing on its own after a minute
  const SLOT_GAP = 50;             // spacing between buddies in group scenes
  const rand = (a, b) => a + Math.random() * (b - a);
  const pick = list => list[Math.floor(Math.random() * list.length)];
  const asset = (base, file) => `${base}/${file}?v=${window.STAMP}`;
  // Activity details come from data.json (via the extension): emoji badge,
  // "side" props (stand beside the buddy, drawn bigger; held ones stay 1:1),
  // a motion, closed eyes, the scene it belongs to and its Thai word.
  const ALARM_META = { id: 'alarm', label: "time's up!", emoji: '⏰', side: true };
  const metaOf = id => (id === 'alarm' ? ALARM_META : st.actions.find(a => a.id === id)) || {};

  // ------------------------------------------------------------ one buddy
  class Actor {
    constructor(el) {
      if (!el) {
        el = document.createElement('div');
        el.className = 'pet';
        el.innerHTML = '<div class="actor"><img class="pix" alt="" draggable="false">'
          + '<div class="vec"></div><img class="prop" alt="" draggable="false" hidden></div>';
        stage.insertBefore(el, $('ground'));
      }
      this.el = el;
      this.actor = el.querySelector('.actor');
      this.pix = el.querySelector('.pix');
      this.vec = el.querySelector('.vec');
      this.prop = el.querySelector('.prop');
      this.mascot = '';
      this.style = '';
      this.action = null;
      this.x = 20;
      this.dir = 1;
      this.walk = 0;
      this.hop = 0;
      this.blink = 0;
      this.nextBlink = rand(30, 150);
      this.target = null;          // group scenes: x to walk to
      this.holdGesture = false;    // keep a looping gesture (alarm shake)
      this.actor.addEventListener('animationend', () => {
        if (!this.holdGesture) this.actor.className = 'actor';
      });
    }

    setArt(mascot, style, svg) {
      if (mascot === this.mascot && style === this.style) return;
      this.mascot = mascot;
      this.style = style;
      this.el.classList.toggle('cartoon', style === 'cartoon');
      this.el.classList.toggle('pixel', style !== 'cartoon');
      this.vec.innerHTML = style === 'cartoon' ? (svg || '') : '';
      this.pix.removeAttribute('src');
      this.setProp(this.action);
    }

    frame(blink, foot) {
      return asset(window.SPRITES, `${this.mascot}_${blink}${foot}.png`);
    }

    setProp(action) {
      this.action = action;
      if (!action) { this.prop.hidden = true; return; }
      const meta = metaOf(action);
      this.prop.src = asset(window.PROPS, `${action}.${this.style === 'cartoon' ? 'svg' : 'png'}`);
      this.prop.className = 'prop';
      void this.prop.offsetWidth;                // restart float / rise animations
      this.prop.classList.toggle('side', !!meta.side);
      this.prop.classList.toggle('float', meta.motion === 'float');
      this.prop.classList.toggle('rise', meta.motion === 'rise');
      this.prop.hidden = false;
    }

    gesture(name) {
      name = name || pick(GESTURES);
      this.actor.className = 'actor';
      void this.actor.offsetWidth;               // restart the CSS animation
      this.actor.className = `actor g-${name}`;
    }

    get width() { return this.el.offsetWidth || 40; }

    // blink timer; returns true while the eyes are shut
    tickBlink() {
      if (this.blink > 0) this.blink--;
      else if (--this.nextBlink <= 0) { this.blink = 6; this.nextBlink = rand(45, 150); }
      if (this.hop > 0) this.hop--;
      return this.blink > 0;
    }

    render(moving, closed) {
      const foot = moving ? Math.floor(this.walk) % 2 : 0;
      let bob = 0;
      if (this.style === 'cartoon') {
        this.vec.classList.toggle('blink', closed);
        this.vec.classList.toggle('step-l', moving && foot === 0);
        this.vec.classList.toggle('step-r', moving && foot === 1);
        bob = moving ? foot : 0;                 // gentle bounce per step
      } else {
        const src = this.frame(closed ? 1 : 0, foot);
        if (this.pix.getAttribute('src') !== src) this.pix.setAttribute('src', src);
      }
      const hopY = this.hop > 0 ? Math.round(12 * (1 - ((this.hop - 7) / 7) ** 2)) : 0;
      this.el.style.transform =
        `translate(${Math.round(this.x)}px, ${-hopY - bob}px) scaleX(${this.dir < 0 ? -1 : 1})`;
    }

    remove() { this.el.remove(); }
  }

  const main = new Actor($('pet'));
  const badge = document.createElement('div');   // emoji above the head while busy
  badge.id = 'doing';
  badge.hidden = true;
  stage.appendChild(badge);
  let guests = [];                 // extra buddies in group scenes

  const st = {
    quiz: false, levelName: '', actions: [], scene: null,
    pause: 0, sprint: 0,
    focused: true, unfocused: 0, sleeping: false,
    revealed: true, showCard: true, word: null,
    actT: 0, alarm: 0, hovering: false,
    clock: {}, choreo: 0, cast: [], groupAct: null, actFrame: 0,
    actEvery: 2, nextActAt: Date.now() + 30000,  // first activity ~30 s in
  };

  // ------------------------------------------------------------ background
  function setScene(sc, style) {
    st.scene = sc;
    document.body.classList.toggle('has-scene', !!sc);
    if (!sc) { scene.hidden = true; return; }
    scene.hidden = false;
    scene.className = `${style === 'cartoon' ? 'cartoon' : 'pixel'}${sc.strength === 'soft' ? ' soft' : ''}`;
    scene.style.background = sc.top;
    scene.querySelector('.floor').style.background = sc.floor;
    const art = scene.querySelector('.art');
    const src = asset(window.SCENES, `${sc.id}.${style === 'cartoon' ? 'svg' : 'png'}`);
    if (art.getAttribute('src') !== src) art.setAttribute('src', src);
  }

  const grouped = () => guests.length > 0;

  function setGuests(list, style) {
    const ids = list.map(g => g.mascot).join();
    const changed = ids !== guests.map(g => g.mascot).join();
    if (changed) {
      guests.forEach(g => g.remove());
      guests = list.map(() => new Actor());
      guests.forEach(g => {
        g.el.addEventListener('click', () => poke(g));
        g.x = main.x;
      });
    }
    list.forEach((g, i) => guests[i].setArt(g.mascot, style, g.svg));
    // line-up: main buddy in the middle
    st.cast = guests.length ? [guests[0], main, ...guests.slice(1)] : [main];
    if (changed) endGroupActivity();
    if (changed && grouped()) { stopAction(); placeCast(); }
  }

  function slotX(i) {
    const n = st.cast.length;
    return stage.clientWidth / 2 + (i - (n - 1) / 2) * SLOT_GAP - main.width / 2;
  }

  function placeCast() {
    st.cast.forEach((a, i) => { a.target = slotX(i); });
    st.choreo = FPS;
  }

  // Group routines, by the scene's style of moving together:
  //   dance   (party)     synced moves, ripples, solos, swaps, group hops
  //   stage   (fanmeet)   synced moves, solos with the others cheering, bows
  //   splash  (Songkran)  water fight: splashes back and forth, dodging hops
  //   hangout (bar, Loy Krathong) calm nods, little wiggles, the odd heart
  const ROUTINES = {
    dance: ['together', 'together', 'ripple', 'solo', 'swap', 'jump'],
    stage: ['together', 'ripple', 'solo', 'solo', 'swap', 'bow'],
    splash: ['splash', 'splash', 'splash', 'jump', 'swap', 'ripple'],
    hangout: ['nod', 'nod', 'heart', 'wiggle', 'swap', 'rest'],
  };

  function burst(a, text, cls) {
    const p = document.createElement('div');
    p.className = `burst ${cls || ''}`;
    p.textContent = text;
    p.style.left = `${Math.round(a.x + a.width / 2 - 6 + rand(-6, 6))}px`;
    stage.appendChild(p);
    setTimeout(() => p.remove(), 1200);
  }

  function choreograph() {
    const cast = st.cast;
    const moves = (st.scene && st.scene.moves) || 'dance';
    const r = pick(ROUTINES[moves] || ROUTINES.dance);
    let pause = rand(1.8, 3.2);
    if (r === 'together') {
      const g = pick(moves === 'dance' ? ['dance', 'wiggle', 'spin'] : ['dance', 'nod', 'wiggle']);
      cast.forEach(a => a.gesture(g));
    } else if (r === 'ripple') {
      const g = pick(['wiggle', 'spin', 'dance']);
      cast.forEach((a, i) => setTimeout(() => a.gesture(g), i * 220));
    } else if (r === 'solo') {
      const star = pick(cast);
      star.hop = 14;
      star.gesture(pick(['spin', 'dance']));
      cast.filter(a => a !== star).forEach(a => setTimeout(() => a.gesture('nod'), 300));
    } else if (r === 'swap' && cast.length > 1) {
      const i = Math.floor(Math.random() * (cast.length - 1));
      [cast[i], cast[i + 1]] = [cast[i + 1], cast[i]];
      placeCast();
      return;
    } else if (r === 'jump') {
      cast.forEach((a, i) => setTimeout(() => { a.hop = 14; }, i * 120));
    } else if (r === 'bow') {
      cast.forEach(a => a.gesture('stretch'));
    } else if (r === 'splash') {             // one splashes, the target dodges
      const from = pick(cast);
      const to = pick(cast.filter(a => a !== from)) || from;
      from.dir = to.x > from.x ? 1 : -1;
      from.gesture('nod');
      burst(from, '💦', 'water');
      setTimeout(() => { to.hop = 14; to.gesture('wiggle'); burst(to, '💧', 'water'); }, 350);
      pause = rand(1.2, 2.2);
    } else if (r === 'nod') {
      cast.forEach((a, i) => setTimeout(() => a.gesture('nod'), i * 400));
      pause = rand(3, 5);
    } else if (r === 'heart') {
      const a = pick(cast);
      a.gesture('wiggle');
      burst(a, '♥', 'love');
      pause = rand(3, 5);
    } else if (r === 'wiggle') {
      pick(cast).gesture('wiggle');
      pause = rand(3, 5);
    } else {                                     // rest: just enjoy the view
      pause = rand(4, 6);
    }
    st.choreo = Math.round(pause * FPS);
  }

  // ------------------------------------------------------------ activities
  // Scene activities only come out in their own scene; the general ones
  // can happen anywhere.
  const usable = () => st.actions.filter(a => !a.scene || (st.scene && a.scene === st.scene.id));

  function activityWord(id) {
    const meta = metaOf(id);
    if (!meta.word || id === 'alarm') return;
    showWord({ thai: meta.word[0], rom: meta.word[1], eng: meta.word[2],
      sceneLabel: meta.emoji, activity: true }, false);
  }

  // per-frame extras while an activity runs
  function motionStep(a, meta, f) {
    if (meta.motion === 'hop' && f % 32 === 0) a.hop = 14;
    else if (meta.motion === 'sparkle' && f % 24 === 0) burst(a, '✨');
    else if (meta.motion === 'confetti' && f % 18 === 0) burst(a, pick(['🎉', '🎊', '✨']));
    else if (meta.motion === 'hearts' && f % 30 === 0) burst(a, '♥', 'love');
    else if (meta.motion === 'wave' && f % 40 === 0) a.gesture(meta.closed ? 'nod' : 'wiggle');
  }

  function startAction(id, seconds) {
    main.setProp(id);
    st.actT = seconds * FPS;
    st.actFrame = 0;
    st.pause = 0;
    activityWord(id);
    // turn away from a nearby wall so side props aren't cut off
    const room = stage.clientWidth - main.width;
    if (main.dir > 0 && main.x > room - 40) main.dir = -1;
    if (main.dir < 0 && main.x < 40) main.dir = 1;
  }

  function stopAction() {
    if (main.action) {                          // next one in ~actEvery minutes
      st.nextActAt = Date.now() + st.actEvery * 60000 * rand(0.85, 1.15);
    }
    main.setProp(null);
    st.actT = 0;
  }

  // mostly this scene's own activities, then its favourite general ones
  function randomActivity() {
    const all = usable();
    if (!all.length) return null;
    const own = all.filter(a => a.scene);
    const general = all.filter(a => !a.scene);
    const fav = general.filter(a => st.scene && (st.scene.acts || []).includes(a.id));
    const r = Math.random();
    const list = own.length && r < 0.6 ? own : fav.length && r < 0.85 ? fav : general;
    return pick(list.length ? list : all).id;
  }

  // Group scenes: one buddy or the whole group does a scene activity
  // together (everyone lets go of their lanterns, clinks glasses...).
  const TOGETHER = new Set(['cheers', 'skylantern', 'krathong', 'sparkler', 'lightstick', 'watergun', 'confetti', 'partyhat']);
  function startGroupActivity(id) {
    const own = usable().filter(a => a.scene);
    id = id || (own.length ? pick(own).id : randomActivity());
    if (!id) return;
    const members = TOGETHER.has(id) || Math.random() < 0.35 ? st.cast.slice() : [pick(st.cast)];
    members.forEach(a => a.setProp(id));
    st.groupAct = { id, members, f: 0, frames: Math.round(rand(15, 25) * FPS) };
    activityWord(id);
  }

  function endGroupActivity() {
    if (!st.groupAct) return;
    st.groupAct.members.forEach(a => a.setProp(null));
    st.groupAct = null;
    st.nextActAt = Date.now() + st.actEvery * 60000 * rand(0.85, 1.15);
    st.choreo = FPS;
  }

  function heartPop(a) {
    const h = document.createElement('div');
    h.className = 'heart';
    h.textContent = '♥';
    h.style.left = `${Math.round(a.x + a.width / 2 - 5)}px`;
    stage.appendChild(h);
    setTimeout(() => h.remove(), 1100);
  }

  function label() {
    if (st.alarm) return "⏰ time's up!";
    if (st.sleeping) return 'having a nap · click to wake me';
    if (main.action) return metaOf(main.action).label || '';
    if (st.groupAct) return metaOf(st.groupAct.id).label || '';
    if (grouped()) {
      return { dance: 'dancing with friends ♪', stage: 'on stage at the fanmeet!',
        splash: 'water fight! 💦', hangout: 'hanging out with a friend' }[st.scene.moves] || 'with friends';
    }
    return 'strolling around · click for a Thai word';
  }

  // ------------------------------------------------------------ word card
  // The word card stays up (unless you hide it with the eye button) and the
  // extension swaps in a new word every few minutes.
  function showWord(w, hop = true) {
    if (!w) return;
    st.word = w;
    bubble.classList.remove('fresh');
    void bubble.offsetWidth;
    bubble.classList.add('fresh');                // little flash on each new word
    $('thai').textContent = w.thai;
    $('rom').textContent = w.rom;
    $('eng').textContent = w.eng;
    const lv = st.levelName.split(' — ')[0];
    $('level').textContent = w.activity ? w.sceneLabel : w.sceneLabel ? `${w.sceneLabel} · ${lv}` : lv;
    st.revealed = !st.quiz;
    bubble.classList.toggle('quiz', !st.revealed);
    bubble.hidden = !st.showCard;
    if (hop && st.showCard) main.hop = 14;
  }

  // ------------------------------------------------------------ footer
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
      t.textContent = `${icon} ${c.timer.label} · ${fmt(c.timer.end - now)} left`;
      t.className = '';
    } else {
      t.textContent = '';
    }
    if (!c.workStart) { w.textContent = ''; return; }
    const worked = `💼 Worked ${short(now - c.workStart)}`;
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

  // ------------------------------------------------------------ messages
  window.addEventListener('message', e => {
    const m = e.data;
    if (m.type === 'state') {
      st.actions = m.actions || [];
      if (main.action && !st.actions.some(a => a.id === main.action) && !st.alarm) stopAction();
      main.setArt(m.mascot, m.style, m.svg);
      setScene(m.scene, m.style);
      setGuests(m.companions || [], m.style);
      st.quiz = m.quiz;
      st.levelName = m.levelName;
      st.showCard = m.showWord !== false;
      if (m.activityEvery && m.activityEvery !== st.actEvery) {
        st.actEvery = m.activityEvery;
        st.nextActAt = Math.min(st.nextActAt, Date.now() + st.actEvery * 60000);
      }
      bubble.hidden = !st.showCard || !st.word;
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
      main.gesture(m.name);
    } else if (m.type === 'activity') {
      if (!st.alarm) {
        if (st.sleeping) setFocus(true);
        if (grouped()) { endGroupActivity(); startGroupActivity(m.id); } else startAction(m.id, rand(20, 30));
        main.gesture('nod');
      }
    } else if (m.type === 'alarm') {
      if (m.on) {
        st.alarm = ALARM_MAX;
        st.alarmLabel = m.label;
        if (st.sleeping) setFocus(true);
        startAction('alarm', 3600);
        main.holdGesture = true;
        main.actor.className = 'actor g-shake';
      } else if (st.alarm) {
        st.alarm = 0;
        main.holdGesture = false;
        main.actor.className = 'actor';
        stopAction();
        main.gesture('dance');
      }
      lastFooter = 0;
    }
  });

  function setFocus(f) {
    if (f && st.sleeping) {
      st.sleeping = false;
      zzz.hidden = true;
      st.cast.forEach(a => { a.hop = 14; });
      if (main.action === 'sleep') stopAction();
    }
    st.focused = f;
    st.unfocused = 0;
  }

  function poke(a) {
    a.hop = 14;
    heartPop(a);
    if (st.sleeping) { setFocus(true); return; }
    if (a === main && !st.alarm && !grouped()) {
      if (main.action && Math.random() < 0.5) stopAction();
      else if (!main.action && st.actions.length && Math.random() < 0.4) {
        startAction(randomActivity(), 8 + Math.random() * 7);
      }
    }
    if (!st.alarm) a.gesture();
    vscode.postMessage({ type: 'poke' });
  }

  main.el.addEventListener('click', () => poke(main));
  main.el.addEventListener('mouseenter', () => { st.hovering = true; });
  main.el.addEventListener('mouseleave', () => { st.hovering = false; tip.hidden = true; });
  bubble.addEventListener('click', () => {
    if (!st.revealed) {                          // quiz: reveal the meaning
      st.revealed = true;
      bubble.classList.remove('quiz');
    } else {
      vscode.postMessage({ type: 'poke' });      // next word
    }
  });
  window.addEventListener('resize', () => { if (grouped()) placeCast(); });

  // ------------------------------------------------------------ main loop
  function walkTo(a) {                           // returns true while walking
    if (a.target === null) return false;
    const d = a.target - a.x;
    if (Math.abs(d) <= 1.2) {
      a.x = a.target;
      a.target = null;
      a.dir = a.x + a.width / 2 < stage.clientWidth / 2 ? 1 : -1;   // face the middle
      return false;
    }
    a.dir = d > 0 ? 1 : -1;
    a.x += a.dir * 1.2;
    a.walk += 0.15;
    return true;
  }

  function tickSolo(width) {
    const due = st.clock.breakAt && Date.now() >= st.clock.breakAt;
    if (st.sleeping || st.alarm) return false;
    if (main.action) {
      const meta = metaOf(main.action);
      motionStep(main, meta, ++st.actFrame);
      if (--st.actT <= 0) { stopAction(); return false; }
      if (!meta.motion && Math.random() < 0.003) main.gesture();
      if (meta.motion === 'ride') {               // tuk-tuk ride across the floor
        main.x += main.dir * 1.8;
        main.walk += 0.2;
        const max = Math.max(0, width - main.width);
        if (main.x <= 0) { main.x = 0; main.dir = 1; }
        if (main.x >= max) { main.x = max; main.dir = -1; }
        return true;
      }
      return false;
    }
    if (st.pause > 0) {
      st.pause--;
      if (Math.random() < 0.004) main.gesture();
      return false;
    }
    if (st.sprint > 0) st.sprint--;
    else if (Math.random() < 0.0015) st.sprint = Math.round(rand(45, 90));  // whole frames
    const speed = st.sprint > 0 ? 2.6 : 1;       // px per frame (~30 px/s walking)
    main.x += main.dir * speed;
    main.walk += st.sprint > 0 ? 0.28 : 0.14;
    const max = Math.max(0, width - main.width);
    if (main.x <= 0) { main.x = 0; main.dir = 1; }
    if (main.x >= max) { main.x = max; main.dir = -1; }
    if (st.sprint <= 0 && Math.random() < 0.003) st.pause = rand(15, 60);
    if (st.sprint <= 0 && Math.random() < 0.002) main.dir *= -1;
    // a new activity about every st.actEvery minutes (sooner, as coffee,
    // when a break is due); each one lasts 20-30 s
    const now = Date.now();
    const ready = now >= st.nextActAt || (due && now >= st.nextActAt - st.actEvery * 45000);
    if (st.sprint <= 0 && st.actions.length && ready) {
      const id = due && st.actions.some(a => a.id === 'coffee') ? 'coffee' : randomActivity();
      if (id) startAction(id, rand(20, 30));
    }
    return true;
  }

  function tick() {
    const width = stage.clientWidth;

    // alarm rings for a while, then the buddy gives up
    if (st.alarm > 0 && --st.alarm === 0) {
      main.holdGesture = false;
      main.actor.className = 'actor';
      stopAction();
      lastFooter = 0;
    }

    // nap when the editor isn't focused
    if (!st.focused && !st.sleeping && !st.alarm && ++st.unfocused > SLEEP_AFTER) {
      st.sleeping = true;
      zzz.hidden = false;
      stopAction();
    }

    if (grouped()) {
      let walking = false;
      const ga = st.groupAct;
      const gaMeta = ga ? metaOf(ga.id) : {};
      for (const a of st.cast) {
        const moving = !st.sleeping && walkTo(a);
        walking = walking || moving;
        const busyEyes = ga && gaMeta.closed && ga.members.includes(a);
        a.render(moving, a.tickBlink() || st.sleeping || !!busyEyes);
      }
      if (!walking && !st.sleeping && !st.alarm) {
        if (ga) {
          ga.f++;
          ga.members.forEach(a => motionStep(a, gaMeta, ga.f));
          if (ga.f >= ga.frames) endGroupActivity();
        } else if (Date.now() >= st.nextActAt && usable().length) {
          startGroupActivity();
        } else if (--st.choreo <= 0) {
          choreograph();
        }
      }
    } else {
      const moving = tickSolo(width);
      const closed = main.tickBlink() || st.sleeping || !!(main.action && metaOf(main.action).closed);
      main.render(moving, closed);
    }
    zzz.style.left = `${Math.round(main.x + main.width - 10)}px`;
    const busy = main.action && !st.sleeping ? metaOf(main.action).emoji || ''
      : st.groupAct && st.groupAct.members.includes(main) ? metaOf(st.groupAct.id).emoji || '' : '';
    badge.hidden = !busy;
    if (busy) {
      if (badge.textContent !== busy) badge.textContent = busy;
      badge.style.left = `${Math.round(main.x + main.width / 2 - 7)}px`;
    }

    if (st.hovering) {
      tip.textContent = label();
      tip.hidden = false;
      const tw = tip.offsetWidth;
      tip.style.left = `${Math.round(Math.min(Math.max(2, main.x + main.width / 2 - tw / 2), width - tw - 2))}px`;
    }

    renderFooter();
  }

  setInterval(tick, 1000 / FPS);
  vscode.postMessage({ type: 'ready' });
})();
