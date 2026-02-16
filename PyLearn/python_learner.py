"""
PyLearn v1.0 — Interactive Python Learning App
Advanced code editor with autocomplete, file operations, and 20 lessons.
"""

import sys, subprocess, re, math, os, random, time, io, threading, shutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QPlainTextEdit, QScrollArea,
    QStackedWidget, QFrame, QGraphicsDropShadowEffect, QSplitter,
    QGraphicsOpacityEffect, QSizePolicy, QCompleter, QFileDialog,
    QLineEdit, QStatusBar, QTabBar, QTextBrowser
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QTimer, QSize,
    QParallelAnimationGroup, QPoint, QRect, QSequentialAnimationGroup,
    pyqtProperty, QStringListModel, QEvent, QUrl, pyqtSignal
)
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QSyntaxHighlighter, QTextCharFormat,
    QPainter, QLinearGradient, QPen, QIcon, QBrush, QRadialGradient,
    QTextCursor, QKeySequence, QShortcut, QAction, QTextBlockFormat
)


# ─── Resource path (PyInstaller compatible) ──────────────────────────────────

def resource_path(rel):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


_FROZEN = getattr(sys, 'frozen', False)


def _find_python():
    """Find a system Python interpreter (for running saved files as subprocess)."""
    if not _FROZEN:
        return sys.executable
    # Try common names
    for name in ("python", "python3", "py"):
        path = shutil.which(name)
        if path:
            return path
    return None


# ─── Theme ───────────────────────────────────────────────────────────────────

THEMES = {
    "Midnight": {
        "bg": "#0d1117", "bg2": "#161b22", "bg3": "#1c2333",
        "accent": "#e94560", "accent2": "#7c3aed",
        "blue": "#58a6ff", "green": "#2cb67d", "orange": "#ff8906",
        "text": "#e6edf3", "dim": "#8b949e", "border": "#30363d",
    },
    "Ocean": {
        "bg": "#0a192f", "bg2": "#112240", "bg3": "#1d3557",
        "accent": "#64ffda", "accent2": "#00b4d8",
        "blue": "#58a6ff", "green": "#64ffda", "orange": "#ffd166",
        "text": "#ccd6f6", "dim": "#8892b0", "border": "#233554",
    },
    "Sunset": {
        "bg": "#1a1a2e", "bg2": "#16213e", "bg3": "#0f3460",
        "accent": "#e94560", "accent2": "#f38181",
        "blue": "#a8dadc", "green": "#06d6a0", "orange": "#ffd166",
        "text": "#edf2f4", "dim": "#8d99ae", "border": "#2a2a4a",
    },
    "Forest": {
        "bg": "#1b2d1b", "bg2": "#243524", "bg3": "#2d4a2d",
        "accent": "#4ade80", "accent2": "#22c55e",
        "blue": "#67e8f9", "green": "#4ade80", "orange": "#fbbf24",
        "text": "#e2e8f0", "dim": "#94a3b8", "border": "#3a5a3a",
    },
}

T = THEMES["Midnight"]


def set_theme(name):
    global T
    T = THEMES[name]


# ─── Autocomplete word lists ────────────────────────────────────────────────

PY_KEYWORDS = [
    "and","as","assert","async","await","break","class","continue","def","del",
    "elif","else","except","finally","for","from","global","if","import","in",
    "is","lambda","nonlocal","not","or","pass","raise","return","try","while",
    "with","yield","True","False","None","match","case",
]
PY_BUILTINS = [
    "print","input","len","range","int","str","float","list","dict","tuple",
    "set","bool","type","isinstance","issubclass","enumerate","zip","map",
    "filter","sorted","reversed","open","super","abs","max","min","sum",
    "round","any","all","hex","bin","oct","ord","chr","format","hasattr",
    "getattr","setattr","delattr","property","staticmethod","classmethod",
    "vars","dir","id","repr","hash","callable","iter","next","slice",
    "frozenset","bytearray","bytes","memoryview","complex","divmod","pow",
    "exec","eval","compile","globals","locals","breakpoint","object",
    "NotImplemented","Ellipsis","__import__","__name__","__file__",
    "__doc__","__all__","__dict__","__class__","__slots__",
]
PY_EXCEPTIONS = [
    "Exception","BaseException","ArithmeticError","AssertionError",
    "AttributeError","BlockingIOError","BrokenPipeError","BufferError",
    "BytesWarning","ChildProcessError","ConnectionAbortedError",
    "ConnectionError","ConnectionRefusedError","ConnectionResetError",
    "DeprecationWarning","EOFError","EnvironmentError","FileExistsError",
    "FileNotFoundError","FloatingPointError","FutureWarning","GeneratorExit",
    "IOError","ImportError","ImportWarning","IndentationError","IndexError",
    "InterruptedError","IsADirectoryError","KeyError","KeyboardInterrupt",
    "LookupError","MemoryError","ModuleNotFoundError","NameError",
    "NotADirectoryError","NotImplementedError","OSError","OverflowError",
    "PendingDeprecationWarning","PermissionError","ProcessLookupError",
    "RecursionError","ReferenceError","ResourceWarning","RuntimeError",
    "RuntimeWarning","StopAsyncIteration","StopIteration","SyntaxError",
    "SyntaxWarning","SystemError","SystemExit","TabError","TimeoutError",
    "TypeError","UnboundLocalError","UnicodeDecodeError","UnicodeEncodeError",
    "UnicodeError","UnicodeTranslateError","UnicodeWarning","UserWarning",
    "ValueError","Warning","ZeroDivisionError",
]
PY_DUNDERS = [
    "__init__","__new__","__del__","__repr__","__str__","__format__",
    "__bytes__","__hash__","__bool__","__len__","__length_hint__",
    "__getitem__","__setitem__","__delitem__","__missing__","__iter__",
    "__next__","__reversed__","__contains__","__add__","__radd__",
    "__iadd__","__sub__","__rsub__","__isub__","__mul__","__rmul__",
    "__imul__","__truediv__","__rtruediv__","__floordiv__","__mod__",
    "__pow__","__and__","__or__","__xor__","__lshift__","__rshift__",
    "__neg__","__pos__","__abs__","__invert__","__int__","__float__",
    "__complex__","__index__","__round__","__enter__","__exit__",
    "__call__","__eq__","__ne__","__lt__","__le__","__gt__","__ge__",
    "__getattr__","__getattribute__","__setattr__","__delattr__",
    "__get__","__set__","__delete__","__init_subclass__",
    "__class_getitem__","__aenter__","__aexit__","__aiter__","__anext__",
    "__await__","__set_name__","__slots__","__dict__","__doc__",
    "__module__","__qualname__","__weakref__","__all__","__annotations__",
]
PY_STR_METHODS = [
    "capitalize","casefold","center","count","encode","endswith",
    "expandtabs","find","format","format_map","index","isalnum",
    "isalpha","isascii","isdecimal","isdigit","isidentifier","islower",
    "isnumeric","isprintable","isspace","istitle","isupper","join",
    "ljust","lower","lstrip","maketrans","partition","removeprefix",
    "removesuffix","replace","rfind","rindex","rjust","rpartition",
    "rsplit","rstrip","split","splitlines","startswith","strip",
    "swapcase","title","translate","upper","zfill",
]
PY_LIST_METHODS = [
    "append","clear","copy","count","extend","index","insert",
    "pop","remove","reverse","sort",
]
PY_DICT_METHODS = [
    "clear","copy","fromkeys","get","items","keys","pop",
    "popitem","setdefault","update","values",
]
PY_SET_METHODS = [
    "add","clear","copy","difference","difference_update","discard",
    "intersection","intersection_update","isdisjoint","issubset",
    "issuperset","pop","remove","symmetric_difference",
    "symmetric_difference_update","union","update",
]
PY_FILE_METHODS = [
    "close","closed","fileno","flush","isatty","read","readable",
    "readline","readlines","seek","seekable","tell","truncate",
    "writable","write","writelines",
]
PY_STDLIB_MODULES = [
    "os","sys","math","random","time","datetime","json","re","io",
    "pathlib","collections","itertools","functools","operator",
    "string","textwrap","unicodedata","struct","codecs","pprint",
    "reprlib","enum","numbers","decimal","fractions","statistics",
    "array","bisect","heapq","copy","types","typing","dataclasses",
    "abc","contextlib","atexit","traceback","warnings","logging",
    "unittest","doctest","argparse","shutil","glob","fnmatch",
    "tempfile","csv","configparser","tomllib","hashlib","hmac",
    "secrets","os.path","subprocess","socket","http","http.server",
    "urllib","urllib.request","urllib.parse","email","html",
    "xml","sqlite3","zipfile","tarfile","gzip","bz2","lzma",
    "pickle","shelve","marshal","threading","multiprocessing",
    "concurrent","concurrent.futures","asyncio","queue","sched",
    "signal","select","selectors","tkinter","turtle",
]
PY_COMMON_ATTRS = [
    "self","cls","args","kwargs","result","data","value","key",
    "index","name","path","file","line","text","msg","error",
    "count","size","length","width","height","start","end","step",
    "parent","child","children","root","node","left","right",
    "head","tail","prev","curr","temp","item","obj","func",
    "callback","handler","listener","event","response","request",
    "config","settings","options","params","headers","body",
    "status","code","message","output","url","port","host",
]
# Snippets: shown as-is, user picks and Tab inserts
PY_SNIPPETS = {
    "def func():": "def func():\n    pass",
    "def __init__(self):": "def __init__(self):\n    pass",
    "class MyClass:": "class MyClass:\n    def __init__(self):\n        pass",
    "if __name__ == \"__main__\":": "if __name__ == \"__main__\":\n    main()",
    "for i in range():": "for i in range():\n    pass",
    "while True:": "while True:\n    break",
    "with open() as f:": "with open(\"file.txt\", \"r\") as f:\n    data = f.read()",
    "try/except": "try:\n    pass\nexcept Exception as e:\n    print(e)",
    "lambda x:": "lambda x: x",
    "list comprehension": "[x for x in range()]",
    "dict comprehension": "{k: v for k, v in items}",
    "set comprehension": "{x for x in range()}",
    "@property": "@property\ndef name(self):\n    return self._name",
    "@staticmethod": "@staticmethod\ndef method():\n    pass",
    "@classmethod": "@classmethod\ndef method(cls):\n    pass",
    "async def":  "async def func():\n    await asyncio.sleep(1)",
    "dataclass": "from dataclasses import dataclass\n\n@dataclass\nclass MyClass:\n    name: str\n    value: int = 0",
    "enumerate()": "for i, item in enumerate(items):\n    print(i, item)",
    "zip()": "for a, b in zip(list1, list2):\n    print(a, b)",
    "map()": "result = list(map(func, iterable))",
    "filter()": "result = list(filter(func, iterable))",
    "sorted(key=)": "sorted(items, key=lambda x: x)",
    "defaultdict": "from collections import defaultdict\ndd = defaultdict(list)",
    "Counter": "from collections import Counter\nc = Counter(items)",
    "namedtuple": "from collections import namedtuple\nPoint = namedtuple('Point', ['x', 'y'])",
    "Path": "from pathlib import Path\np = Path('.')",
    "json.dumps()": "import json\ndata = json.dumps(obj, indent=2)",
    "json.loads()": "import json\nobj = json.loads(text)",
    "datetime.now()": "from datetime import datetime\nnow = datetime.now()",
    "argparse": "import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument('name')\nargs = parser.parse_args()",
    "logging.basicConfig": "import logging\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)",
    "unittest.TestCase": "import unittest\n\nclass TestMyClass(unittest.TestCase):\n    def test_example(self):\n        self.assertEqual(1, 1)",
}

