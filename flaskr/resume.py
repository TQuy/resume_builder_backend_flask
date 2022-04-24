from flask import Blueprint, request, jsonify
from flaskr.decorators import token_required
from flaskr.models import db, User, Resume
from sqlalchemy import select

bp = Blueprint('resume', __name__, url_prefix='/')

@bp.route('/resumes/', methods=('GET',))
@token_required
def list_resume(current_user):
    if request.method == 'GET':
        resume_list = db.session.execute(select(Resume.id, Resume.name).join(User).where(User.id==current_user.id)).all()
        resume_list = [dict(i) for i in resume_list]
        return jsonify({
            'content': resume_list,
            'message': 'Loaded list of resumes successfully'
        }), 200
    else:
        return jsonify({
            'message': 'Method not supported.'
        }), 405
