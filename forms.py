from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired

class CarForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    image_url = StringField('image_url', validators=[DataRequired()])
    endpoint = StringField('endpoint', validators=[DataRequired()])
    category = SelectField('category', choices=[('Autos', 'Autos'), ('SUVs', 'SUVs'), ('Comerciales', 'Comerciales'), ('EVs', 'EVs'), ('Pickups', 'Pickups')], validators=[DataRequired()])

class DocumentForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    url = StringField('url', validators=[DataRequired()])
    image_url = StringField('image_url', validators=[DataRequired()])
    doc_type = StringField('doc_type', validators=[DataRequired()])
    car_id = SelectField('car_id', choices=[], validators=[DataRequired()])
