# KiroPet for VS Code & Kiro

A GMMTV buddy (MuvMuv, Lunar, Any, Jewel, Vimmy, Wesley, plus Goldie and
LOLO), in cartoon or pixel style, that walks along the bottom of the **KiroPet** panel in the
Explorer and teaches you a Thai word every few minutes.

## Panel pet or screen pet — you choose

Nothing starts on its own. When the editor opens, KiroPet asks which pet you
want (change this with `kiropet.startup`), and the 🐾 in the status bar
switches any time:

- **Panel pet** — walks inside the KiroPet panel in the Explorer (any OS).
- **Screen pet** — the original `kiro_pet.py` that walks around the edge of the
  editor window (Windows only). The extension starts it with your buddy,
  style and Thai level, and stops it when the editor closes.
- **Both** or **Neither** (timers and the status-bar word keep working).

If the screen pet used to start at Windows login, run `remove_autostart.bat`
from the KiroPet folder once.

- **Click the buddy** for a new word. **Click the bubble** to hide it (or to
  reveal the meaning in quiz mode).
- Right-click the panel (or use its title buttons): change buddy, switch
  art style (cartoon / pixel), choose Thai level, next word.
- The current word also sits in the status bar; click it for the next one.
- **Timer / alarm…** (⏱ button or right-click): countdowns (5–60 min,
  Pomodoro, custom) or an alarm at a clock time like `15:30` / `3:30pm`.
  The countdown shows in the panel footer and status bar; when it ends you
  get a notification (snooze 5 min) and the buddy rings an alarm clock.
- **Break reminder…**: like the desktop buddy, it tracks how long you've
  worked and nudges you every 30/45/60/90 min. Being away from the editor
  for 5+ min counts as a break and resets the clock.
- The buddy stops now and then for an activity (coffee, music, reading,
  games, noodles, TV…) and does little gestures (wiggle, dance, spin,
  stretch, nod). Hover over it to see what it's up to, or right-click → **Do an activity…**
  to pick one.
- The buddy naps when the editor loses focus, and wakes when you come back.

## Settings

| Setting | Default | What it does |
| --- | --- | --- |
| `kiropet.startup` | `ask` | `ask`, `panel`, `screen`, `both` or `none` |
| `kiropet.screenPet.script` | *(empty)* | Path to `kiro_pet.py` (asked once if empty) |
| `kiropet.screenPet.python` | *(empty)* | Python for the screen pet (default `pythonw`, then `pyw`) |
| `kiropet.mascot` | `muvmuv` | Which buddy walks around |
| `kiropet.style` | `cartoon` | `cartoon` or `pixel` art |
| `kiropet.thaiLevel` | `beginner` | `beginner`, `elementary`, `intermediate`, `advanced` or `all` |
| `kiropet.wordIntervalMinutes` | `5` | New word every N focused minutes |
| `kiropet.activities` | `true` | Little activities with props |
| `kiropet.breakReminderMinutes` | `60` | 0 (off), 30, 45, 60 or 90 |
| `kiropet.breakResetMinutes` | `5` | Time away that counts as a break |
| `kiropet.quizMode` | `false` | Blur the English until you click the bubble |
| `kiropet.showInStatusBar` | `true` | Show the word in the status bar |

## Install / update

```sh
cd vscode-extension
npx @vscode/vsce package --skip-license --allow-missing-repository
code --install-extension kiropet-0.4.0.vsix     # VS Code
kiro --install-extension kiropet-0.4.0.vsix     # Kiro
```

Pixel sprites and words come from the Python app (`sprites.py`,
`thai_vocab.py`); cartoon art lives in `tools/cartoon.py`.
After editing those, re-run `python3 tools/export_web.py` and package again.
