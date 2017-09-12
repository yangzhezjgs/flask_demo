# coding: utf-8

from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='sqlite:////tmp/messages.db'
))

db = SQLAlchemy(app)
class Item(db.Model):
	__tablename__ = 'items'
	id = db.Column(db.Integer,primary_key=True)
	text = db.Column(db.String(64))
	isFinished = db.Column(db.Boolean)
	
	def to_dict(self):
		return {
			'text':self.text,
			'isFinished':self.isFinished
		}

@app.route('/api/get', methods=['GET'])
def get_item():
	items = Item.query.all()
	return jsonify([item.to_dict() for item in items])

@app.route('/api/insert',methods=['POST'])
def insert_item():
	data = request.get_json()
	item = Item(text=data['text'],isFinished=data['isFinished'])
	db.session.add(item)
	db.session.commit()
	return jsonify(ok=True)

@app.route('/api/update',methods=['POST'])
def update_item():
	data = request.get_json()
	item = Item.query.filter_by(text=data['text']).first()
	item.isFinished = not item.isFinished
	db.session.add(item)
	db.session.commit()
	return jsonify(ok=True)

@app.route('/api/delete',methods=['POST'])
def delete_item():
	data = request.get_json()
	item = Item.query.filter_by(text=data['text']).first()
	db.session.delete(item)
	db.session.commit()
	return jsonify(ok=True)
if __name__ == '__main__':
    app.run()
