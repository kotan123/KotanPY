# KotanPY

A collection of open-source Python projects by **Kotan123**.

## Projects

### [PyLearn](./PyLearn) 🆕
Interactive Python Learning Desktop App. Built with PyQt6.

- **20 structured lessons** — from variables to data structures
- **Code editor** — syntax highlighting, bracket matching, multi-tab
- **4 themes** — Midnight, Ocean, Sunset, Forest
- **Built-in console** — run code with Ctrl+Enter

### [PasswordGenerator](./PasswordGenerator)
Secure password generator with a dark space-themed UI. Built with CustomTkinter.

- **Adjustable length** — 4 to 64 characters
- **Character types** — uppercase, lowercase, digits, symbols
- **Strength meter** — 4-segment visual bar
- **Copy to clipboard** — one-click copy
- **Recent history** — last 5 generated passwords

### [NeonSnake](./NeonSnake)
A feature-rich Snake game built with Pygame. 10 color themes, 3 game modes, smooth animations, particle effects, powerups and combo system.

- **Classic Mode** — no walls, snake wraps around
- **Walls Mode** — deadly walls + level obstacles
- **Speed Mode** — starts fast, gets faster

### [MiniGamesArcade](./MiniGamesArcade)
12 mini games in one app, built with Pygame. No external assets — everything is drawn with code.

- **Games:** Pong, Flappy Bird, Breakout, Space Invaders, Asteroids, Memory Match, Dodge Master, Color Catch, Meteor Storm, Platform Jump, Tank Battle, Rhythm Tap
- **4 color themes** — Neon, Ocean, Sunset, Matrix
- **Features:** particle effects, double jump, control hints, progressive difficulty

### [Calculators](./Calculators)
Two calculator apps:

- **Smart Calculator** (`smart_calculator.pyw`) — GUI calculator with 3 themes (Dark / Light / Neon Red), neon-glow buttons, floating particles, scientific functions
- **Terminal Calculator** (`calculator.py`) — colorful terminal calculator with expression evaluation, history, and scientific functions

## Requirements

- Python 3.10+
- `PyQt6` (for PyLearn)
- `pygame` (for NeonSnake & MiniGamesArcade)
- `customtkinter`, `Pillow`, `pyperclip` (for PasswordGenerator)
- `tkinter` (for Smart Calculator, included with Python)

## Quick Start

```bash
# Install dependencies
pip install PyQt6 pygame customtkinter Pillow pyperclip

# Run PyLearn
python PyLearn/python_learner.py

# Run Password Generator
python PasswordGenerator/password_generator.pyw

# Run Mini Games Arcade
python MiniGamesArcade/mini_games.pyw

# Run NeonSnake
python NeonSnake/snake.pyw

# Run Smart Calculator
python Calculators/smart_calculator.pyw
```

## Downloads

Standalone `.exe` files available in [Releases](https://github.com/kotan123/KotanPY/releases) — no installation required.

## License

MIT License — free to use, modify, and distribute. See [LICENSE](./LICENSE).

---

**By Kotan123**
