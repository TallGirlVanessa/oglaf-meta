from flask_wtf import FlaskForm
from wtforms import SearchField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    search = SearchField("Search", validators=[DataRequired(), Length(min=3, max=50)])
