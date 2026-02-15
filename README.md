# KotanPY

A collection of open-source Python projects by **kotan123**.

## Projects

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

- Python 3.8+
- `pygame` (for NeonSnake & MiniGamesArcade)
- `tkinter` (for Smart Calculator, included with Python)

## Quick Start

```bash
# Install pygame for the snake game
pip install pygame

# Run Mini Games Arcade
python MiniGamesArcade/mini_games.pyw

# Run NeonSnake
python NeonSnake/snake.pyw

# Run Smart Calculator
python Calculators/smart_calculator.pyw

# Run Terminal Calculator
python Calculators/calculator.py
```

## License

MIT License — free to use, modify, and distribute. See [LICENSE](./LICENSE).
