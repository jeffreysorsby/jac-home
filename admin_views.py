
from flask_admin.contrib.sqla import ModelView
import flask_wtf
from flask_admin.contrib import sqla

class DocumentView(ModelView):
    form_base_class = flask_wtf.Form
    column_hide_backrefs = True
    can_export = True
    column_searchable_list = ['name']


class CarView(ModelView):
    form_base_class = flask_wtf.Form
    column_hide_backrefs = True
    can_export = True
    column_exclude_list = ['documents']
    column_searchable_list = ['name']
    form_choices = {
    'category': [
        ('Autos', 'Autos'),
        ('EVs', 'EVs'),
        ('SUVs', 'SUVs'),
        ('Pickups', 'Pickups'),
        ('LCVs', 'LCVs')
    ]
}
    
