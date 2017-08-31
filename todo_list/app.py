from flask import Flask, jsonify, request, abort,url_for,render_template,redirect
from time import time
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo

app = Flask(__name__)

mongo = pymongo.MongoClient('127.0.0.1', 27017)
db = mongo.todos

class Todo(object):
    @classmethod
    def create_doc(cls, content):
        return {
            'content': content,
            'created_at': time(),
            'is_finished': False,
            'finished_at': None
        }

@app.route('/todo/',methods=['GET'])
def index():
    todos = db.todos.find({})
    return  render_template('index.html',todos=todos)

@app.route('/todo/', methods=['POST'])
def add():
    content = request.form.get('content', None)
    if not content:
        abort(400)
    db.todos.insert(Todo.create_doc(content))
    return redirect('/todo/')

@app.route('/todo/<content>/finished')
def finish(content):
    result = db.todos.update_one(
        {'content':content},
        {
            '$set': {
                'is_finished': True,
                'finished_at': time()
            }
        }    
    )
    return redirect('/todo/')

@app.route('/todo/<content>')
def delete(content):
    result = db.todos.delete_one(
        {'content':content}
    )
    return redirect('/todo/')

if __name__ == '__main__':
    app.run(debug=True)
