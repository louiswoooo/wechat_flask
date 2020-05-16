from flask.ext.wtf import Form
from wtform import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    oepnid=StringField('openid',validators=[DataRequired()])
    remember_me=BooleanField('remember_me',default=False)