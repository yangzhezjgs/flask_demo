from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField,TextField,TextAreaField,SubmitField,BooleanField
from wtforms.validators import Required, Length

class LoginForm(Form):
	username = StringField(validators=[Required(), Length(max=15)])
	password = StringField(validators=[Required(), Length(max=15)])
	remember_me = BooleanField('remember me', default=False)
	submit = SubmitField('Login')

class SignUpForm(Form):
	username = StringField(validators=[Required(), Length(max=15)])
	password = StringField(validators=[Required(), Length(max=15)])
	submit = SubmitField('Sign up')

class EditForm(Form):
	username = TextField('username', validators = [Required()])
	about_me = TextAreaField('about_me', validators = [Length(min = 0, max =140)])
	def __init__(self, original_username, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_username = original_username
	def validate(self):
		if not Form.validate(self):
			return False
		if self.username.data == self.original_username:
			return True
		user = User.query.filter_by(username = self.username.data).first()
		if user != None:
			return False
		return True

class ChangeForm(Form):
	title = TextField('title', validators = [Required()])
	content = TextAreaField('content', validators = [Length(min = 0, max=140)])

class PostForm(Form):
	title = TextField('title', validators = [Required(Length(min =0,max=120))])
	content = TextAreaField('content', validators = [Length(min = 0, max=1200)])
