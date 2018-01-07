# coding: utf-8

from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField
from wtforms.validators import Required,Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///./messages.db'
))

db = SQLAlchemy(app)

class ItemForm(Form):
        text = StringField(validators=[Required(), Length(1, 64)])

class Item(db.Model):
	__tablename__ = 'items'
	id = db.Column(db.Integer,primary_key=True,autoincrement=True)
	text = db.Column(db.String(64))
	is_Finished = db.Column(db.Boolean)

	def to_dict(self):
		return {
			'id' : self.id,
			'text' : self.text,
			'is_Finished' : self.is_Finished
			}

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()
		

class RestView(MethodView):
	def get(self):
		items = Item.query.all()
		return jsonify([item.to_dict() for item in items])

	def post(self):
		data = request.get_json()
		form = ItemForm(text=data, obj=None, csrf_enabled=False)
		if not form.validate():
			print (form.errors)
			return jsonify(ok=False,errors=form.errors),422
		item = Item(text=data['text'],is_Finished=data['isFinished'])
		item.save()
		return jsonify(ok=True,id=item.id),201

	def put(slef):
		data = request.get_json()
		item = Item.query.filter_by(id=data['id']).first()
		item.is_Finished = not item.is_Finished
		item.save()
		return jsonify(ok=True)

	def delete(self):
		data = request.get_json()
		print(data)
		item = Item.query.filter_by(id=data['id']).first()
		item.delete()
		return jsonify(ok=True)

app.add_url_rule('/api/item', view_func=RestView.as_view('todo'))

if __name__ == '__main__':
	app.run()
