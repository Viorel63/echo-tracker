from flask import Blueprint
from app.routes.api import api_bp

@api_bp.route('/comments/<int:issue_id>', methods=['GET'])
def get_comments(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return jsonify([{
        'author': c.author.username if c.author else None,
        'text': c.text,
        'created_at': c.created_at.isoformat()
    } for c in issue.comments])


comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/comments')
def index():
    return "Comments route is working"
