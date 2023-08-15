from flask_login import current_user
from models import User


def inject_current_user():
    user = None
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
    return {'current_user': user}
