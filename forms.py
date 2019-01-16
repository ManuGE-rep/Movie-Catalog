# Importations nécessaires aux formulaires
# from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

# Class for the input of new movies


class MovieForm(FlaskForm):
    title = StringField('title',
                        validators=[DataRequired(), Length(min=2, max=80)])
    year = IntegerField('year',
                        validators=[DataRequired(),
                                    NumberRange(min=1970, max=2019,
                                    message='Date between 1970 and 2019')])
    description = StringField('description', validators=[DataRequired(),
                              Length(min=2, max=500)])
    cover = StringField('cover (url)',
                        validators=[DataRequired(), Length(min=2, max=250)])
    category = StringField('category', validators=[DataRequired(), Length(
                           min=2, max=80)])

    submit = SubmitField('submit')


# Class for edit and update a movie


class EditMovieForm(FlaskForm):
    title = StringField('title',
                        validators=[DataRequired(), Length(min=2, max=80)])
    year = IntegerField('year',
                        validators=[DataRequired(), NumberRange(
                         min=1970, max=2019, message='Date between 1970 '
                         'and 2019')])
    description = StringField('description', validators=[DataRequired(),
                              Length(min=2, max=500)])
    cover = StringField('cover (url)',
                        validators=[DataRequired(), Length(min=2, max=250)])
    category = StringField('category', validators=[DataRequired(),
                           Length(min=2, max=80)])
    submit = SubmitField('submit')
