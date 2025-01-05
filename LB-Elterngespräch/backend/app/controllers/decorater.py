# controllers/decorater.py
from flask import redirect, url_for, flash
from functools import wraps
from flask_login import current_user

def requires_access_level(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                flash("You do not have the required permissions to access this page.", "danger")
                return redirect(url_for('index_blueprint.index'))
            return func(*args, **kwargs)
        return wrapper
    return decorator
