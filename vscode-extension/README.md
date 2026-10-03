# ThaiDevPet for VS Code & Kiro

A GMMTV buddy (MuvMuv, Lunar, Any, Jewel, Vimmy, Wesley, plus Goldie and
LOLO), in cartoon or pixel style, that walks along the bottom of the **ThaiDevPet** panel in the
Explorer and teaches you a Thai word every few minutes.

## Panel pet or screen pet — you choose

Nothing starts on its own. When the editor opens, ThaiDevPet asks which pet you
want (change this with `thaidevpet.startup`), and the 🐾 in the status bar
switches any time:

- **Panel pet** — walks inside the ThaiDevPet panel in the Explorer (any OS).
- **Screen pet** — the original `kiro_pet.py` that walks around the edge of the
  editor window (Windows only). The extension starts it with your buddy,
  style and Thai level, and stops it when the editor closes.
- **Both** or **Neither** (timers and the status-bar word keep working).

If the screen pet used to start at Windows login, run `remove_autostart.bat`
from the ThaiDevPet folder once.

- **Click the buddy** for a new word. **Click the bubble** to hide it (or to
  reveal the meaning in quiz mode).
- Right-click the panel (or use its title buttons): change buddy, switch
  art style (cartoon / pixel), choose Thai level, next word.
- The **Thai word card** stays at the top of the panel and changes on its own
  every 2 minutes (`thaidevpet.wordIntervalMinutes`). Click it for the next
  word; the 👁 button on the panel title (or right-click → Show / hide Thai
  word card) hides or shows it.
- The current word also sits in the status bar; click it for the next one.
- **Timer / alarm…** (⏱ button or right-click): countdowns (5–60 min,
  Pomodoro, custom) or an alarm at a clock time like `15:30` / `3:30pm`.
  The countdown shows in the panel footer and status bar; when it ends you
  get a notification (snooze 5 min) and the buddy rings an alarm clock.
- **Break reminder…**: like the desktop buddy, it tracks how long you've
  worked and nudges you every 30/45/60/90 min (or pick **No break
  reminders** to show just the worked time). Being away from the editor
  for 5+ min counts as a break and resets the clock.
- The buddy stops now and then for an activity (coffee, music, reading,
  games, noodles, TV…) and does little gestures (wiggle, dance, spin,
  stretch, nod). Hover over it to see what it's up to, or right-click → **Do an activity…**
  to pick one.
- The buddy naps when the editor loses focus, and wakes when you come back.

## Backgrounds

Right-click the panel → **Background…** (or the paint-can button). Pick one
scene, **shuffle** a category, shuffle everything, or no background:

| Category | Scenes |
| --- | --- |
| **Everyday** (default shuffle) | 💼 Office · ☕ Café · 🛏️ Bedroom · 🌧️ Rainy day |
| **Thailand** | 🛕 Wat Arun · 🛶 Floating market · 🏝️ Krabi beach · 🏮 Yaowarat · 🛺 Tuk-tuk street |
| **Festivals** | 💦 Songkran (3-buddy water fight) · 🪷 Loy Krathong (2 buddies) |
| **Party** | 🎤 SAMTUABAHT Fanmeet (3 on stage) · 🪩 Dance party (3) · 🍸 Rooftop bar (2) |

- In group scenes friends join your buddy: dance routines, stage shows with
  solos and bows, splash fights, or a calm hangout. **Party buddies…** picks
  who joins (or leave it to chance).
- Alone, the buddy picks activities that suit the scene (laptop in the
  office, bubble tea at the market, a nap in the bedroom…).
- **Full colour** or **Soft** (faded into your theme); cartoon and pixel art.
- Each scene brings ~20–30 Thai words, by level, mixed into the word card.

## Settings

| Setting | Default | What it does |
| --- | --- | --- |
| `thaidevpet.startup` | `ask` | `ask`, `panel`, `screen`, `both` or `none` |
| `thaidevpet.screenPet.script` | *(empty)* | Path to `kiro_pet.py` (asked once if empty) |
| `thaidevpet.screenPet.python` | *(empty)* | Python for the screen pet (default `pythonw`, then `pyw`) |
| `thaidevpet.mascot` | `muvmuv` | Which buddy walks around |
| `thaidevpet.style` | `cartoon` | `cartoon` or `pixel` art |
| `thaidevpet.scene` | `shuffle:everyday` | A scene id, `shuffle`, `shuffle:<category>` or `none` |
| `thaidevpet.sceneShuffleMinutes` | `30` | How often a shuffle switches scene |
| `thaidevpet.sceneStrength` | `full` | `full` or `soft` |
| `thaidevpet.sceneWords` | `true` | Mix in the scene's Thai words |
| `thaidevpet.partyBuddies` | `[]` | Up to 2 friends for the stage / party |
| `thaidevpet.thaiLevel` | `beginner` | `beginner`, `elementary`, `intermediate`, `advanced` or `all` |
| `thaidevpet.wordIntervalMinutes` | `2` | New word every N focused minutes |
| `thaidevpet.activities` | `true` | Little activities with props |
| `thaidevpet.breakReminderMinutes` | `60` | 0 (off), 30, 45, 60 or 90 |
| `thaidevpet.breakResetMinutes` | `5` | Time away that counts as a break |
| `thaidevpet.showWord` | `true` | Show the Thai word card |
| `thaidevpet.quizMode` | `false` | Blur the English until you click the bubble |
| `thaidevpet.showInStatusBar` | `true` | Show the word in the status bar |

## Install / update

```sh
cd vscode-extension
npx @vscode/vsce package --skip-license --allow-missing-repository
code --install-extension thaidevpet-0.6.3.vsix     # VS Code
kiro --install-extension thaidevpet-0.6.3.vsix     # Kiro
```

Pixel sprites and words come from the Python app (`sprites.py`,
`thai_vocab.py`); cartoon art lives in `tools/cartoon.py` and backgrounds in
`tools/scenes.py`.
After editing those, re-run `python3 tools/export_web.py` and package again.
