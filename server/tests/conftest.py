"""
tests/conftest.py — הגדרות משותפות ל-pytest
"""
import sys
import os

# מוסיף את שורש הפרויקט ל-sys.path כדי שכל ה-imports יעבדו
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