_ALL_WORDS = sorted(set(
    PY_KEYWORDS + PY_BUILTINS + PY_EXCEPTIONS + PY_DUNDERS +
    PY_STR_METHODS + PY_LIST_METHODS + PY_DICT_METHODS +
    PY_SET_METHODS + PY_FILE_METHODS + PY_STDLIB_MODULES +
    PY_COMMON_ATTRS + list(PY_SNIPPETS.keys())
))


# ─── Floating Particles Background ──────────────────────────────────────────

class ParticleWidget(QWidget):
    """Floating dots background — purely cosmetic."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.particles = []
        for _ in range(12):
            self.particles.append({
                "x": random.random(), "y": random.random(),
                "r": random.uniform(1.5, 3), "dx": random.uniform(-0.0003, 0.0003),
                "dy": random.uniform(-0.0004, -0.0001), "a": random.randint(10, 30)
            })
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(33)

    def _tick(self):
        for p in self.particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            if p["y"] < -0.05:
                p["y"] = 1.05
                p["x"] = random.random()
            if p["x"] < -0.05 or p["x"] > 1.05:
                p["dx"] *= -1
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        ac = QColor(T["accent"])
        for p in self.particles:
            ac2 = QColor(ac)
            ac2.setAlpha(p["a"])
            painter.setBrush(QBrush(ac2))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(p["x"] * w), int(p["y"] * h),
                                int(p["r"] * 2), int(p["r"] * 2))
        painter.end()


# ─── Animated Slide Stack ────────────────────────────────────────────────────

class SlideStack(QStackedWidget):
    """QStackedWidget with smooth fade/slide animation (no glitches)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animating = False

    def slide_to(self, idx):
        if idx == self.currentIndex() or self._animating:
            return
        self._animating = True
        self.setCurrentIndex(idx)
        self._animating = False


# ─── Syntax Highlighter ─────────────────────────────────────────────────────

class PythonHL(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []
        kw = QTextCharFormat(); kw.setForeground(QColor("#c678dd")); kw.setFontWeight(QFont.Weight.Bold)
        for w in PY_KEYWORDS:
            self.rules.append((re.compile(rf"\b{w}\b"), kw))
        bf = QTextCharFormat(); bf.setForeground(QColor("#61afef"))
        for w in ["print","input","len","range","int","str","float","list","dict","tuple",
                   "set","bool","type","isinstance","enumerate","zip","map","filter","sorted",
                   "reversed","open","super","abs","max","min","sum","round","any","all","hex",
                   "bin","oct","ord","chr","format","hasattr","getattr","setattr","property"]:
            self.rules.append((re.compile(rf"\b{w}\b"), bf))
        sf = QTextCharFormat(); sf.setForeground(QColor("#98c379"))
        self.rules.append((re.compile(r'"""[\s\S]*?"""'), sf))
        self.rules.append((re.compile(r"'''[\s\S]*?'''"), sf))
        self.rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), sf))
        self.rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), sf))
        nf = QTextCharFormat(); nf.setForeground(QColor("#d19a66"))
        self.rules.append((re.compile(r"\b\d+\.?\d*\b"), nf))
        cf = QTextCharFormat(); cf.setForeground(QColor("#5c6370")); cf.setFontItalic(True)
        self.rules.append((re.compile(r"#[^\n]*"), cf))
        dc = QTextCharFormat(); dc.setForeground(QColor("#e5c07b"))
        self.rules.append((re.compile(r"@\w+"), dc))
        se = QTextCharFormat(); se.setForeground(QColor("#e06c75")); se.setFontItalic(True)
        self.rules.append((re.compile(r"\bself\b"), se))
        fn = QTextCharFormat(); fn.setForeground(QColor("#61afef"))
        self.rules.append((re.compile(r"(?<=\bdef\s)\w+"), fn))
        self.rules.append((re.compile(r"(?<=\bclass\s)\w+"), fn))

    def highlightBlock(self, text):
        for pat, fmt in self.rules:
            for m in pat.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


# ─── Code Editor with Line Numbers + Autocomplete ───────────────────────────

class LineNumArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    def sizeHint(self):
        return QSize(self.editor.ln_width(), 0)
    def paintEvent(self, e):
        self.editor.paint_ln(e)

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.ln = LineNumArea(self)
        self.blockCountChanged.connect(self._update_w)
        self.updateRequest.connect(self._update_area)
        self.cursorPositionChanged.connect(self._highlight_current_line)
        self.cursorPositionChanged.connect(self._highlight_brackets)
        self._update_w(0)
        self.setFont(QFont("Consolas", 12))
        self.setTabStopDistance(32)
        self.hl = PythonHL(self.document())
        self._bracket_selections = []

        # Autocomplete — IntelliJ-style
        self._completer = QCompleter(_ALL_WORDS, self)
        self._completer.setWidget(self)
        self._completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self._completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
        self._completer.setMaxVisibleItems(8)
        self._completer.activated.connect(self._insert_completion)
        self._completer_model = QStringListModel(_ALL_WORDS, self)
        self._completer.setModel(self._completer_model)
        # Delay timer — don't pop up instantly
        self._ac_timer = QTimer(self)
        self._ac_timer.setSingleShot(True)
        self._ac_timer.setInterval(250)
        self._ac_timer.timeout.connect(self._try_complete)

    def _update_completions(self):
        """Update word list with identifiers from current code."""
        code = self.toPlainText()
        user_words = set(re.findall(r'\b[a-zA-Z_]\w{2,}\b', code))
        all_words = sorted(set(_ALL_WORDS) | user_words)
        self._completer_model.setStringList(all_words)

    def apply_theme(self):
        self.setStyleSheet(f"""QPlainTextEdit{{
            background:{T['bg2']};color:{T['text']};border:1px solid {T['border']};
            border-radius:8px;padding:8px;selection-background-color:#264f78;}}""")
        popup = self._completer.popup()
        popup.setStyleSheet(f"""QListView{{
            background:{T['bg2']};color:{T['text']};
            border:1px solid {T['accent']};border-radius:6px;
            padding:3px;font-family:Consolas;font-size:11px;
            outline:none;}}
            QListView::item{{padding:3px 8px;border-radius:3px;}}
            QListView::item:selected{{background:{T['accent']};color:white;}}
            QListView::item:hover{{background:{T['bg3']};}}
            QScrollBar:vertical{{background:{T['bg2']};width:6px;}}
            QScrollBar::handle:vertical{{background:{T['bg3']};border-radius:3px;min-height:20px;}}
            QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}""")
        self._highlight_current_line()

    def _highlight_current_line(self):
        selections = list(self._bracket_selections)
        sel = QTextEdit.ExtraSelection()
        sel.format.setBackground(QColor(T.get("bg3", "#1c2333")))
        sel.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
        sel.cursor = self.textCursor()
        sel.cursor.clearSelection()
        selections.insert(0, sel)
        self.setExtraSelections(selections)

    def _highlight_brackets(self):
        """Highlight matching bracket pairs."""
        self._bracket_selections = []
        cursor = self.textCursor()
        text = self.toPlainText()
        pos = cursor.position()
        if pos <= 0 or pos > len(text):
            return
        ch = text[pos - 1] if pos > 0 else ''
        pairs = {'(': ')', '[': ']', '{': '}'}
        rpairs = {')': '(', ']': '[', '}': '{'}
        match_pos = -1
        if ch in pairs:
            # Search forward
            target = pairs[ch]
            depth = 0
            for i in range(pos, len(text)):
                if text[i] == ch: depth += 1
                elif text[i] == target:
                    depth -= 1
                    if depth == 0:
                        match_pos = i
                        break
        elif ch in rpairs:
            # Search backward
            target = rpairs[ch]
            depth = 0
            for i in range(pos - 2, -1, -1):
                if text[i] == ch: depth += 1
                elif text[i] == target:
                    depth -= 1
                    if depth == 0:
                        match_pos = i
                        break
        if match_pos >= 0:
            fmt = QTextCharFormat()
            fmt.setBackground(QColor(T["accent"]))
            fmt.setForeground(QColor("white"))
            for p in [pos - 1, match_pos]:
                sel = QTextEdit.ExtraSelection()
                sel.format = fmt
                c = self.textCursor()
                c.setPosition(p)
                c.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
                sel.cursor = c
                self._bracket_selections.append(sel)
        self._highlight_current_line()

    def keyPressEvent(self, e):
        popup = self._completer.popup()
        # ── When popup is visible ──
        if popup.isVisible():
            if e.key() == Qt.Key.Key_Tab:
                # Tab = accept top/selected completion
                idx = popup.currentIndex()
                if idx.isValid():
                    self._insert_completion(idx.data())
                elif self._completer.currentCompletion():
                    self._insert_completion(self._completer.currentCompletion())
                popup.hide()
                return
            elif e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                idx = popup.currentIndex()
                if idx.isValid():
                    self._insert_completion(idx.data())
                    popup.hide()
                    return
                popup.hide()
                # Fall through to auto-indent
            elif e.key() == Qt.Key.Key_Escape:
                popup.hide()
                return
            elif e.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down):
                # Let popup handle arrow keys
                popup.keyPressEvent(e)
                return
            elif e.key() in (Qt.Key.Key_Left, Qt.Key.Key_Right,
                             Qt.Key.Key_Home, Qt.Key.Key_End):
                popup.hide()

        # ── Ctrl+/ toggle comment ──
        if e.key() == Qt.Key.Key_Slash and e.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._toggle_comment()
            return

        # ── Auto-indent after colon ──
        if e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            line = cursor.block().text()
            indent = len(line) - len(line.lstrip())
            spaces = " " * indent
            if line.rstrip().endswith(":"):
                spaces += "    "
            super().keyPressEvent(e)
            self.insertPlainText(spaces)
            return

        # ── Tab as indent (when popup NOT visible) ──
        if e.key() == Qt.Key.Key_Tab and not popup.isVisible():
            cursor = self.textCursor()
            if cursor.hasSelection():
                # Indent selection
                start = cursor.selectionStart()
                end = cursor.selectionEnd()
                cursor.setPosition(start)
                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
                cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
                text = cursor.selectedText()
                lines = text.split('\u2029')
                cursor.insertText('\u2029'.join('    ' + l for l in lines))
            else:
                self.insertPlainText("    ")
            return

        super().keyPressEvent(e)

        # ── Trigger autocomplete with delay ──
        if e.text() and (e.text().isalpha() or e.text() == '_'):
            self._ac_timer.start()
        elif not e.text() or not (e.text().isalnum() or e.text() == '_'):
            self._ac_timer.stop()
            popup.hide()

    def _try_complete(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        prefix = cursor.selectedText()
        if len(prefix) < 2:
            self._completer.popup().hide()
            return
        self._update_completions()
        self._completer.setCompletionPrefix(prefix)
        cnt = self._completer.completionCount()
        if cnt == 0:
            self._completer.popup().hide()
            return
        if cnt == 1 and self._completer.currentCompletion() == prefix:
            self._completer.popup().hide()
            return
        cr = self.cursorRect()
        cr.setWidth(280)
        self._completer.complete(cr)
        # Auto-select first item
        popup = self._completer.popup()
        popup.setCurrentIndex(self._completer.completionModel().index(0, 0))

    def _insert_completion(self, completion):
        cursor = self.textCursor()
        # Check if it's a snippet
        if completion in PY_SNIPPETS:
            # Delete the whole current line and insert snippet
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            line_text = cursor.selectedText()
            indent = len(line_text) - len(line_text.lstrip())
            indent_str = " " * indent
            snippet = PY_SNIPPETS[completion]
            # Apply current indentation to each line of snippet
            lines = snippet.split("\n")
            indented = lines[0]
            for ln in lines[1:]:
                indented += "\n" + indent_str + ln
            cursor.insertText(indent_str + indented)
        else:
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            cursor.insertText(completion)
        self.setTextCursor(cursor)
        self._completer.popup().hide()

    def _toggle_comment(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
        text = cursor.selectedText()
        lines = text.split('\u2029')
        all_commented = all(l.lstrip().startswith('#') for l in lines if l.strip())
        if all_commented:
            new_lines = []
            for l in lines:
                idx = l.find('# ')
                if idx >= 0:
                    new_lines.append(l[:idx] + l[idx+2:])
                else:
                    idx = l.find('#')
                    if idx >= 0:
                        new_lines.append(l[:idx] + l[idx+1:])
                    else:
                        new_lines.append(l)
        else:
            new_lines = ['# ' + l if l.strip() else l for l in lines]
        cursor.insertText('\n'.join(new_lines))

    def ln_width(self):
        return 16 + self.fontMetrics().horizontalAdvance("9") * max(1, len(str(self.blockCount())))
    def _update_w(self, _): self.setViewportMargins(self.ln_width(), 0, 0, 0)
    def _update_area(self, rect, dy):
        if dy: self.ln.scroll(0, dy)
        else: self.ln.update(0, rect.y(), self.ln.width(), rect.height())
        if rect.contains(self.viewport().rect()): self._update_w(0)
    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        self.ln.setGeometry(cr.left(), cr.top(), self.ln_width(), cr.height())
    def paint_ln(self, event):
        p = QPainter(self.ln)
        p.fillRect(event.rect(), QColor(T["bg3"]))
        b = self.firstVisibleBlock(); n = b.blockNumber()
        top = round(self.blockBoundingGeometry(b).translated(self.contentOffset()).top())
        bot = top + round(self.blockBoundingRect(b).height())
        cur_block = self.textCursor().blockNumber()
        while b.isValid() and top <= event.rect().bottom():
            if b.isVisible() and bot >= event.rect().top():
                color = T["text"] if n == cur_block else T["dim"]
                p.setPen(QColor(color)); p.setFont(QFont("Consolas", 9))
                p.drawText(0, top, self.ln.width()-6, self.fontMetrics().height(),
                           Qt.AlignmentFlag.AlignRight, str(n+1))
            b = b.next(); top = bot
            bot = top + round(self.blockBoundingRect(b).height()); n += 1
        p.end()


# ─── Animated Lesson Card ───────────────────────────────────────────────────

class LessonCard(QFrame):
    def __init__(self, number, title, desc):
        super().__init__()
        self.setFixedHeight(76)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.num = number

        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 8, 14, 8)
        lay.setSpacing(12)

        self.badge = QLabel(str(number).zfill(2))
        self.badge.setFixedSize(38, 38)
        self.badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.badge.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        lay.addWidget(self.badge)

        tb = QVBoxLayout(); tb.setSpacing(1)
        self.title_lbl = QLabel(title)
        self.title_lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        tb.addWidget(self.title_lbl)
        self.desc_lbl = QLabel(desc)
        self.desc_lbl.setFont(QFont("Segoe UI", 9))
        tb.addWidget(self.desc_lbl)
        lay.addLayout(tb, 1)

        self.arrow = QLabel("\u276f")
        self.arrow.setFont(QFont("Segoe UI", 13))
        lay.addWidget(self.arrow)

        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setBlurRadius(0)
        self._shadow.setOffset(0, 0)
        self.setGraphicsEffect(self._shadow)
        self._anims = []

    def apply_theme(self):
        self._shadow.setColor(QColor(T["accent"]))
        self.badge.setStyleSheet(f"""background:qlineargradient(x1:0,y1:0,x2:1,y2:1,
            stop:0 {T['accent']},stop:1 {T['accent2']});color:white;border-radius:19px;""")
        self.title_lbl.setStyleSheet(f"color:{T['text']};background:transparent;")
        self.desc_lbl.setStyleSheet(f"color:{T['dim']};background:transparent;")
        self.arrow.setStyleSheet(f"color:{T['dim']};background:transparent;")
        self._set_base()

    def _set_base(self):
        self.setStyleSheet(f"LessonCard{{background:{T['bg2']};border:1px solid {T['border']};border-radius:10px;}}")

    def _set_hover(self):
        self.setStyleSheet(f"LessonCard{{background:{T['bg3']};border:1px solid {T['accent']};border-radius:10px;}}")

    def enterEvent(self, e):
        self._set_hover()
        self.arrow.setStyleSheet(f"color:{T['accent']};background:transparent;")
        a1 = QPropertyAnimation(self._shadow, b"blurRadius"); a1.setDuration(200)
        a1.setStartValue(0); a1.setEndValue(25); a1.setEasingCurve(QEasingCurve.Type.OutCubic)
        a2 = QPropertyAnimation(self._shadow, b"color"); a2.setDuration(200)
        ac = QColor(T["accent"]); ac.setAlpha(0)
        ac2 = QColor(T["accent"]); ac2.setAlpha(100)
        a2.setStartValue(ac); a2.setEndValue(ac2)
        g = QParallelAnimationGroup(self); g.addAnimation(a1); g.addAnimation(a2); g.start()
        self._anims = [g]; super().enterEvent(e)

    def leaveEvent(self, e):
        self._set_base()
        self.arrow.setStyleSheet(f"color:{T['dim']};background:transparent;")
        a1 = QPropertyAnimation(self._shadow, b"blurRadius"); a1.setDuration(250)
        a1.setStartValue(25); a1.setEndValue(0)
        a2 = QPropertyAnimation(self._shadow, b"color"); a2.setDuration(250)
        ac = QColor(T["accent"]); ac.setAlpha(100)
        ac2 = QColor(T["accent"]); ac2.setAlpha(0)
        a2.setStartValue(ac); a2.setEndValue(ac2)
        g = QParallelAnimationGroup(self); g.addAnimation(a1); g.addAnimation(a2); g.start()
        self._anims = [g]; super().leaveEvent(e)


# ─── Pulsing Glow Button ────────────────────────────────────────────────────

class GlowButton(QPushButton):
    """Button with a pulsing glow shadow."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._glow = QGraphicsDropShadowEffect()
        self._glow.setOffset(0, 0)
        self._glow.setBlurRadius(0)
        self._glow.setColor(QColor(T["green"]))
        self.setGraphicsEffect(self._glow)
        self._pulse_anim = None

    def start_pulse(self):
        if self._pulse_anim:
            return
        self._glow.setColor(QColor(T["green"]))
        seq = QSequentialAnimationGroup(self)
        a_in = QPropertyAnimation(self._glow, b"blurRadius")
        a_in.setDuration(1200); a_in.setStartValue(0); a_in.setEndValue(18)
        a_in.setEasingCurve(QEasingCurve.Type.InOutSine)
        a_out = QPropertyAnimation(self._glow, b"blurRadius")
        a_out.setDuration(1200); a_out.setStartValue(18); a_out.setEndValue(0)
        a_out.setEasingCurve(QEasingCurve.Type.InOutSine)
        seq.addAnimation(a_in); seq.addAnimation(a_out)
        seq.setLoopCount(-1); seq.start()
        self._pulse_anim = seq

    def stop_pulse(self):
        if self._pulse_anim:
            self._pulse_anim.stop()
            self._pulse_anim = None
            self._glow.setBlurRadius(0)

    def update_glow_color(self):
        self._glow.setColor(QColor(T["green"]))


# ─── 20 Lessons ──────────────────────────────────────────────────────────────

LESSONS = [
  {"title":"Variables & Data Types","desc":"Store and use data",
   "content":"<h2 style='color:{ac}'>Variables & Data Types</h2><p>Variables store data. Python creates them on assignment.</p><h3 style='color:{bl}'>Types</h3><ul><li><b>int</b> — <code>42</code></li><li><b>float</b> — <code>3.14</code></li><li><b>str</b> — <code>\"hello\"</code></li><li><b>bool</b> — <code>True/False</code></li></ul><h3 style='color:{bl}'>Type Checking</h3><p><code>type(x)</code>, <code>isinstance(x, int)</code></p>",
   "code":'# Variables\nname = "Alice"\nage = 25\npi = 3.14\nis_active = True\n\nprint(f"Name: {name}, Age: {age}")\nprint(f"Pi: {pi}, Active: {is_active}")\nprint(f"\\nTypes:")\nfor v in [name, age, pi, is_active]:\n    print(f"  {v!r:>10} -> {type(v).__name__}")'},

  {"title":"Strings","desc":"Text manipulation mastery",
   "content":"<h2 style='color:{ac}'>Strings</h2><p>Text sequences with powerful methods.</p><h3 style='color:{bl}'>Operations</h3><ul><li>Concatenation: <code>\"a\" + \"b\"</code></li><li>Repetition: <code>\"ha\" * 3</code></li><li>Slicing: <code>s[1:4]</code></li></ul><h3 style='color:{bl}'>f-Strings</h3><p><code>f\"Value: {{x}}\"</code></p><h3 style='color:{bl}'>Methods</h3><p><code>.upper() .lower() .strip() .split() .replace() .find() .startswith()</code></p>",
   "code":"# Strings\nmsg = \"Hello, Python World!\"\nprint(msg.upper())\nprint(msg.replace(\"World\", \"Learner\"))\nprint(f\"Slice [7:13]: {msg[7:13]}\")\n\n# f-strings\nname, score = \"Alex\", 95\nresult = \"Pass\" if score >= 60 else \"Fail\"\nprint(f\"\\n{name} got {score}% - {result}\")\n\n# Methods\ncsv = \"  apple, banana, cherry  \"\nprint(f\"\\nStripped: '{csv.strip()}'\")\nprint(f\"Split: {csv.strip().split(', ')}\")"},

  {"title":"Numbers & Math","desc":"Arithmetic and math operations",
   "content":"<h2 style='color:{ac}'>Numbers & Math</h2><h3 style='color:{bl}'>Operators</h3><ul><li><code>+ - * /</code> basic</li><li><code>//</code> floor div, <code>%</code> modulo</li><li><code>**</code> power</li></ul><h3 style='color:{bl}'>Built-in Functions</h3><p><code>abs() round() min() max() sum() divmod()</code></p><h3 style='color:{bl}'>math module</h3><p><code>math.sqrt() math.pi math.ceil() math.floor()</code></p>",
   "code":'# Numbers & Math\nimport math\n\nprint(f"17 / 5  = {17/5}")\nprint(f"17 // 5 = {17//5}")\nprint(f"17 % 5  = {17%5}")\nprint(f"2 ** 10 = {2**10}")\n\nprint(f"\\npi = {math.pi:.6f}")\nprint(f"sqrt(144) = {math.sqrt(144)}")\nprint(f"ceil(4.2) = {math.ceil(4.2)}")\n\nnums = [3, 7, 1, 9, 4]\nprint(f"\\nsum={sum(nums)} min={min(nums)} max={max(nums)}")'},

  {"title":"Lists","desc":"Ordered mutable collections",
   "content":"<h2 style='color:{ac}'>Lists</h2><p>Ordered, mutable sequences.</p><h3 style='color:{bl}'>Methods</h3><ul><li><code>.append() .insert() .remove() .pop()</code></li><li><code>.sort() .reverse() .index() .count()</code></li></ul><h3 style='color:{bl}'>Comprehensions</h3><p><code>[expr for x in iterable if cond]</code></p>",
   "code":'# Lists\nfruits = ["apple", "banana", "cherry"]\nfruits.append("orange")\nfruits.insert(1, "mango")\nprint(f"Fruits: {fruits}")\nprint(f"Popped: {fruits.pop()}")\n\n# Comprehensions\nsquares = [x**2 for x in range(1, 8)]\nprint(f"\\nSquares: {squares}")\n\nevens = [x for x in range(20) if x % 2 == 0]\nprint(f"Evens: {evens}")\n\n# Nested\nmatrix = [[1,2,3],[4,5,6],[7,8,9]]\nflat = [n for row in matrix for n in row]\nprint(f"\\nFlattened: {flat}")'},

  {"title":"Tuples & Sets","desc":"Immutable sequences and unique collections",
   "content":"<h2 style='color:{ac}'>Tuples & Sets</h2><h3 style='color:{bl}'>Tuples</h3><p>Immutable sequences. Unpacking: <code>a, b = (1, 2)</code></p><h3 style='color:{bl}'>Sets</h3><p>Unordered unique elements. <code>| & - ^</code> for union, intersection, difference, symmetric diff.</p>",
   "code":'# Tuples\npoint = (3, 7)\nx, y = point\nprint(f"Point: x={x}, y={y}")\n\ncolors = ("red", "green", "blue")\nprint(f"Colors: {colors}, len={len(colors)}")\n\n# Sets\na = {1, 2, 3, 4, 5}\nb = {4, 5, 6, 7, 8}\nprint(f"\\nUnion: {a | b}")\nprint(f"Intersection: {a & b}")\nprint(f"Difference: {a - b}")\nprint(f"Symmetric: {a ^ b}")\n\nwords = ["hello", "world", "hello", "python", "world"]\nprint(f"\\nUnique: {set(words)}")'},

  {"title":"Conditionals","desc":"if / elif / else branching",
   "content":"<h2 style='color:{ac}'>Conditionals</h2><h3 style='color:{bl}'>if / elif / else</h3><p>Branch based on conditions.</p><h3 style='color:{bl}'>Operators</h3><ul><li><code>== != < > <= >=</code></li><li><code>and or not</code></li><li><code>in</code> membership</li></ul><h3 style='color:{bl}'>Ternary</h3><p><code>x if cond else y</code></p>",
   "code":'# Conditionals\nage = 18\n\nif age >= 21:\n    print("Full access")\nelif age >= 18:\n    print("Limited access")\nelif age >= 13:\n    print("Teen mode")\nelse:\n    print("Denied")\n\n# Ternary\nstatus = "adult" if age >= 18 else "minor"\nprint(f"Status: {status}")\n\n# Match (Python 3.10+)\nhttp_code = 404\nmatch http_code:\n    case 200: msg = "OK"\n    case 404: msg = "Not Found"\n    case 500: msg = "Server Error"\n    case _: msg = "Unknown"\nprint(f"\\n{http_code}: {msg}")'},

  {"title":"Loops","desc":"for, while, and control flow",
   "content":"<h2 style='color:{ac}'>Loops</h2><h3 style='color:{bl}'>for</h3><p><code>for x in iterable:</code></p><h3 style='color:{bl}'>while</h3><p><code>while condition:</code></p><h3 style='color:{bl}'>Control</h3><ul><li><code>break</code> — exit</li><li><code>continue</code> — skip</li><li><code>else</code> — runs if no break</li></ul>",
   "code":'# Loops\nfor lang in ["Python", "Rust", "Go", "JS"]:\n    print(f"  Love {lang}!")\n\nprint("\\n--- Multiplication ---")\nfor i in range(1, 6):\n    print(f"  {i} x 7 = {i*7}")\n\n# Enumerate\nprint("\\n--- Enumerate ---")\nfor i, ch in enumerate("PYTHON"):\n    print(f"  [{i}] = {ch}")\n\n# While + break\nprint("\\n--- Countdown ---")\nn = 5\nwhile n > 0:\n    print(n, end=" ")\n    n -= 1\nprint("Launch!")'},

  {"title":"Functions","desc":"Define reusable code blocks",
   "content":"<h2 style='color:{ac}'>Functions</h2><h3 style='color:{bl}'>Syntax</h3><p><code>def name(params): return result</code></p><h3 style='color:{bl}'>Features</h3><ul><li>Default params: <code>def f(x=10)</code></li><li><code>*args</code>, <code>**kwargs</code></li><li>Type hints: <code>def f(x: int) -> str</code></li></ul><h3 style='color:{bl}'>Lambda</h3><p><code>lambda x: x * 2</code></p>",
   "code":'# Functions\ndef greet(name, greeting="Hello"):\n    return f"{greeting}, {name}!"\n\nprint(greet("Alice"))\nprint(greet("Bob", "Hey"))\n\n# Multiple returns\ndef stats(numbers):\n    return min(numbers), max(numbers), sum(numbers)/len(numbers)\n\nlo, hi, avg = stats([4, 7, 1, 9, 3])\nprint(f"\\nMin={lo} Max={hi} Avg={avg:.1f}")\n\n# Lambda + map\nnums = [1, 2, 3, 4, 5]\ncubed = list(map(lambda x: x**3, nums))\nprint(f"\\nCubed: {cubed}")\n\n# *args\ndef total(*args):\n    return sum(args)\nprint(f"Total: {total(10, 20, 30)}")'},

  {"title":"Dictionaries","desc":"Key-value pair storage",
   "content":"<h2 style='color:{ac}'>Dictionaries</h2><p>Fast key-value lookups.</p><h3 style='color:{bl}'>Methods</h3><ul><li><code>.get(key, default)</code></li><li><code>.keys() .values() .items()</code></li><li><code>.update() .pop() .setdefault()</code></li></ul><h3 style='color:{bl}'>Comprehension</h3><p><code>{{k: v for k, v in items}}</code></p>",
   "code":"# Dictionaries\nstudent = {'name': 'Alice', 'age': 20, 'grades': [90, 85, 92]}\nprint(f\"Name: {student['name']}\")\nprint(f\"GPA: {sum(student['grades'])/len(student['grades']):.1f}\")\n\n# Safe access\nemail = student.get('email', 'N/A')\nprint(f\"Email: {email}\")\n\n# Iteration\nprint('\\n--- Entries ---')\nfor k, v in student.items():\n    print(f'  {k}: {v}')\n\n# Comprehension\nsq = {n: n**2 for n in range(1, 6)}\nprint(f'\\nSquares: {sq}')"},

  {"title":"File I/O","desc":"Read and write files",
   "content":"<h2 style='color:{ac}'>File I/O</h2><h3 style='color:{bl}'>with statement</h3><p><code>with open(path, mode) as f:</code></p><h3 style='color:{bl}'>Modes</h3><ul><li><code>'r'</code> read, <code>'w'</code> write, <code>'a'</code> append</li><li><code>'rb'/'wb'</code> binary</li></ul><h3 style='color:{bl}'>Methods</h3><p><code>.read() .readline() .readlines() .write() .writelines()</code></p>",
   "code":'# File I/O\nimport tempfile, os\npath = os.path.join(tempfile.gettempdir(), "pylearn.txt")\n\nwith open(path, "w") as f:\n    f.write("Hello File I/O!\\n")\n    f.write("Line 2\\n")\n    f.write("Line 3\\n")\n\nwith open(path) as f:\n    for i, line in enumerate(f, 1):\n        print(f"  Line {i}: {line.strip()}")\n\nwith open(path, "a") as f:\n    f.write("Appended!\\n")\n\nprint(f"\\nFull content:")\nprint(open(path).read())\nos.remove(path)\nprint("Cleaned up!")'},

  {"title":"Error Handling","desc":"try / except / finally",
   "content":"<h2 style='color:{ac}'>Error Handling</h2><h3 style='color:{bl}'>Structure</h3><pre>try:\n    ...\nexcept ErrorType as e:\n    ...\nelse:\n    # no error\nfinally:\n    # always runs</pre><h3 style='color:{bl}'>Common</h3><p><code>ValueError TypeError KeyError IndexError ZeroDivisionError FileNotFoundError</code></p>",
   "code":'# Error Handling\ndef safe_div(a, b):\n    try:\n        result = a / b\n    except ZeroDivisionError:\n        return "Cannot divide by zero!"\n    except TypeError as e:\n        return f"Type error: {e}"\n    else:\n        return f"{a}/{b} = {result:.2f}"\n    finally:\n        pass  # cleanup here\n\nprint(safe_div(10, 3))\nprint(safe_div(10, 0))\nprint(safe_div("a", 3))\n\n# Custom exception\nclass AgeError(Exception): pass\n\ntry:\n    raise AgeError("Age must be 0-150")\nexcept AgeError as e:\n    print(f"\\nCaught: {e}")'},

  {"title":"OOP Basics","desc":"Classes, objects, inheritance",
   "content":"<h2 style='color:{ac}'>OOP Basics</h2><h3 style='color:{bl}'>Class</h3><p><code>class Name: def __init__(self): ...</code></p><h3 style='color:{bl}'>Key Concepts</h3><ul><li><code>__init__</code> constructor</li><li><code>self</code> — instance ref</li><li>Inheritance: <code>class B(A)</code></li></ul><h3 style='color:{bl}'>Special Methods</h3><p><code>__str__ __repr__ __len__ __eq__</code></p>",
   "code":'# OOP\nclass Animal:\n    def __init__(self, name, sound):\n        self.name = name\n        self.sound = sound\n    def speak(self):\n        return f"{self.name} says {self.sound}!"\n    def __str__(self):\n        return f"Animal({self.name})"\n\nclass Dog(Animal):\n    def __init__(self, name, breed):\n        super().__init__(name, "Woof")\n        self.breed = breed\n    def fetch(self, item):\n        return f"{self.name} fetches the {item}!"\n\nbuddy = Dog("Buddy", "Golden")\nprint(buddy.speak())\nprint(buddy.fetch("ball"))\nprint(f"Is Animal? {isinstance(buddy, Animal)}")'},

  {"title":"List Comprehensions","desc":"Powerful one-liner list creation",
   "content":"<h2 style='color:{ac}'>List Comprehensions</h2><p>Concise way to create lists.</p><h3 style='color:{bl}'>Syntax</h3><p><code>[expr for x in iter if cond]</code></p><h3 style='color:{bl}'>Nested</h3><p><code>[expr for x in A for y in B]</code></p><h3 style='color:{bl}'>Dict/Set</h3><p><code>{{k:v for ...}}</code> and <code>{{x for ...}}</code></p>",
   "code":'# Comprehensions\n\n# Basic\nsquares = [x**2 for x in range(10)]\nprint(f"Squares: {squares}")\n\n# With filter\nevens = [x for x in range(20) if x % 2 == 0]\nprint(f"Evens: {evens}")\n\n# Nested\nmatrix = [[1,2,3],[4,5,6],[7,8,9]]\nflat = [n for row in matrix for n in row]\nprint(f"Flat: {flat}")\n\n# Dict comprehension\nword = "abracadabra"\nfreq = {ch: word.count(ch) for ch in set(word)}\nprint(f"\\nFrequency: {freq}")\n\n# Set comprehension\nfirst_letters = {w[0] for w in ["apple","avocado","banana","blueberry"]}\nprint(f"First letters: {first_letters}")'},

  {"title":"Modules & Imports","desc":"Organize and reuse code",
   "content":"<h2 style='color:{ac}'>Modules & Imports</h2><h3 style='color:{bl}'>Import Styles</h3><ul><li><code>import math</code></li><li><code>from math import sqrt</code></li><li><code>from math import *</code></li><li><code>import math as m</code></li></ul><h3 style='color:{bl}'>Useful Stdlib</h3><p><code>os sys json datetime random collections itertools</code></p>",
   "code":'# Modules\nimport random\nimport datetime\nimport json\nfrom collections import Counter\n\n# Random\nnums = [random.randint(1, 10) for _ in range(15)]\nprint(f"Random: {nums}")\n\n# Counter\ncounts = Counter(nums)\nprint(f"Counts: {dict(counts)}")\nprint(f"Most common: {counts.most_common(3)}")\n\n# DateTime\nnow = datetime.datetime.now()\nfmt = now.strftime("%Y-%m-%d %H:%M")\nprint(f"\\nNow: {fmt}")\n\n# JSON\ndata = {"name": "Alice", "scores": [95, 87, 92]}\nj = json.dumps(data, indent=2)\nprint(f"\\nJSON:\\n{j}")'},

  {"title":"String Formatting","desc":"f-strings, format(), and more",
   "content":"<h2 style='color:{ac}'>String Formatting</h2><h3 style='color:{bl}'>f-Strings</h3><p><code>f\"text {{expr}}\"</code> — most modern</p><h3 style='color:{bl}'>Format Spec</h3><ul><li><code>:.2f</code> — 2 decimal places</li><li><code>:>10</code> — right align, width 10</li><li><code>:,</code> — thousand separator</li><li><code>:#x</code> — hex</li></ul>",
   "code":'# String Formatting\npi = 3.14159265\nprint(f"Pi: {pi:.2f}")       # 2 decimals\nprint(f"Pi: {pi:.6f}")       # 6 decimals\n\nbig = 1234567890\nprint(f"\\nFormatted: {big:,}")  # commas\nprint(f"Hex: {255:#x}")       # 0xff\nprint(f"Binary: {42:#b}")     # 0b101010\n\n# Alignment\nfor item, price in [("Apple", 1.5), ("Banana", 0.75), ("Cherry", 3.0)]:\n    print(f"  {item:<10} ${price:>6.2f}")\n\n# Debug with =\nx, y = 42, "hello"\nprint(f"\\n{x = }")\nprint(f"{y = }")'},

  {"title":"Decorators","desc":"Modify function behavior",
   "content":"<h2 style='color:{ac}'>Decorators</h2><p>Functions that wrap other functions.</p><h3 style='color:{bl}'>Syntax</h3><pre>@decorator\ndef func(): ...</pre><h3 style='color:{bl}'>Use Cases</h3><ul><li>Timing, logging, caching</li><li>Access control, validation</li></ul>",
   "code":'# Decorators\nimport time\n\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        start = time.perf_counter()\n        result = func(*args, **kwargs)\n        elapsed = time.perf_counter() - start\n        print(f"  {func.__name__} took {elapsed:.4f}s")\n        return result\n    return wrapper\n\n@timer\ndef slow_sum(n):\n    return sum(range(n))\n\n@timer\ndef fast_sum(n):\n    return n * (n - 1) // 2\n\nprint("Slow:", slow_sum(1_000_000))\nprint("Fast:", fast_sum(1_000_000))\n\n# Decorator with args\ndef repeat(n):\n    def decorator(func):\n        def wrapper(*a, **k):\n            for _ in range(n):\n                func(*a, **k)\n        return wrapper\n    return decorator\n\n@repeat(3)\ndef say_hi():\n    print("Hi!")\n\nprint("\\n--- Repeat ---")\nsay_hi()'},

  {"title":"Generators","desc":"Lazy evaluation with yield",
   "content":"<h2 style='color:{ac}'>Generators</h2><p>Functions that yield values one at a time — memory efficient.</p><h3 style='color:{bl}'>yield</h3><p><code>def gen(): yield value</code></p><h3 style='color:{bl}'>Generator Expressions</h3><p><code>(x**2 for x in range(10))</code></p><h3 style='color:{bl}'>Use Cases</h3><p>Large data streams, infinite sequences, pipelines</p>",
   "code":'# Generators\ndef fibonacci(limit):\n    a, b = 0, 1\n    while a < limit:\n        yield a\n        a, b = b, a + b\n\nfibs = list(fibonacci(100))\nprint(f"Fibonacci: {fibs}")\n\n# Generator expression\nsq_gen = (x**2 for x in range(10))\nprint(f"\\nSquares: {list(sq_gen)}")\n\n# Infinite generator\ndef count_up(start=0):\n    n = start\n    while True:\n        yield n\n        n += 1\n\ncounter = count_up(10)\nfirst_5 = [next(counter) for _ in range(5)]\nprint(f"\\nCount from 10: {first_5}")\n\n# Pipeline\ndef evens(nums):\n    for n in nums:\n        if n % 2 == 0: yield n\n\ndef doubled(nums):\n    for n in nums: yield n * 2\n\nresult = list(doubled(evens(range(10))))\nprint(f"Pipeline: {result}")'},

  {"title":"Context Managers","desc":"with statement and resource management",
   "content":"<h2 style='color:{ac}'>Context Managers</h2><p>Automatic setup and cleanup with <code>with</code>.</p><h3 style='color:{bl}'>Custom</h3><p>Use <code>__enter__</code> and <code>__exit__</code>, or <code>@contextmanager</code></p>",
   "code":'# Context Managers\nfrom contextlib import contextmanager\nimport time\n\n@contextmanager\ndef timer(label):\n    start = time.perf_counter()\n    print(f"[{label}] Starting...")\n    yield\n    elapsed = time.perf_counter() - start\n    print(f"[{label}] Done in {elapsed:.4f}s")\n\nwith timer("Computation"):\n    total = sum(range(1_000_000))\n    print(f"  Sum = {total:,}")\n\n# Class-based\nclass Indenter:\n    def __init__(self):\n        self.level = 0\n    def __enter__(self):\n        self.level += 1\n        return self\n    def __exit__(self, *args):\n        self.level -= 1\n    def print(self, text):\n        print("  " * self.level + text)\n\nwith Indenter() as indent:\n    indent.print("Level 1")\n    with indent:\n        indent.print("Level 2")\n        with indent:\n            indent.print("Level 3")\n    indent.print("Back to 1")'},

  {"title":"Regular Expressions","desc":"Pattern matching in strings",
   "content":"<h2 style='color:{ac}'>Regular Expressions</h2><h3 style='color:{bl}'>Functions</h3><ul><li><code>re.search()</code> — find first match</li><li><code>re.findall()</code> — find all</li><li><code>re.sub()</code> — replace</li><li><code>re.split()</code> — split by pattern</li></ul>",
   "code":'# Regex\nimport re\n\ntext = "Call me at 555-1234 or 555-5678. Email: test@mail.com"\n\n# Find phone numbers\nphones = re.findall(r"\\d{3}-\\d{4}", text)\nprint(f"Phones: {phones}")\n\n# Find email\nemail = re.search(r"[\\w.]+@[\\w.]+", text)\nprint(f"Email: {email.group()}")\n\n# Replace\ncensored = re.sub(r"\\d{3}-\\d{4}", "XXX-XXXX", text)\nprint(f"\\nCensored: {censored}")\n\n# Validate\ndef is_valid_email(s):\n    return bool(re.match(r"^[\\w.]+@[\\w]+\\.[a-z]{2,}$", s))\n\nfor e in ["user@site.com", "bad@", "ok@x.org"]:\n    print(f"  {e:>15} -> valid={is_valid_email(e)}")'},

  {"title":"Data Structures","desc":"Advanced built-in structures",
   "content":"<h2 style='color:{ac}'>Data Structures</h2><h3 style='color:{bl}'>collections module</h3><ul><li><code>Counter</code> — count elements</li><li><code>defaultdict</code> — dict with defaults</li><li><code>deque</code> — double-ended queue</li><li><code>namedtuple</code> — tuple with names</li></ul>",
   "code":'# Data Structures\nfrom collections import Counter, defaultdict, deque, namedtuple\n\n# Counter\nwords = "the cat sat on the mat the cat".split()\nc = Counter(words)\nprint(f"Word counts: {dict(c)}")\nprint(f"Top 2: {c.most_common(2)}")\n\n# defaultdict\ngraph = defaultdict(list)\nfor a, b in [(1,2),(1,3),(2,4),(3,4)]:\n    graph[a].append(b)\nprint(f"\\nGraph: {dict(graph)}")\n\n# deque\ndq = deque([1, 2, 3], maxlen=5)\ndq.appendleft(0)\ndq.append(4)\nprint(f"\\nDeque: {list(dq)}")\n\n# namedtuple\nPoint = namedtuple("Point", ["x", "y"])\np = Point(3, 7)\nprint(f"\\nPoint: {p}, x={p.x}, y={p.y}")'},
]


# ─── Lessons List Page ───────────────────────────────────────────────────────

class LessonsPage(QWidget):
    def __init__(self, on_click):
        super().__init__()
        self.on_click = on_click
        self.cards = []
        self._entrance_played = False

        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)

        self.header = QLabel("  📚 Lessons")
        self.header.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.header.setFixedHeight(50)
        self.layout_.addWidget(self.header)

        self.sub = QLabel(f"  {len(LESSONS)} topics — select one to learn  •  By Kotan123")
        self.sub.setFont(QFont("Segoe UI", 10))
        self.layout_.addWidget(self.sub)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setObjectName("lessonScroll")

        self.container = QWidget()
        self.container.setObjectName("lessonContainer")
        self.clayout = QVBoxLayout(self.container)
        self.clayout.setContentsMargins(10, 4, 10, 14)
        self.clayout.setSpacing(5)

        for i, lesson in enumerate(LESSONS):
            card = LessonCard(i + 1, lesson["title"], lesson["desc"])
            card.mousePressEvent = lambda e, idx=i: self.on_click(idx)
            self.clayout.addWidget(card)
            self.cards.append(card)

        self.clayout.addStretch()
        self.scroll.setWidget(self.container)
        self.layout_.addWidget(self.scroll)

    def apply_theme(self):
        bg = T['bg']
        bgc = QColor(bg)
        self.header.setStyleSheet(f"color:{T['text']};padding:14px 0 2px 10px;background:{bg};")
        self.sub.setStyleSheet(f"color:{T['dim']};padding:0 0 6px 10px;background:{bg};font-style:italic;")
        # Scrollbar styling + force scroll background
        self.scroll.setStyleSheet(f"""
            QScrollArea#lessonScroll{{border:none;background:{bg};}}
            QScrollBar:vertical{{background:{bg};width:8px;margin:0;border:none;}}
            QScrollBar::handle:vertical{{background:{T['bg3']};border-radius:4px;min-height:30px;}}
            QScrollBar::handle:vertical:hover{{background:{T['dim']};}}
            QScrollBar::add-line:vertical{{height:0;border:none;background:none;}}
            QScrollBar::sub-line:vertical{{height:0;border:none;background:none;}}
            QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{{background:{bg};}}""")
        # Force bg via palette on every level
        for w in [self, self.scroll, self.scroll.viewport(), self.container]:
            w.setAutoFillBackground(True)
            p = w.palette()
            for role in (QPalette.ColorRole.Window, QPalette.ColorRole.Base,
                         QPalette.ColorRole.AlternateBase):
                p.setColor(role, bgc)
            w.setPalette(p)
        for card in self.cards:
            card.apply_theme()

    def play_entrance(self):
        """Staggered slide-in animation for lesson cards."""
        self._entrance_anims = []
        for i, card in enumerate(self.cards):
            card.setGraphicsEffect(card._shadow)   # keep existing shadow
            # Slide from right
            start_pos = QPoint(card.x() + 60, card.y())
            end_pos = QPoint(card.x(), card.y())
            a = QPropertyAnimation(card, b"pos")
            a.setDuration(350)
            a.setStartValue(start_pos)
            a.setEndValue(end_pos)
            a.setEasingCurve(QEasingCurve.Type.OutCubic)
            QTimer.singleShot(i * 40, a.start)
            self._entrance_anims.append(a)


# ─── Lesson Detail Page ──────────────────────────────────────────────────────

class LessonDetailPage(QWidget):
    def __init__(self, on_back, on_try):
        super().__init__()
        self.on_back = on_back
        self.on_try = on_try
        self._idx = 0
        self._typing_timer = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        top = QHBoxLayout()
        top.setContentsMargins(10, 8, 10, 0)

        self.back_btn = QPushButton("\u2190  Back")
        self.back_btn.setFont(QFont("Segoe UI", 11))
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.clicked.connect(on_back)
        top.addWidget(self.back_btn)

        self.lesson_title = QLabel("")
        self.lesson_title.setFont(QFont("Consolas", 13, QFont.Weight.Bold))
        top.addWidget(self.lesson_title, 1)

        self.try_btn = QPushButton("\u25b6  Try in Editor")
        self.try_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.try_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.try_btn.clicked.connect(lambda: self.on_try(LESSONS[self._idx]["code"]))
        top.addWidget(self.try_btn)
        lay.addLayout(top)

        self.content = QTextEdit()
        self.content.setReadOnly(True)
        self.content.setFont(QFont("Segoe UI", 11))
        lay.addWidget(self.content)

    def apply_theme(self):
        bg = T['bg']
        self.back_btn.setStyleSheet(f"""QPushButton{{background:transparent;color:{T['accent']};border:none;padding:8px 12px;}}
            QPushButton:hover{{color:{T['text']};}}""")
        self.try_btn.setStyleSheet(f"""QPushButton{{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,
            stop:0 {T['accent']},stop:1 {T['accent2']});color:white;border:none;border-radius:8px;padding:10px 18px;}}
            QPushButton:hover{{background:{T['accent2']};}}""")
        bgc = QColor(bg)
        self.content.setStyleSheet(f"""QTextEdit{{background:{bg};color:{T['text']};border:none;padding:14px;}}
            QScrollBar:vertical{{background:{bg};width:8px;margin:0;border:none;}}
            QScrollBar::handle:vertical{{background:{T['bg3']};border-radius:4px;min-height:30px;}}
            QScrollBar::handle:vertical:hover{{background:{T['dim']};}}
            QScrollBar::add-line:vertical{{height:0;border:none;background:none;}}
            QScrollBar::sub-line:vertical{{height:0;border:none;background:none;}}
            QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{{background:{bg};}}""")
        for widget in [self.content.viewport(), self.content]:
            widget.setAutoFillBackground(True)
            pal = widget.palette()
            pal.setColor(QPalette.ColorRole.Window, bgc)
            pal.setColor(QPalette.ColorRole.Base, bgc)
            widget.setPalette(pal)
        self.lesson_title.setStyleSheet(f"color:{T['accent']};background:transparent;padding-left:8px;")

    def set_lesson(self, idx):
        self._idx = idx
        lesson = LESSONS[idx]
        self._type_title(lesson["title"])
        html_content = lesson["content"].format(ac=T["accent"], bl=T["blue"])
        self.content.setHtml(f"""
        <div style='font-family:Segoe UI;color:{T["text"]};line-height:1.7;'>
            {html_content}
            <br><h3 style='color:{T["blue"]}'>Example Code:</h3>
            <pre style='background:{T["bg"]};padding:12px;border-radius:8px;
                font-family:Consolas;font-size:12px;color:{T["text"]};
                border:1px solid {T["border"]};line-height:1.4;'>{lesson["code"]}</pre>
        </div>""")

    def _type_title(self, text):
        if self._typing_timer:
            self._typing_timer.stop()
        self._typed = ""
        self._full_title = text
        self._char_idx = 0
        self._typing_timer = QTimer(self)
        self._typing_timer.timeout.connect(self._type_next)
        self._typing_timer.start(40)

    def _type_next(self):
        if self._char_idx < len(self._full_title):
            self._typed += self._full_title[self._char_idx]
            self.lesson_title.setText(self._typed + "\u258c")
            self._char_idx += 1
        else:
            self.lesson_title.setText(self._full_title)
            self._typing_timer.stop()


# ─── Editor Page (Advanced IDE) ─────────────────────────────────────────────

class EditorPage(QWidget):
    def __init__(self, status_callback=None):
        super().__init__()
        self._status_cb = status_callback
        self._tabs = []          # list of {file: path|None, code: str}
        self._active_tab = -1
        self._new_counter = 0
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # ── Toolbar row ──
        toolbar = QWidget()
        toolbar.setFixedHeight(42)
        bar = QHBoxLayout(toolbar)
        bar.setContentsMargins(12, 0, 12, 0)
        bar.setSpacing(8)

        self.title_lbl = QLabel("Code Editor")
        self.title_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        bar.addWidget(self.title_lbl)

        bar.addStretch()

        # File buttons — equal spacing
        self._file_btns = []
        for label, slot in [("New", "_file_new"), ("Open", "_file_open"),
                            ("Save", "_file_save"), ("Save As", "_file_save_as"),
                            ("Clear", "_clear")]:
            btn = QPushButton(label)
            btn.setFont(QFont("Segoe UI", 9))
            btn.setFixedHeight(28)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(getattr(self, slot))
            bar.addWidget(btn)
            self._file_btns.append(btn)
            setattr(self, f"btn_{label.lower().replace(' ','_')}", btn)

        bar.addSpacing(6)

        self.run_btn = GlowButton("\u25b6 Run")
        self.run_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.run_btn.setFixedHeight(28)
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self._run_code)
        bar.addWidget(self.run_btn)
        lay.addWidget(toolbar)

        # Accent gradient bar
        self._accent_bar = QFrame()
        self._accent_bar.setFixedHeight(2)
        lay.addWidget(self._accent_bar)

        # ── Tab bar ──
        self.tab_bar = QTabBar()
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setFont(QFont("Consolas", 9))
        self.tab_bar.currentChanged.connect(self._on_tab_changed)
        self.tab_bar.tabCloseRequested.connect(self._close_tab)
        lay.addWidget(self.tab_bar)

        # ── Splitter: editor + console ──
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.editor = CodeEditor()
        self.editor.setPlaceholderText("# Write Python code here...\n# Ctrl+Enter = run, Ctrl+S = save, Ctrl+N = new tab\n")
        self.editor.cursorPositionChanged.connect(self._update_status)
        self.splitter.addWidget(self.editor)

        # Console
        console_box = QWidget()
        cl = QVBoxLayout(console_box)
        cl.setContentsMargins(12, 4, 12, 4)
        cl.setSpacing(2)

        console_header = QHBoxLayout()
        self.out_lbl = QLabel("Console")
        self.out_lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        console_header.addWidget(self.out_lbl)
        console_header.addStretch()

        self.time_lbl = QLabel("")
        self.time_lbl.setFont(QFont("Consolas", 9))
        console_header.addWidget(self.time_lbl)

        self.clear_console_btn = QPushButton("Clear")
        self.clear_console_btn.setFont(QFont("Segoe UI", 8))
        self.clear_console_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_console_btn.clicked.connect(lambda: self.output.clear())
        console_header.addWidget(self.clear_console_btn)
        cl.addLayout(console_header)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 11))
        self.output.setPlaceholderText("Output appears here...")
        cl.addWidget(self.output)

        self.splitter.addWidget(console_box)
        self.splitter.setSizes([400, 200])
        lay.addWidget(self.splitter)

        # Progress bar
        self.progress = QFrame()
        self.progress.setFixedHeight(3)
        self.progress.setStyleSheet("background:transparent;")
        lay.addWidget(self.progress)
        self._prog_anim = None

        # Create first tab
        self._new_counter += 1
        self._add_tab(f"untitled-{self._new_counter}", None, "")

    # ── Tab management ──

    def _add_tab(self, name, filepath, code):
        """Add a new tab and switch to it."""
        self._save_current_tab()
        idx = self.tab_bar.addTab(name)
        self._tabs.append({"file": filepath, "code": code})
        self.tab_bar.setCurrentIndex(idx)

    def _save_current_tab(self):
        """Save editor content into current tab's data."""
        if 0 <= self._active_tab < len(self._tabs):
            self._tabs[self._active_tab]["code"] = self.editor.toPlainText()

    def _on_tab_changed(self, idx):
        if idx < 0 or idx >= len(self._tabs):
            return
        if self._active_tab >= 0 and self._active_tab < len(self._tabs):
            self._tabs[self._active_tab]["code"] = self.editor.toPlainText()
        self._active_tab = idx
        tab = self._tabs[idx]
        self.editor.setPlainText(tab["code"])
        self.output.clear()
        self._update_status()

    def _close_tab(self, idx):
        if len(self._tabs) <= 1:
            # Don't close last tab, just clear it
            self._tabs[0] = {"file": None, "code": ""}
            self.tab_bar.setTabText(0, "untitled")
            self.editor.clear()
            self.output.clear()
            return
        self._tabs.pop(idx)
        self.tab_bar.removeTab(idx)
        # _active_tab will be updated by currentChanged signal

    def _current_file(self):
        if 0 <= self._active_tab < len(self._tabs):
            return self._tabs[self._active_tab]["file"]
        return None

    def _set_current_file(self, path):
        if 0 <= self._active_tab < len(self._tabs):
            self._tabs[self._active_tab]["file"] = path

    def _update_tab_title(self):
        if 0 <= self._active_tab < len(self._tabs):
            f = self._tabs[self._active_tab]["file"]
            name = os.path.basename(f) if f else "untitled"
            self.tab_bar.setTabText(self._active_tab, name)

    # ── Theme ──

    def apply_theme(self):
        self.title_lbl.setStyleSheet(f"color:{T['text']};background:transparent;")
        self._accent_bar.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"stop:0 {T['accent']},stop:0.5 {T['accent2']},stop:1 {T['accent']});")
        file_btn_style = f"""QPushButton{{background:{T['bg2']};color:{T['dim']};
            border:1px solid {T['border']};border-radius:4px;padding:4px 12px;}}
            QPushButton:hover{{background:{T['bg3']};color:{T['text']};}}"""
        for btn in self._file_btns:
            btn.setStyleSheet(file_btn_style)
        self.clear_console_btn.setStyleSheet(f"""QPushButton{{background:transparent;color:{T['dim']};
            border:none;padding:2px 6px;font-size:8px;}}
            QPushButton:hover{{color:{T['text']};}}""")
        self._idle_style = f"""QPushButton{{background:{T['green']};color:white;border:none;
            border-radius:6px;padding:5px 14px;min-width:60px;}}
            QPushButton:hover{{background:#24a06b;}}"""
        self._active_style = f"""QPushButton{{background:{T['orange']};color:white;border:none;
            border-radius:6px;padding:5px 14px;min-width:60px;}}"""
        self.run_btn.setStyleSheet(self._idle_style)
        self.run_btn.update_glow_color()
        self.run_btn.start_pulse()
        # Tab bar style
        self.tab_bar.setStyleSheet(f"""
            QTabBar{{background:{T['bg']};border:none;}}
            QTabBar::tab{{
                background:{T['bg2']};color:{T['dim']};
                border:1px solid {T['border']};border-bottom:none;
                padding:5px 18px 5px 12px;margin-right:2px;
                border-top-left-radius:6px;border-top-right-radius:6px;
                min-width:80px;
            }}
            QTabBar::tab:selected{{
                background:{T['bg3']};color:{T['text']};
                border-bottom:2px solid {T['accent']};
            }}
            QTabBar::tab:hover{{background:{T['bg3']};color:{T['text']};}}
            QTabBar::close-button{{
                subcontrol-position:right;
                margin:2px;
                border-radius:3px;
                padding:1px;
            }}
            QTabBar::close-button:hover{{
                background:{T['accent']};
            }}""")
        self.editor.apply_theme()
        self.out_lbl.setStyleSheet(f"color:{T['dim']};background:transparent;")
        self.time_lbl.setStyleSheet(f"color:{T['dim']};background:transparent;")
        self.output.setStyleSheet(f"""QTextEdit{{background:{T['bg2']};color:{T['green']};
            border:1px solid {T['border']};border-radius:8px;padding:8px;}}
            QScrollBar:vertical{{background:{T['bg']};width:8px;border-radius:4px;}}
            QScrollBar::handle:vertical{{background:{T['bg3']};border-radius:4px;min-height:30px;}}
            QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}""")
        self.splitter.setStyleSheet(f"QSplitter::handle{{background:{T['border']};height:2px;}}")

    def _update_status(self):
        if self._status_cb:
            cursor = self.editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            f = self._current_file()
            name = os.path.basename(f) if f else "untitled"
            self._status_cb(f"  {name}    Ln {line}, Col {col}    {self.editor.blockCount()} lines")

    # ── File operations ──

    def _file_new(self):
        """Create a new tab (keeps existing tabs)."""
        self._save_current_tab()
        self._new_counter += 1
        self._add_tab(f"untitled-{self._new_counter}", None, "")
        self.editor.clear()
        self.output.clear()

    def _file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Python File", "",
            "Python Files (*.py *.pyw);;All Files (*)")
        if path:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                code = f.read()
            # Open in new tab
            self._save_current_tab()
            name = os.path.basename(path)
            self._add_tab(name, path, code)
            self.editor.setPlainText(code)
            self.output.clear()

    def _file_save(self):
        f = self._current_file()
        if f:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(self.editor.toPlainText())
            self.time_lbl.setText("Saved!")
            QTimer.singleShot(2000, lambda: self.time_lbl.setText(""))
        else:
            self._file_save_as()

    def _file_save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Python File", "",
            "Python Files (*.py);;All Files (*)")
        if path:
            self._set_current_file(path)
            self._update_tab_title()
            self._file_save()

    def set_code(self, code):
        """Load lesson code into a new tab."""
        self._save_current_tab()
        self._add_tab("lesson", None, code.strip())
        self.editor.setPlainText(code.strip())
        self.output.clear()

    def _clear(self):
        self.editor.clear()
        self.output.clear()

    def _run_code(self):
        code = self.editor.toPlainText()
        if not code.strip():
            c = T["orange"]
            self.output.setHtml(f"<span style='color:{c}'>No code to run.</span>")
            return
        self.run_btn.stop_pulse()
        self.run_btn.setStyleSheet(self._active_style)
        self.run_btn.setText("Running...")
        self.run_btn.setEnabled(False)
        self.progress.setStyleSheet(f"background:{T['accent']};")
        self.progress.setFixedWidth(0)
        a = QPropertyAnimation(self.progress, b"minimumWidth")
        a.setDuration(2000); a.setStartValue(0); a.setEndValue(self.width())
        a.setEasingCurve(QEasingCurve.Type.Linear); a.start()
        self._prog_anim = a
        c = T["dim"]
        self.output.setHtml(f"<span style='color:{c}'>Running...</span>")
        self._run_start = time.perf_counter()
        QTimer.singleShot(50, lambda: self._exec(code))

    def _exec(self, code):
        cg, ce, cd = T["green"], T["accent"], T["dim"]
        py = _find_python()
        cur_file = self._current_file()
        try:
            if py is None:
                self.output.setHtml(f"<span style='color:{ce}'>Python not found! Install Python and add to PATH.</span>")
                return
            if cur_file:
                r = subprocess.run([py, cur_file],
                    capture_output=True, text=True, timeout=15,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                    cwd=os.path.dirname(cur_file))
            else:
                r = subprocess.run([py, "-c", code],
                    capture_output=True, text=True, timeout=15,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            o, e = r.stdout, r.stderr
            if o and e:
                self.output.setHtml(f"<pre style='color:{cg}'>{self._e(o)}</pre><pre style='color:{ce}'>{self._e(e)}</pre>")
            elif o:
                self.output.setHtml(f"<pre style='color:{cg}'>{self._e(o)}</pre>")
            elif e:
                self.output.setHtml(f"<pre style='color:{ce}'>{self._e(e)}</pre>")
            else:
                self.output.setHtml(f"<span style='color:{cd}'>Done (no output).</span>")
        except subprocess.TimeoutExpired:
            self.output.setHtml(f"<span style='color:{ce}'>Timeout (15s).</span>")
        except Exception as ex:
            self.output.setHtml(f"<span style='color:{ce}'>Error: {self._e(str(ex))}</span>")
        finally:
            elapsed = time.perf_counter() - self._run_start
            self.time_lbl.setText(f"{elapsed:.3f}s")
            self.run_btn.setEnabled(True)
            self.run_btn.setText("\u25b6 Run")
            self.run_btn.setStyleSheet(self._idle_style)
            self.run_btn.start_pulse()
            if self._prog_anim:
                self._prog_anim.stop()
            self.progress.setFixedWidth(self.width())
            QTimer.singleShot(400, lambda: self.progress.setStyleSheet("background:transparent;"))

    def _e(self, t):
        return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")


# ─── AI Assistant Page (Pollinations AI — free, no key) ───────────────────────

_AI_URL = "https://text.pollinations.ai/"
_SYS_PROMPT = ("Your name is PyLearn AI. You are the built-in Python coding assistant of the PyLearn app, created by Kotan123. "
    "NEVER say you are ChatGPT, GPT, OpenAI, or any other AI. You are ONLY 'PyLearn AI'. "
    "If asked who you are, say: 'I am PyLearn AI, your Python coding assistant built into PyLearn by Kotan123.' "
    "IMPORTANT: You MUST reply in the SAME language the user writes in. "
    "If the user writes in Russian, reply in Russian. If in English, reply in English. "
    "When writing code, wrap it in ```python blocks. Be concise and helpful. Focus on Python. "
    "CRITICAL: The user has PyQt6 installed (NOT PyQt5). When writing any GUI code, "
    "ALWAYS use PyQt6 imports (from PyQt6.QtWidgets, from PyQt6.QtCore, from PyQt6.QtGui). "
    "NEVER use PyQt5. Also in PyQt6: exec() not exec_(), and enums use full path like Qt.AlignmentFlag.AlignCenter.")


class AiPage(QWidget):
    _sig_response = pyqtSignal(str)

    def __init__(self, insert_code_cb=None):
        super().__init__()
        self._insert_cb = insert_code_cb
        self._history = []       # [{role, text}]
        self._code_blocks = []   # collected during _render_chat
        self._busy = False
        self._sig_response.connect(self._on_response)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Header
        hbar = QHBoxLayout()
        hbar.setContentsMargins(14, 8, 14, 4)
        self._title = QLabel("🤖 AI Assistant")
        self._title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        hbar.addWidget(self._title)
        hbar.addStretch()
        self._clear_btn = QPushButton("Clear")
        self._clear_btn.setFont(QFont("Segoe UI", 9))
        self._clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._clear_btn.setToolTip("Clear chat")
        self._clear_btn.clicked.connect(self._clear_chat)
        hbar.addWidget(self._clear_btn)
        lay.addLayout(hbar)

        # Gradient accent bar
        self._accent_bar = QFrame()
        self._accent_bar.setFixedHeight(2)
        lay.addWidget(self._accent_bar)

        # Chat area
        self._chat = QTextBrowser()
        self._chat.setFont(QFont("Segoe UI", 11))
        self._chat.setOpenExternalLinks(False)
        self._chat.setOpenLinks(False)
        self._chat.anchorClicked.connect(self._on_link)
        lay.addWidget(self._chat, 1)

        # Input bar
        ibar = QHBoxLayout()
        ibar.setContentsMargins(10, 6, 10, 10)
        ibar.setSpacing(8)
        self._input = QLineEdit()
        self._input.setFont(QFont("Segoe UI", 11))
        self._input.setPlaceholderText("Ask AI to write Python code...")
        self._input.returnPressed.connect(self._send)
        ibar.addWidget(self._input, 1)
        self._send_btn = GlowButton("Send")
        self._send_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self._send_btn.setFixedHeight(34)
        self._send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._send_btn.clicked.connect(self._send)
        ibar.addWidget(self._send_btn)
        lay.addLayout(ibar)

    def apply_theme(self):
        self._title.setStyleSheet(f"color:{T['text']};background:transparent;")
        self._accent_bar.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"stop:0 {T['accent']},stop:0.5 {T['accent2']},stop:1 {T['accent']});")
        self._clear_btn.setStyleSheet(f"""QPushButton{{background:{T['bg2']};color:{T['dim']};border:none;
            border-radius:6px;padding:4px 10px;}}
            QPushButton:hover{{color:{T['text']};background:{T['bg3']};}}""")
        self._chat.setStyleSheet(f"""QTextBrowser{{background:{T['bg']};color:{T['text']};border:none;padding:10px;}}
            QScrollBar:vertical{{background:{T['bg']};width:8px;margin:0;border:none;}}
            QScrollBar::handle:vertical{{background:{T['bg3']};border-radius:4px;min-height:30px;}}
            QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{{background:{T['bg']};}}
            QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}""")
        self._input.setStyleSheet(f"""QLineEdit{{background:{T['bg2']};color:{T['text']};
            border:1px solid {T['border']};border-radius:8px;padding:8px 12px;}}
            QLineEdit:focus{{border:1px solid {T['accent']};}}""")
        self._send_btn.setStyleSheet(f"""QPushButton{{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,
            stop:0 {T['accent']},stop:1 {T['accent2']});color:white;border:none;
            border-radius:8px;padding:6px 18px;}}
            QPushButton:hover{{background:{T['accent2']};}}
            QPushButton:disabled{{background:{T['bg3']};color:{T['dim']};}}""")
        self._send_btn._glow.setColor(QColor(T["accent"]))
        self._send_btn.start_pulse()
        self._render_chat()

    def _clear_chat(self):
        self._history.clear()
        self._render_chat()

    def _send(self):
        msg = self._input.text().strip()
        if not msg or self._busy:
            return
        self._input.clear()
        self._input.setPlaceholderText("Thinking...")
        self._history.append({"role": "user", "text": msg})
        self._render_chat()
        self._busy = True
        self._send_btn.setEnabled(False)
        threading.Thread(target=self._call_api, args=(msg,), daemon=True).start()

    def _call_api(self, user_msg):
        import urllib.request, json as _json, ssl
        try:
            ctx = ssl.create_default_context()
            # Build messages array
            messages = [{"role": "system", "content": _SYS_PROMPT}]
            for h in self._history:
                if h["role"] == "user":
                    messages.append({"role": "user", "content": h["text"]})
                elif h["role"] == "ai":
                    messages.append({"role": "assistant", "content": h["text"]})
            body = _json.dumps({"model": "openai", "messages": messages}).encode("utf-8")
            req = urllib.request.Request(_AI_URL, data=body, headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            try:
                resp = urllib.request.urlopen(req, timeout=60, context=ctx)
            except Exception:
                # Fallback: skip SSL verification if certs missing (frozen .exe)
                ctx = ssl._create_unverified_context()
                resp = urllib.request.urlopen(req, timeout=60, context=ctx)
            with resp:
                text = resp.read().decode("utf-8")
            self._sig_response.emit(text)
        except Exception as ex:
            err = str(ex)
            self._sig_response.emit(f"Error: {err}")

    def _on_response(self, text):
        self._history.append({"role": "ai", "text": text})
        self._busy = False
        self._send_btn.setEnabled(True)
        self._input.setPlaceholderText("Ask AI to write Python code...")
        self._render_chat()

    def _append_system(self, text):
        self._history.append({"role": "system", "text": text})
        self._render_chat()

    def _render_chat(self):
        self._code_blocks = []
        html = ""
        if not self._history:
            html += (f"<div style='text-align:center;padding:40px 20px;'>"
                     f"<p style='color:{T['accent']};font-size:22px;font-weight:bold;'>🤖 AI Assistant</p>"
                     f"<p style='color:{T['dim']};font-size:12px;margin-top:6px;'>"
                     f"Ask me to write any Python code!</p>"
                     f"<p style='color:{T['border']};font-size:10px;margin-top:20px;'>"
                     f"Powered by PyLearn • By Kotan123</p></div>")
        for msg in self._history:
            if msg["role"] == "user":
                html += self._render_user(msg["text"])
            elif msg["role"] == "ai":
                html += self._render_ai(msg["text"])
            else:
                html += f"<p style='color:{T['dim']};font-style:italic;text-align:center;'>{self._e(msg['text'])}</p>"
        if self._busy:
            html += f"<p style='color:{T['accent']};'>\u23f3 Thinking...</p>"
        self._chat.setHtml(f"<div style='font-family:Segoe UI;font-size:11px;'>{html}</div>")
        sb = self._chat.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _render_user(self, text):
        return (f"<div style='text-align:right;margin:8px 0;'>"
                f"<span style='background:{T['accent']};color:white;padding:6px 12px;"
                f"border-radius:12px 12px 2px 12px;display:inline-block;'>"
                f"{self._e(text)}</span></div>")

    def _render_ai(self, text):
        parts = self._parse_response(text)
        html = f"<div style='margin:8px 0;'>"
        for kind, content in parts:
            if kind == "code":
                idx = len(self._code_blocks)
                self._code_blocks.append(content)
                esc = self._e(content)
                html += (f"<pre style='background:{T['bg2']};color:{T['green']};padding:10px;"
                         f"border-radius:8px;border:1px solid {T['border']};font-family:Consolas;"
                         f"font-size:11px;white-space:pre-wrap;'>{esc}</pre>")
                html += (f"<p><a href='#insert_{idx}' style='color:{T['accent']};font-size:10px;"
                         f"text-decoration:none;'>\u25b6 Insert to Editor</a></p>")
            else:
                t = self._e(content)
                t = re.sub(r'\*\*(.+?)\*\*', rf"<b>\1</b>", t)
                t = re.sub(r'`(.+?)`', rf"<code style='background:{T['bg2']};padding:1px 4px;"
                           f"border-radius:3px;font-family:Consolas;'>\1</code>", t)
                t = t.replace('\n', '<br>')
                html += f"<span style='color:{T['text']};'>{t}</span>"
        html += "</div>"
        return html

    def _parse_response(self, text):
        parts = []
        chunks = re.split(r'```(?:python)?\n?', text)
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            if i % 2 == 0:
                parts.append(("text", chunk.strip()))
            else:
                parts.append(("code", chunk.rstrip('`').strip()))
        return parts

    def _on_link(self, url):
        href = url.toString()
        if href.startswith("#insert_") and self._insert_cb:
            try:
                idx = int(href.split("_")[1])
                if 0 <= idx < len(self._code_blocks):
                    self._insert_cb(self._code_blocks[idx])
            except (ValueError, IndexError):
                pass

    def _e(self, t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ─── Sidebar ─────────────────────────────────────────────────────────────────

class Sidebar(QFrame):
    def __init__(self, on_nav, on_theme):
        super().__init__()
        self.setFixedWidth(200)
        self.on_nav = on_nav
        self.on_theme = on_theme

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        logo_box = QWidget()
        logo_box.setFixedHeight(64)
        logo_box.setStyleSheet("background:transparent;")
        ll = QVBoxLayout(logo_box)
        ll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo = QLabel("{ Py }")
        self.logo.setFont(QFont("Consolas", 22, QFont.Weight.Bold))
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._logo_shadow = QGraphicsDropShadowEffect()
        self._logo_shadow.setOffset(0, 0)
        self._logo_shadow.setBlurRadius(0)
        self.logo.setGraphicsEffect(self._logo_shadow)
        ll.addWidget(self.logo)
        self.logo_sub = QLabel("Learn Python • By Kotan123")
        self.logo_sub.setFont(QFont("Segoe UI", 8))
        self.logo_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ll.addWidget(self.logo_sub)
        lay.addWidget(logo_box)

        self.sep = QFrame()
        self.sep.setFixedHeight(1)
        lay.addWidget(self.sep)
        lay.addSpacing(6)

        self.nav_btns = []
        for text in ["📚 Lessons", "💻 Code Editor", "🤖 AI Assistant"]:
            btn = QPushButton(f"  {text}")
            btn.setFont(QFont("Segoe UI", 11))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(42)
            btn.clicked.connect(lambda ch, t=text: self._nav(t))
            lay.addWidget(btn)
            self.nav_btns.append((btn, text))

        lay.addSpacing(12)

        theme_label = QLabel("  Theme")
        theme_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        lay.addWidget(theme_label)
        self._theme_label = theme_label

        self.theme_btns = []
        for name in THEMES:
            btn = QPushButton(f"  {name}")
            btn.setFont(QFont("Segoe UI", 10))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(34)
            btn.clicked.connect(lambda ch, n=name: self.on_theme(n))
            lay.addWidget(btn)
            self.theme_btns.append((btn, name))

        lay.addStretch()

        self.foot = QLabel("v1.0 • By Kotan123")
        self.foot.setFont(QFont("Segoe UI", 8))
        self.foot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.foot)

        self.active_page = "📚 Lessons"
        self.active_theme = "Midnight"

    def apply_theme(self):
        self.setStyleSheet(f"Sidebar{{background:{T['bg2']};border-right:1px solid {T['border']};}}")
        self.logo.setStyleSheet(f"color:{T['accent']};background:transparent;")
        self._logo_shadow.setColor(QColor(T["accent"]))
        self.logo_sub.setStyleSheet(f"color:{T['dim']};background:transparent;")
        self.sep.setStyleSheet(f"background:{T['border']};")
        self._theme_label.setStyleSheet(f"color:{T['dim']};padding-left:8px;background:transparent;")
        self.foot.setStyleSheet(f"color:{T['dim']};padding:10px;background:transparent;")
        for btn, text in self.nav_btns:
            btn.setStyleSheet(self._nav_style(text == self.active_page))
        for btn, name in self.theme_btns:
            btn.setStyleSheet(self._theme_style(name == self.active_theme))

    def _nav_style(self, active):
        if active:
            return f"""QPushButton{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {T['accent']},stop:1 {T['accent2']});color:white;border:none;
                border-radius:8px;text-align:left;padding-left:12px;margin:2px 8px;}}"""
        return f"""QPushButton{{background:transparent;color:{T['dim']};border:none;
            border-radius:8px;text-align:left;padding-left:12px;margin:2px 8px;}}
            QPushButton:hover{{background:{T['bg3']};color:{T['text']};
            border-left:3px solid {T['accent']};}}"""

    def _theme_style(self, active):
        if active:
            return f"""QPushButton{{background:{T['bg3']};color:{T['text']};border:none;
                border-radius:6px;text-align:left;padding-left:12px;margin:1px 8px;
                border-left:3px solid {T['accent']};}}"""
        return f"""QPushButton{{background:transparent;color:{T['dim']};border:none;
            border-radius:6px;text-align:left;padding-left:12px;margin:1px 8px;}}
            QPushButton:hover{{background:{T['bg3']};color:{T['text']};}}"""

    def set_active(self, name):
        self.active_page = name
        for btn, text in self.nav_btns:
            btn.setStyleSheet(self._nav_style(text == name))

    def set_active_theme(self, name):
        self.active_theme = name

    def _nav(self, name):
        self.set_active(name)
        self.on_nav(name)

    def _pulse_logo(self):
        seq = QSequentialAnimationGroup(self)
        a_in = QPropertyAnimation(self._logo_shadow, b"blurRadius")
        a_in.setDuration(800); a_in.setStartValue(0); a_in.setEndValue(25)
        a_in.setEasingCurve(QEasingCurve.Type.InOutSine)
        a_out = QPropertyAnimation(self._logo_shadow, b"blurRadius")
        a_out.setDuration(800); a_out.setStartValue(25); a_out.setEndValue(0)
        a_out.setEasingCurve(QEasingCurve.Type.InOutSine)
        seq.addAnimation(a_in); seq.addAnimation(a_out)
        seq.setLoopCount(-1); seq.start()
        self._logo_pulse = seq


# ─── Main Window ─────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyLearn — By Kotan123")
        self.resize(1000, 680)
        self.setMinimumSize(750, 500)
        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Status bar
        self.status = QStatusBar()
        self.status.setFont(QFont("Consolas", 9))
        self.setStatusBar(self.status)
        self._status_lbl = QLabel("  PyLearn • By Kotan123")
        self.status.addWidget(self._status_lbl)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        ml = QHBoxLayout(self.central)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        self.sidebar = Sidebar(self._navigate, self._change_theme)
        ml.addWidget(self.sidebar)

        content_area = QWidget()
        cl = QVBoxLayout(content_area)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        self.stack = SlideStack()
        cl.addWidget(self.stack)
        ml.addWidget(content_area, 1)

        self.particles = ParticleWidget(content_area)
        self.particles.lower()

        self.lessons_page = LessonsPage(self._open_lesson)
        self.detail_page = LessonDetailPage(self._back, self._try_code)
        self.editor_page = EditorPage(self._set_status)
        self.ai_page = AiPage(self._insert_ai_code)

        self.stack.addWidget(self.lessons_page)   # 0
        self.stack.addWidget(self.detail_page)    # 1
        self.stack.addWidget(self.editor_page)    # 2
        self.stack.addWidget(self.ai_page)        # 3

        # Shortcuts
        QShortcut(QKeySequence("Ctrl+Return"), self, self.editor_page._run_code)
        QShortcut(QKeySequence("Ctrl+S"), self, self.editor_page._file_save)
        QShortcut(QKeySequence("Ctrl+O"), self, self.editor_page._file_open)
        QShortcut(QKeySequence("Ctrl+N"), self, self.editor_page._file_new)

        self._apply_all_themes()
        QTimer.singleShot(50, self._startup)

    def _set_status(self, text):
        self._status_lbl.setText(text)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'particles'):
            ca = self.central
            self.particles.setGeometry(self.sidebar.width(), 0,
                ca.width() - self.sidebar.width(), ca.height())

    def _apply_all_themes(self):
        self.central.setStyleSheet(f"background:{T['bg']};")
        self.stack.setStyleSheet(f"background:{T['bg']};")
        self.status.setStyleSheet(f"QStatusBar{{background:{T['bg2']};color:{T['dim']};border-top:1px solid {T['border']};}}")
        self._status_lbl.setStyleSheet(f"color:{T['dim']};")
        self.sidebar.apply_theme()
        self.lessons_page.apply_theme()
        self.detail_page.apply_theme()
        self.editor_page.apply_theme()
        self.ai_page.apply_theme()

    def _startup(self):
        self.sidebar._pulse_logo()
        QTimer.singleShot(200, self.lessons_page.play_entrance)

    def _change_theme(self, name):
        set_theme(name)
        self.sidebar.set_active_theme(name)
        self._apply_all_themes()

    def _navigate(self, name):
        if "Lessons" in name:
            self.stack.slide_to(0)
        elif "Code Editor" in name:
            self.stack.slide_to(2)
        elif "AI Assistant" in name:
            self.stack.slide_to(3)

    def _open_lesson(self, idx):
        self.detail_page.set_lesson(idx)
        self.stack.slide_to(1)

    def _back(self):
        self.stack.slide_to(0)
        self.sidebar.set_active("📚 Lessons")

    def _try_code(self, code):
        self.editor_page.set_code(code)
        self.stack.slide_to(2)
        self.sidebar.set_active("💻 Code Editor")

    def _insert_ai_code(self, code):
        self.editor_page.set_code(code)
        self.stack.slide_to(2)
        self.sidebar.set_active("💻 Code Editor")
        self._set_status("  Code inserted from AI")


# ─── Entry ───────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(T["bg"]))
    p.setColor(QPalette.ColorRole.WindowText, QColor(T["text"]))
    p.setColor(QPalette.ColorRole.Base, QColor(T["bg2"]))
    p.setColor(QPalette.ColorRole.Text, QColor(T["text"]))
    p.setColor(QPalette.ColorRole.Highlight, QColor(T["accent"]))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor(T["text"]))
    app.setPalette(p)
    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
