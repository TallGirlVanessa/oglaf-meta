from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class TagSearchForm(FlaskForm):
    search = StringField("Tag search", validators=[DataRequired()])
