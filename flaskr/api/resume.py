import json
from flask import Blueprint, request, jsonify
from flaskr.decorators import token_required
from flaskr.models import db, User, Resume
from sqlalchemy import select

from flaskr.services.resume import delete_resume, list_resume, load_resume, save_resume, validate_input_save_form

bp = Blueprint('resume', __name__, url_prefix='/resume/')


@bp.route('list/', methods=('GET',))
@token_required
def list(current_user):
    if request.method == 'GET':
        resume_list = list_resume(current_user)
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
def load(current_user, resume_id):
    resume = load_resume(current_user, resume_id)
    if resume is None:
        return jsonify({
            'message': 'Resume not found.'
        }), 404
    return jsonify({
        'id': resume_id,
        'name': resume.name,
        'content': json.loads(resume.content),
        'message': 'Loaded resume successfully'
    }), 200


@bp.route('save/', methods=('POST',))
@token_required
def save(current_user):
    name = request.json.get('name', None)
    content = request.json.get('content', None)
    error = validate_input_save_form(name, content)
    if error:
        return jsonify({
            'message': error
        }), 400
    resume = save_resume(current_user, name, content)

    return jsonify({
        'id': resume.id,
        'name': resume.name,
        'content': json.loads(resume.content),
        'message': 'Saved resume successfully.'
    }), 200


@bp.route('delete/<int:resume_id>/', methods=('DELETE',))
@token_required
def delete(current_user, resume_id):
    res = delete_resume(current_user, resume_id)
    if not res:
        return jsonify({
            'message': 'Resume not found.'
        }), 404
    return jsonify({
        'message': 'Deleted resume successfully.'
    }), 200
