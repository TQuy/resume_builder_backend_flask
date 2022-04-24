from flask import request, jsonify, current_app
from functools import wraps
import jwt
from flaskr.models import User

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'Authentication' in request.headers:
           token = request.headers['Authentication']
 
       if not token:
           return jsonify({'message': 'A valid token is missing'})
       try:
           data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(id=data['user_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator