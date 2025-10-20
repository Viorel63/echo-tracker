from flask import Blueprint, request, jsonify
from app.models import Issue, Comment, User, IssueHistory
from app.extensions import db
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Получение списка багов
@api_bp.route('/issues', methods=['GET'])
def get_issues():
    status = request.args.get('status')
    priority = request.args.get('priority')
    assignee_id = request.args.get('assignee_id')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_dir = request.args.get('sort_dir', 'desc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Issue.query

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if assignee_id:
        query = query.filter_by(assignee_id=assignee_id)

    sort_column = getattr(Issue, sort_by, Issue.created_at)
    query = query.order_by(sort_column.asc() if sort_dir == 'asc' else sort_column.desc())

    pagination = query.paginate(page=page, per_page=per_page)
    issues = pagination.items

    return jsonify({
        'page': page,
        'total_pages': pagination.pages,
        'total_items': pagination.total,
        'issues': [{
            'id': i.id,
            'title': i.title,
            'status': i.status,
            'priority': i.priority,
            'assignee': i.assignee.username if i.assignee else None,
            'created_at': i.created_at.isoformat()
        } for i in issues]
    })

# Получение одного бага
@api_bp.route('/issues/<int:issue_id>', methods=['GET'])
def get_issue_by_id(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return jsonify({
        'id': issue.id,
        'title': issue.title,
        'description': issue.description,
        'status': issue.status,
        'priority': issue.priority,
        'assignee': issue.assignee.username if issue.assignee else None,
        'created_at': issue.created_at.isoformat(),
        'comments_count': issue.comments.count(),
        'history_count': len(issue.history)
    })

# Создание бага
@api_bp.route('/issues', methods=['POST'])
def create_issue():
    data = request.json
    issue = Issue(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'Open'),
        priority=data.get('priority', 'Medium'),
        assignee_id=data.get('assignee_id')
    )
    db.session.add(issue)
    db.session.commit()
    return jsonify({'id': issue.id}), 201

# Обновление бага
@api_bp.route('/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    data = request.json
    issue.title = data.get('title', issue.title)
    issue.description = data.get('description', issue.description)
    issue.status = data.get('status', issue.status)
    issue.priority = data.get('priority', issue.priority)
    issue.assignee_id = data.get('assignee_id', issue.assignee_id)
    db.session.commit()
    return jsonify({'message': 'Issue updated'})

# Удаление бага
@api_bp.route('/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    return jsonify({'message': 'Issue deleted'})

# Добавление комментария
@api_bp.route('/issues/<int:issue_id>/comments', methods=['POST'])
def add_comment(issue_id):
    data = request.json
    comment = Comment(
        issue_id=issue_id,
        author_id=data['author_id'],
        text=data['text']
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added'}), 201

# Получение комментариев
@api_bp.route('/comments/<int:issue_id>', methods=['GET'])
def fetch_comments(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return jsonify([{
        'author': c.author.username if c.author else None,
        'text': c.text,
        'created_at': c.created_at.isoformat()
    } for c in issue.comments])

# Получение истории изменений
@api_bp.route('/history/<int:issue_id>', methods=['GET'])
def get_history(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return jsonify([{
        'field': h.field_changed,
        'old': h.old_value,
        'new': h.new_value,
        'changed_by': h.user.username if h.user else None,
        'changed_at': h.changed_at.isoformat()
    } for h in issue.history])
