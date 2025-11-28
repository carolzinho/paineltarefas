from flask import Flask, render_template, request, jsonify
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/paineltarefas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return jsonify([{'id': t.id, 'title': t.title, 'completed': t.completed} for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Título obrigatório'}), 400
    task = Task(title=data['title'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    if 'completed' in data:
        task.completed = data['completed']
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
