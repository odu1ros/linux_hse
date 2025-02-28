from flask import request, jsonify, make_response
from app import app, db, api
from app.models import Task, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields
from datetime import timedelta

# namespaces for requests
namespace_tasks = Namespace('tasks', description='Requests related to tasks management')
namespace_auth = Namespace('auth', description='Requests related to user authentication')

api.add_namespace(namespace_tasks)
api.add_namespace(namespace_auth)

# general task parameter fields for swagger documentation
task_model = api.model('Task', {
    'id': fields.Integer(readonly=True, description='Task id in the database'),
    'title': fields.String(required=True, description='Task title'),
    'description': fields.String(description='Task description'),
    'done': fields.Boolean(description='Task completement state')
})

# task creation parameter fields for swagger documentation
task_creation_model = api.model('TaskCreation', {
    'title': fields.String(required=True, description='Task title'),
    'description': fields.String(description='Task description')
})

@namespace_tasks.route('')
class Tasks(Resource):
    """
    class of methods used for accessing tasks in database, /tasks namespace
    """
    @jwt_required()
    @namespace_tasks.doc(description="""Get all tasks for current user
                                      **Example Usage:**
                                      ```
                                      curl -X GET -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:5000/tasks -v
                                      ```""")
    @namespace_tasks.marshal_list_with(task_model, code=200)
    def get(self):
        """
        get tasks of current user

        :return: all tasks, code 200: json
        """
        current_user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        
        return tasks, 200
 
    @jwt_required()
    @namespace_tasks.doc(description="""Create new task for current user
                                      **Example Usage:**
                                      ```
                                      curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_JWT_TOKEN" -d "{\"title\": \"My New Task\", \"description\": \"Task description here\"}" http://127.0.0.1:5000/tasks -v
                                      ```""",
                                      )
    @namespace_tasks.expect(task_creation_model, mask=False)
    @namespace_tasks.marshal_with(task_model, code=201)
    @namespace_tasks.response(400, 'Title is required')
    def post(self):
        """
        add new task in database for current user

        :return: new task, code 201: json
        """
        data = request.get_json()
        if not data or 'title' not in data:
            return make_response(jsonify({'message': 'Title is required'}), 400)
         
        current_user_id = get_jwt_identity()
        new_task = Task(title=data['title'], description=data.get('description', ''), done=False, user_id=current_user_id)
        db.session.add(new_task)
        db.session.commit()

        return new_task, 201


@namespace_tasks.route('/<int:task_id>')
class TaskById(Resource):
    """
    class of methods used for accessing specific tasks in database, /tasks namespace
    """
    @jwt_required()
    @namespace_tasks.doc(description="""Get specific task of current user by task id 
                                      **Example Usage:**
                                      ```
                                      curl -X GET -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:5000/tasks/1 -v
                                      ```""",
                          )
    @namespace_tasks.marshal_with(task_model, code=200)
    @namespace_tasks.response(404, 'Task not found')
    def get(self, task_id):
        """
        get info of specific task for current user

        :return: task, code 200: json
        """
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        if task is None:
            return make_response(jsonify({'message': 'Task not found'}), 404)
        
        return task, 200

    @jwt_required()
    @namespace_tasks.doc(description="""Update specific task of current user by task id 
                                      **Example Usage:**
                                      ```
                                      curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_JWT_TOKEN" -d "{\"title\": \"Updated Task Title\", \"description\": \"Updated description\", \"done\": true}" http://127.0.0.1:5000/tasks/1 -v 
                                      ```""",
                          )
    @namespace_tasks.expect(task_model, mask=False)
    @namespace_tasks.marshal_with(task_model, code=200)
    @namespace_tasks.response(404, 'Task not found')
    def put(self, task_id):
        """
        update a specific task for current user

        :return: updated task, code 201: json
        """
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        if task is None:
            return make_response(jsonify({'message': 'Task not found'}), 404)
         
        data = request.get_json()
        if data:
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.done = data.get('done', task.done)
            db.session.commit()

        return Task.query.filter_by(id=task_id, user_id=current_user_id).first(), 200
 
    @jwt_required()
    @namespace_tasks.doc(description="""Delete specific task of current user by id 
                                      **Example Usage:**
                                      ```
                                      curl -X DELETE -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:5000/tasks/1 -v 
                                      ```""",
                          )
    @namespace_tasks.response(204, '')
    @namespace_tasks.response(404, 'Task not found')
    def delete(self, task_id):
        """
        delete a specific task of current user

        :return: empty str, code 204: json
        """
        current_user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
        if task is None:
            return make_response(jsonify({'message': 'Task not found'}), 404)
         
        db.session.delete(task)
        db.session.commit()
        return '', 204
     

