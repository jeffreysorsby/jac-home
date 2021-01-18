import os
from flask import Flask, jsonify, abort, request, render_template, flash, url_for, redirect, send_file, send_from_directory
from models import setup_db, Car, Document, Boletin
from admin_views import DocumentView, CarView
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from forms import CarForm, DocumentForm
from flask_wtf import CSRFProtect
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link
from flask_admin.contrib import sqla
from flask_admin import Admin
from flask_babelex import Babel
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.fileadmin.s3 import S3FileAdmin
import os.path as op
from flask_basicauth import BasicAuth

from auth import AuthException


import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.config.from_object('config')
db = setup_db(app)

basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_USERNAME'] = os.environ['BASIC_AUTH_USERNAME']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['BASIC_AUTH_PASSWORD']

Bootstrap(app)
nav = Nav(app)
nav.init_app(app)
CORS(app)
CORS(app, resources={r"*": {"origins": "*"}})
#csrf = CSRFProtect(app)
babel = Babel(app)

class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated. Refresh the page.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

app.config['FLASK_ADMIN_SWATCH'] = 'lumen'
admin = Admin(app, name='JAC Home Admin', template_mode='bootstrap3')
admin.add_view(CarView(Car, db.session))
admin.add_view(DocumentView(Document, db.session))
admin.add_view(ModelView(Boletin, db.session))
admin.add_view(S3FileAdmin('jachome.mx', 'us-east-1', os.environ['S3_KEY_ID'], os.environ['S3_SECRET']))

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@babel.localeselector
def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'es'

@nav.navigation()
def navbar_home():
    return Navbar(
        'JAC Home',
       View('Modelos', 'home'),
       View('Documentos', 'get_documents'),
       Link('Admin', '/admin')
)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


#HOME
@app.route('/')
def home():
    resp = get_cars().get_json()
    data = resp.get('data')
    return render_template('home.html', cars=data)

@app.route('/logout')
def logout():
    raise AuthException('Successfully logged out.')

@app.route('/files/<path:filename>')
def download(filename):
    uploads = os.path.join(app.root_path, 'files')
    return send_from_directory(directory=uploads, filename=filename)


#MODELS
@app.route('/model/<endpoint>')
def get_models(endpoint):
    try:
        car = Car.query.filter(Car.endpoint == endpoint).one_or_none()
        name = car.name
        resp = get_car_documents(car.id).get_json()
        data = resp.get('documents')
    except:
        abort(404)
    
    return render_template('models.html', docs=data, name=name)
#GET ALL CARS
@app.route('/cars', methods=['GET'])
def get_cars():
    try:
        cars = Car.query.order_by(Car.name).all()
        data = [car.format() for car in cars]
    except:
        abort(400)
    
    return jsonify({
        'success': True,
        'data': data
        })
#GET CARS BY ID
@app.route('/cars/<int:car_id>', methods=['GET'])
def get_cars_byid(car_id):
    try:
        cars = Car.query.filter(Car.id == car_id).one_or_none()
        data = cars.format()
    except:
        abort(400)
    
    return jsonify({
        'success': True,
        'data': data
        })
#CREATE CARS
@app.route('/cars', methods=['POST'])
def post_car():
    try:
        request_name = request.form.get('name')
        request_image_url = request.form.get('image_url')
        request_endpoint = request.form.get('endpoint')
        request_category = request.form.get('category')
        new_car = Car(name=request_name, image_url=request_image_url, endpoint=request_endpoint, category=request_category)
        new_car.insert()
    except:
        abort(400)
    return jsonify({
        'success': True,
        'new_car': new_car.format()
    })
#CREATE CARS FORM
@app.route('/cars/create', methods=['GET'])
def post_car_form():
    form = CarForm()
    return render_template('new_car.html', form=form)
#DELETE CARS
@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.filter(Car.id == car_id).one_or_none()
    if car is None:
        abort(400)
    try:
        car.delete()
        return jsonify({
            'success': True,
            'message': 'Car successfully deleted'
        })
    except:
        abort(400)
#EDIT CARS FORM
@app.route('/cars/edit/<int:car_id>', methods=['GET'])
def edit_car_form(car_id):
    car = Car.query.filter(Car.id == car_id).one_or_none()
    form = CarForm(obj=car)
    return render_template('edit_car.html', form=form, car=car)
