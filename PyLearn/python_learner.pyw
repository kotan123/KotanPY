"""PyLearn Launcher — runs without console window on Windows."""
import runpy, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
runpy.run_module("python_learner", run_name="__main__")
