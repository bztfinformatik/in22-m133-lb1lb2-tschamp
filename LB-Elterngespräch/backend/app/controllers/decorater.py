from flask import redirect, request, flash, url_for
from flask.templating import render_template
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from functools import wraps

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated: #the user is not logged in
                return redirect('/')

            #user = User.query.filter_by(id=current_user.id).first()

            if not current_user.allowed(access_level):
                flash('You do not have access to this resource.', 'danger')
                return redirect('/')
            return f(*args, **kwargs)
        return decorated_function
    return decorator