#EDIT CARS
@app.route('/cars/<int:car_id>', methods=['POST'])
def edit_car(car_id):
    error = False
    try:
        form = CarForm(request.form)
        car = Car.query.filter(Car.id == car_id).one_or_none()
        if car is None:
            abort(404)
        car.name = request.form.get('name')
        car.image_url = request.form.get('image_url')
        car.endpoint = request.form.get('endpoint')
        car.category = request.form.get('category')
        car.update()
    except:
        abort(400)
        error = True
    if not error:
        flash('Car successfully updated!')
    else:
        flash('Car was not updated!')
    
    
    return redirect(url_for('home'))
#GET ALL DOCUMENTS
@app.route('/documents', methods=['GET'])
def get_documents():
    try:
        docs = Document.query.order_by(Document.name).all()
        data = [doc.format() for doc in docs]
    except:
        abort(400)
    
    return render_template('documents.html', docs=data)
@app.route('/all-documents')
def get_all_documents():
    try:
        docs = Document.query.join(Car).all()
        data = [doc.format() for doc in docs]
        
    except:
        abort(400)
    
    return jsonify({
        "data": data
    })
@app.route('/documents/<int:document_id>', methods=['GET'])
def get_documents_byid(document_id):
    try:
        docs = Document.query.filter(Document.id == document_id).one_or_none()
        data = docs.format()
    except:
        abort(400)
    
    return jsonify({
        'data': data
        })
#CREATE DOCUMENT FORM
@app.route('/documents/create', methods=['GET'])
def get_document_form():
    cars = Car.query.all()
    cars = [(car.id, car.name) for car in cars]
    form = DocumentForm()
    form.car_id.choices = cars
    return render_template('new_document.html', form=form)
#CREATE DOCUMENT
@app.route('/documents', methods=['POST'])
def post_documents():
    try:
        request_name = request.form.get('name')
        request_url = request.form.get('url')
        request_image_url = request.form.get('image_url')
        request_car_id = request.form.get('car_id')
        request_doc_type = request.form.get('doc_type')
        document = Document(name=request_name, url=request_url, image_url=request_image_url, car_id=request_car_id, doc_type=request_doc_type)
        document.insert()
    except:
        abort(400)
    return redirect(url_for('home'))
#EDIT DOCUMENT FORM
@app.route('/documents/edit/<int:document_id>')
def edit_document_form(document_id):
    doc = Document.query.filter(Document.id == document_id).one_or_none()
    form = DocumentForm(obj=doc)
    return render_template('edit_document.html', form=form, document=doc)
#EDIT DOCUMENT
@app.route('/documents/<int:document_id>', methods=['POST'])
def edit_documents(document_id):
    error = False
    try:
        form = DocumentForm(request.form)
        doc = Document.query.filter(Document.id == document_id).one_or_none()
        request_name = request.form.get('name')
        request_url = request.form.get('url')
        request_image_url = request.form.get('image_url')
        request_car_id = request.form.get('car_id')
        request_doc_type = request.form.get('doc_type')
        doc.name = request_name
        doc.url = request_url
        doc.image_url = request_image_url
        doc.car_id = request_car_id
        doc.doc_type = request_doc_type
        doc.update()
    except:
        abort(400)
        error = True
    if not error:
        flash('Document successfully updated!')
    else:
        flash('Document was not updated!')
    return redirect(url_for('home'))
#DELETE DOCUMENT
@app.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    doc = Document.query.filter(Document.id == document_id).one_or_none()
    if doc is None:
        abort(400)
    try:
        doc.delete()
        return jsonify({
            'success': True,
            'message': 'Document successfully deleted'
        })
    except:
        abort(400)
#GET CAR DOCUMENTS
@app.route('/cars/<int:car_id>/documents')
def get_car_documents(car_id):
    try:
        docs = Document.query.filter(Document.car_id == car_id)
        data = [doc.format() for doc in docs]
    except:
        abort(400)
    return jsonify({
        'success': True,
        'documents': data
    })

@app.route('/cars/search', methods=['POST'])
def search_cars():
    car_search = request.form.get('search_term')
    cars = Car.query.filter(Car.name.ilike('%' + car_search + '%')).all()
    data = [car.format() for car in cars]
    return render_template('car_search.html', cars=data)

@app.route('/documents/search', methods=['POST'])
def search_documents():
    doc_search = request.form.get('search_term')
    docs = Document.query.filter(Document.name.ilike('%' + doc_search + '%')).all()
    data = [doc.format() for doc in docs]
    return render_template('document_search.html', docs=data)

@app.errorhandler(404)  
def not_found_error(error):
    return jsonify({
        'message': 'Not found',
        'status_code': 404,
        'success': False
    }), 404

@app.errorhandler(401)
def permissions_error(error):
    return jsonify({
        'message': 'Permissions error',
        'status_code': 401,
        'success': False
    }), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)