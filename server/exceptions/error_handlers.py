"""
exceptions/error_handlers.py — רישום Global Error Handlers ב-Flask
"""
import logging
from flask import Flask, jsonify

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "הנתיב המבוקש אינו קיים"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method לא מורשה לנתיב זה"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        logger.exception("Unhandled 500 error")
        return jsonify({"error": "שגיאה פנימית בשרת"}), 500
