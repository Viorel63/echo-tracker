from flask import Blueprint, render_template, redirect, url_for, request
from app.forms import IssueForm, CommentForm
from app.models import Issue, Comment, User
from app.extensions import db
from datetime import datetime

issues_bp = Blueprint('issues', __name__)

@issues_bp.route('/issues')
def list_issues():
    status = request.args.get('status')
    priority = request.args.get('priority')
    assignee_id = request.args.get('assignee_id')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_dir = request.args.get('sort_dir', 'desc')
    page = request.args.get('page', 1, type=int)
    per_page = 10

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

    return render_template('index.html', issues=issues, pagination=pagination, filters=request.args)

@issues_bp.route('/issue/<int:issue_id>')
def view_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return render_template('issue_detail.html', issue=issue)

@issues_bp.route('/issue/<int:issue_id>/comment', methods=['POST'])
def add_comment(issue_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            issue_id=issue_id,
            author_id=form.author_id.data,
            text=form.text.data
        )
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('issues.view_issue', issue_id=issue_id))

@issues_bp.route('/create', methods=['GET', 'POST'])
def create_issue():
    form = IssueForm()
    if form.validate_on_submit():
        new_issue = Issue(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            assignee_id=form.assignee_id.data or None
        )
        db.session.add(new_issue)
        db.session.commit()
        return redirect(url_for('issues.list_issues'))
    return render_template('create.html', form=form)

@issues_bp.route('/edit/<int:issue_id>', methods=['GET', 'POST'])
def edit_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    form = IssueForm(obj=issue)

    if form.validate_on_submit():
        issue.title = form.title.data
        issue.description = form.description.data
        issue.status = form.status.data
        issue.priority = form.priority.data
        issue.assignee_id = form.assignee_id.data or None
        db.session.commit()
        return redirect(url_for('issues.view_issue', issue_id=issue.id))

    return render_template('edit.html', form=form, issue=issue)

@issues_bp.route('/delete/<int:issue_id>', methods=['POST'])
def delete_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    return redirect(url_for('issues.list_issues'))

@issues_bp.route('/create', methods=['POST'])
def create_issue_inline():
    title = request.form['title']
    description = request.form.get('description')
    status = request.form.get('status', 'Open')
    priority = request.form.get('priority', 'Medium')
    assignee_id = request.form.get('assignee_id') or None

    new_issue = Issue(
        title=title,
        description=description,
        status=status,
        priority=priority,
        assignee_id=assignee_id
    )
    db.session.add(new_issue)
    db.session.commit()
    return redirect(url_for('issues.list_issues'))
