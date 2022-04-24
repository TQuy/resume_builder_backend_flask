from email.policy import default
from enum import unique
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now())

    def __repr__(self):
        return f"<User {self.username}>"


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(
        'User', backref=db.backref(
            'resumes', lazy='select'))
    __table_args__ = (
        db.UniqueConstraint(
            'name',
            'user_id',
            name='unique_resume__name_user'),
    )

# class Resume(models.Model):
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     created_at = models.DateField(auto_now_add=True)
#     modified_at = models.DateField(auto_now=True)
#     name = models.CharField(max_length=100)
#     # to avoid overload
#     content = models.TextField(blank=True, max_length=1000)

#     def __str__(self):
#         return f"{self.id} - {self.name}"

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['name', 'user'], name='unique_resume_name')
