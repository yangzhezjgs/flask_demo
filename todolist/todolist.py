# coding: utf-8
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField
from wtforms.validators import Required,Length
from werkzeug.datastructures import MultiDict

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

class ItemForm(Form):
	text = StringField(validators=[Required(), Length(1, 64)])

@app.route('/api/get', methods=['GET'])
def get_item():
	items = Item.query.all()
	return jsonify([item.to_dict() for item in items])

@app.route('/api/insert',methods=['POST'])
def insert_item():
	data = MultiDict(request.get_json())
	form = ItemForm(text=data, obj=None, csrf_enabled=False)
	if not form.validate():
		print form.errors
		return jsonify(ok=False,errors=form.errors),422
	item = Item(text=data['text'],isFinished=data['isFinished'])
	db.session.add(item)
	db.session.commit()
	return jsonify(ok=True),201

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