@namespace_auth.route('/register')
class Register(Resource):
    """
    class of methods used for registering a user, /register namespace
    """
    @namespace_auth.doc(description="""Register new user 
                                      **Example Usage:**
                                      ```
                                      curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"new_user\", \"password\": \"new_password\"}" http://127.0.0.1:5000/auth/register -v 
                                      ```""", 
                                      code=201)
    @namespace_auth.response(400, 'No username or password provided')
    @namespace_auth.response(400, 'Username already taken')
    @namespace_auth.response(201, 'User registered successfully')
    def post(self):
        """
        create a record of new user login data in the database

        :return: message: str successful registration, code 201: Response object
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response(jsonify({'message': 'No username or password provided'}), 400)
         
        if User.query.filter_by(username=username).first():
            print('taken')
            return make_response(jsonify({'message': 'Username already taken'}), 400)
         
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'message': 'User registered successfully'}), 201)

@namespace_auth.route('/login')
class Login(Resource):
    """
    class of methods used to logging in a user, /login namespace
    """
    @namespace_auth.doc(description="""Log in existing user 
                                      **Example Usage:**
                                      ```
                                      curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"new_user\", \"password\": \"new_password\"}" http://127.0.0.1:5000/auth/login -v 
                                      ```""",
                                      code=200)
    @namespace_auth.response(400, 'No username or password provided')
    @namespace_auth.response(401, 'Invalid username or password')
    def post(self):
        """
        create a token for user to access his records in the database

        :return: user token, code 200: Response object
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response(jsonify({'message': 'No username or password provided'}), 400)

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
            return make_response(jsonify(access_token=access_token), 200)
         
        return make_response(jsonify({'message': 'Invalid username or password'}), 401)

@app.route('/')
def index():
    """
    root directory
    """
    return "Welcome to the Task Management API! Go to /api to view swagger documentation"

# @app.route('/')
# def index():
#     return "Welcome to the Task Management REST API!"

# @app.route('/tasks', methods=['GET'])
# @jwt_required() # adding possibility of assessing user's personal tasks
# def get_tasks():
#     current_user_id = get_jwt_identity()
#     tasks = Task.query.filter_by(user_id=current_user_id).all()
#     task_list = [{'id': task.id, 'title': task.title, 'description': task.description, 'done': task.done} for task in tasks]
#     return jsonify(task_list), 200


# @app.route('/tasks', methods=['POST'])
# @jwt_required()
# def create_task():
#     data = request.get_json()
#     if not data or 'title' not in data:
#         return jsonify({'message': 'Title is required'}), 400
    
#     current_user_id = get_jwt_identity()
#     new_task = Task(title=data['title'], description=data.get('description', ''), done=False, user_id=current_user_id)
#     db.session.add(new_task)
#     db.session.commit()
#     return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description, 'done': new_task.done}), 201


# @app.route('/tasks/<int:task_id>', methods=['GET'])
# @jwt_required()
# def get_task(task_id):
#     current_user_id = get_jwt_identity()
#     task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
#     if task is None:
#         return jsonify({'message': 'Task not found'}), 404
#     return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'done': task.done}), 200


# @app.route('/tasks/<int:task_id>', methods=['PUT'])
# @jwt_required()
# def update_task(task_id):
#     current_user_id = get_jwt_identity()
#     task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
#     if task is None:
#          return jsonify({'message': 'Task not found'}), 404
    
#     data = request.get_json()
#     if data:
#         task.title = data.get('title', task.title)
#         task.description = data.get('description', task.description)
#         task.done = data.get('done', task.done)
#         db.session.commit()

#     return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'done': task.done}), 200


# @app.route('/tasks/<int:task_id>', methods=['DELETE'])
# @jwt_required()
# def delete_task(task_id):
#     current_user_id = get_jwt_identity()
#     task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()
#     if task is None:
#         # not found here since i think ignoring does not tell user anything about the task
#         # but not found says of previous state of it
#         return jsonify({'message': 'Task not found'}), 404
    
#     db.session.delete(task)
#     db.session.commit()
#     return '', 204

# @app.route('/register', methods=['POST'])
# def register_user():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'No username or password provided'}), 400
    
#     if User.query.filter_by(username=username).first():
#         return jsonify({'message': 'Username already taken'}), 400
    
#     user = User(username=username, password=password)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({'message': 'User registered successfully'}), 201

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'No username or password provided'}), 400

#     user = User.query.filter_by(username=username).first()
#     if user and user.password == password:
#         access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
#         return jsonify(access_token=access_token), 200
    
#     return jsonify({'message': 'Invalid username or password'}), 401