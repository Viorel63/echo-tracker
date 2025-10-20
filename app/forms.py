from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Optional

class IssueForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])

    status = SelectField('Status', choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed')
    ], default='Open')

    priority = SelectField('Priority', choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical')
    ], default='Medium')

    assignee_id = IntegerField('Assignee ID', validators=[Optional()])

    submit = SubmitField('Create Issue')

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    author_id = IntegerField('Author ID', validators=[DataRequired()])
    submit = SubmitField('Add Comment')
