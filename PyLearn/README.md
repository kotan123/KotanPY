# PyLearn — By Kotan123

**Interactive Python Learning Desktop App**

A modern, feature-rich desktop application for learning Python — built with PyQt6. Includes 20 structured lessons, an advanced code editor with Smart Autocomplete, and 4 beautiful themes.


---

## Features

### 💻 Code Editor
- **Smart Autocomplete** — 400+ suggestions including:
  - Python keywords, built-in functions, exceptions, dunder methods
  - String, list, dict, set, and file methods
  - Standard library modules
  - **30+ code snippets** (classes, functions, comprehensions, decorators, etc.)
  - Identifiers extracted from your current code in real-time
- **Tab to insert** — press `Tab` or `Enter` to accept a suggestion
- **Syntax highlighting** — keywords, strings, numbers, comments, decorators, builtins
- **Current line highlight** — always see where your cursor is
- **Bracket matching** — highlights matching `()`, `[]`, `{}`
- **Auto-indent** — automatically indents after `:`
- **Toggle comment** — `Ctrl+/` to comment/uncomment selected lines
- **Line numbers** — with active line number highlighting
- **Multi-tab support** — open multiple files in tabs

### 📁 File Operations
- **New** (`Ctrl+N`) — create a new file tab
- **Open** (`Ctrl+O`) — open any `.py` / `.pyw` file
- **Save** (`Ctrl+S`) — save the current file
- **Save As** — save with a new filename

### ▶️ Console
- **Run code** (`Ctrl+Enter`) — execute your code
- **Colored output** — green for stdout, red for stderr
- **Execution time** — displayed after each run
- **Timeout protection** — 15-second timeout prevents infinite loops

### 📚 20 Structured Lessons

| # | Topic | Description |
|---|-------|-------------|
| 1 | Variables & Data Types | `int`, `float`, `str`, `bool`, type conversion |
| 2 | Strings | Slicing, f-strings, methods |
| 3 | Numbers & Math | Arithmetic, `math` module |
| 4 | Lists | Create, modify, slice, comprehensions |
| 5 | Tuples & Sets | Immutability, set operations |
| 6 | Conditionals | `if`/`elif`/`else`, ternary, `match`/`case` |
| 7 | Loops | `for`, `while`, `break`, `continue`, `enumerate` |
| 8 | Functions | `def`, `*args`, `**kwargs`, `lambda` |
| 9 | Dictionaries | CRUD, comprehensions, `.get()` |
| 10 | File I/O | Read, write, append, `with` |
| 11 | Error Handling | `try`/`except`/`finally`, custom exceptions |
| 12 | OOP Basics | Classes, `__init__`, methods, `__str__` |
| 13 | List Comprehensions | Nested, conditional, dict/set comprehensions |
| 14 | Modules & Imports | `import`, `from`, packages |
| 15 | String Formatting | f-strings, format spec, alignment |
| 16 | Decorators | `@decorator`, parameterized decorators |
| 17 | Generators | `yield`, generator expressions, pipelines |
| 18 | Context Managers | `with`, `__enter__`/`__exit__`, `@contextmanager` |
| 19 | Regular Expressions | `re.search`, `re.findall`, `re.sub` |
| 20 | Data Structures | `Counter`, `defaultdict`, `deque`, `namedtuple` |

Each lesson includes theory, runnable example code, and "Try in Editor" button.

### 🎨 Themes

| Theme | Style |
|-------|-------|
| **Midnight** | Dark blue/gray — easy on the eyes |
| **Ocean** | Deep navy blue tones |
| **Sunset** | Warm dark reds and oranges |
| **Forest** | Natural dark greens |

All themes feature floating particle background animation and smooth transitions.

---

## Installation

### Option 1: Standalone `.exe` (Windows)

Download `PyLearn.exe` from [Releases](https://github.com/kotan123/KotanPY/releases) — no installation required. Double-click to run.

> **Note:** Python must be installed on the system for the Run button (code execution). The app itself runs standalone.

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/kotan123/KotanPY.git
cd KotanPY/PyLearn

# Install dependencies
pip install PyQt6

# Run the app
python python_learner.py
```

Or use the `.pyw` launcher (no console window on Windows):
```bash
pythonw python_learner.pyw
```

### Build `.exe` Yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico --name=PyLearn --add-data "icon.ico;." python_learner.py
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Run code |
| `Ctrl+S` | Save file |
| `Ctrl+O` | Open file |
| `Ctrl+N` | New file |
| `Ctrl+/` | Toggle comment |
| `Tab` | Accept autocomplete |
| `Escape` | Dismiss autocomplete |

---

## Project Structure

```
PyLearn/
├── python_learner.py    # Main application
├── python_learner.pyw   # Full app (no console window)
├── icon.ico             # Application icon
└── README.md            # This file
```

---

## Author

**Kotan123** — [GitHub](https://github.com/kotan123)

---

## License

MIT License. Free to use, modify, and distribute.

---

**Made with PyQt6 • By Kotan123**
