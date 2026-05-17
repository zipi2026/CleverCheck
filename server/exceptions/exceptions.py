"""
exceptions/exceptions.py — חריגות מותאמות לפרויקט
"""


class CleverCheckBaseError(Exception):
    """בסיס לכל חריגות הפרויקט."""
    http_status: int = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


# ── שכבת Service ─────────────────────────────────────────────
class ModelNotFoundError(CleverCheckBaseError):
    """מודל ה-embedding אינו נמצא בנתיב שהוגדר."""
    http_status = 503


class GradingError(CleverCheckBaseError):
    """שגיאה כללית בתהליך הערכה."""
    http_status = 500


# ── שכבת Validation ──────────────────────────────────────────
class ValidationError(CleverCheckBaseError):
    """קלט לא תקין מהמשתמש."""
    http_status = 400


# ── שכבת Repository ──────────────────────────────────────────
class DatabaseError(CleverCheckBaseError):
    """שגיאת גישה / כתיבה למסד הנתונים."""
    http_status = 503
