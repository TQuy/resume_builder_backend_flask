import json
from flask import Blueprint, request, jsonify
from flaskr.decorators import token_required
from flaskr.models import db, User, Resume
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

bp = Blueprint('resume', __name__, url_prefix='/resume/')


@bp.route('list/', methods=('GET',))
@token_required
def list_resume(current_user):
    if request.method == 'GET':
        resume_list = db.session.execute(
            select(
                Resume.id,
                Resume.name).join(User).where(
                User.id == current_user.id)).all()
        resume_list = [dict(i) for i in resume_list]
        return jsonify({
            'content': resume_list,
            'message': 'Loaded list of resumes successfully'
        }), 200
    else:
        return jsonify({
            'message': 'Method not supported.'
        }), 405


@bp.route('<int:resume_id>/', methods=('GET',))
@token_required
def load_resume(current_user, resume_id):
    if request.method == 'GET':
        try:
            resume = db.session.scalars(
                select(Resume).where(
                    Resume.id == resume_id).where(
                    Resume.user_id == current_user.id)).one()
        except NoResultFound:
            return jsonify({
                'message': 'Resume not found.'
            }), 404
        return jsonify({
            'id': resume_id,
            'name': resume.name,
            'content': json.loads(resume.content),
            'message': 'Loaded resume successfully'
        }), 200
    else:
        return jsonify({
            'message': 'Method not allowed.'
        }), 405


@bp.route('save/', methods=('POST',))
@token_required
def save_resume(current_user):
    if request.method == 'POST':
        name = request.json.get('name', None)
        content = request.json.get('content', None)
        if name is None:
            return jsonify({
                'message': 'Empty name value',
            }), 400
        elif content is None:
            return jsonify({
                'message': 'Empty content value',
            }), 400
        existed = True
        try:
            resume = Resume.query.filter_by(user=current_user, name=name).one()
        except NoResultFound:
            resume = Resume(
                name=name,
                user=current_user
            )
            existed = False
        finally:
            resume.content = json.dumps(content)
            if existed:
                db.session.add(resume)
            db.session.commit()
        return jsonify({
            'id': resume.id,
            'name': resume.name,
            'content': json.loads(resume.content),
            'message': 'Saved resume successfully.'
        }), 200
    else:
        return jsonify({
            'message': 'Method not allowed.'
        }), 405


@bp.route('delete/<int:resume_id>/', methods=('DELETE',))
@token_required
def delete_resume(current_user, resume_id):
    if request.method == 'DELETE':
        try:
            resume = Resume.query.filter_by(
                id=resume_id, user=current_user).one()
        except NoResultFound:
            return jsonify({
                'message': 'Resume not found.'
            }), 404
        else:
            db.session.delete(resume)
            db.session.commit()
        return jsonify({
            'message': 'Deleted resume successfully.'
        }), 200
    else:
        return jsonify({
            'message': 'Method not allowed.'
        }), 405
