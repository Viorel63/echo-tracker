from datetime import datetime
from app.extensions import db

# 👤 Пользователь
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # tester, developer, manager

    issues = db.relationship('Issue', backref='assignee', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# 🐞 Баг / задача
class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(20), default='Open')  # Open, In Progress, Resolved, Closed
    priority = db.Column(db.String(20), default='Medium')  # Low, Medium, High, Critical

    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', backref='issue', lazy=True)

    def __repr__(self):
        return f'<Issue {self.title}>'

# 💬 Комментарий
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id} on Issue {self.issue_id}>'

class IssueHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    field_changed = db.Column(db.String(64))
    old_value = db.Column(db.String(256))
    new_value = db.Column(db.String(256))
    changed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='history_entries')