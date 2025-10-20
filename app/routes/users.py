from flask import Blueprint
from app.models import db
from app.extensions import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
def index():
    return "Users route is working"
