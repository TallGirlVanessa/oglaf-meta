from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class TagSearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired(), Length(min=3, max=50)])
