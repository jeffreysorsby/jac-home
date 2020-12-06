import os
from flask import Flask, jsonify, abort, request
from models import setup_db, Car, Document
from flask_cors import CORS
from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    #GET ALL CARS
    @app.route('/cars', methods=['GET'])
    @requires_auth('get:cars')
    def get_cars(payload):
        try:
            cars = Car.query.all()
            data = [car.format() for car in cars]
        except:
            abort(400)
        
        return jsonify({
            'success': True,
            'data': data
            })

    #GET CARS BY ID
    @app.route('/cars/<int:car_id>', methods=['GET'])
    @requires_auth('get:cars')
    def get_cars_byid(payload, car_id):
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
    @requires_auth('post:cars')
    def post_car(payload):
        body = request.get_json()
        request_name = body.get('name')
        request_image_url = body.get('image_url')
        request_endpoint = body.get('endpoint')

        try:
            new_car = Car(name=request_name, image_url=request_image_url, endpoint=request_endpoint)
            new_car.insert()
        except:
            abort(400)

        return jsonify({
            'success': True,
            'new_car': new_car.format()
        })

    #DELETE CARS
    @app.route('/cars/<int:car_id>', methods=['DELETE'])
    @requires_auth('delete:cars')
    def delete_car(payload, car_id):
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

    #PATCH CARS
    @app.route('/cars/<int:car_id>', methods=['PATCH'])
    @requires_auth('patch:cars')
    def edit_car(payload, car_id):
        try:
            car = Car.query.filter(Car.id == car_id).one_or_none()
            if car is None:
                abort(404)
            body = request.get_json()
            car.name = body.get('name')
            car.image_url = body.get('image_url')
            car.endpoint = body.get('endpoint')
            car.update()
        except:
            abort(400)
        
        return jsonify({
            'success': True,
            'car': [car.format()]
        })

    #GET ALL DOCUMENTS
    @app.route('/documents', methods=['GET'])
    @requires_auth('get:documents')
    def get_documents(payload):
        try:
            docs = Document.query.all()
            data = [doc.format() for doc in docs]
        except:
            abort(400)
        
        return jsonify({
            'data': data,
            'success': True
            })
    #GET DOCUMENT BY ID
    @app.route('/documents/<int:document_id>', methods=['GET'])
    @requires_auth('get:documents')
    def get_documents_byid(payload, document_id):
        try:
            docs = Document.query.filter(Document.id == document_id).one_or_none()
            data = docs.format()
        except:
            abort(400)
        
        return jsonify({
            'data': data,
            'success': True
            })

    #CREATE DOCUMENT
    @app.route('/documents', methods=['POST'])
    @requires_auth('post:documents')
    def post_documents(payload):
        try:
            body = request.get_json()
            request_name = body.get('name')
            request_url = body.get('url')
            request_image_url = body.get('image_url')
            request_car_id = body.get('car_id')
            request_doc_type = body.get('doc_type')
            document = Document(name=request_name, url=request_url, image_url=request_image_url, car_id=request_car_id, doc_type=request_doc_type)
            document.insert()
        except:
            abort(400)

        return jsonify({
            'success': True,
            'document': document.format()
        })

    #EDIT DOCUMENT
    @app.route('/documents/<int:document_id>', methods=['PATCH'])
    @requires_auth('patch:documents')
    def patch_documents(payload, document_id):
        try:
            doc = Document.query.filter(Document.id == document_id).one_or_none()
            body = request.get_json()
            request_name = body.get('name')
            request_url = body.get('url')
            request_image_url = body.get('image_url')
            request_car_id = body.get('car_id')
            request_doc_type = body.get('doc_type')

            doc.name = request_name
            doc.url = request_url
            doc.image_url = request_image_url
            doc.car_id = request_car_id
            doc.doc_type = request_doc_type
            doc.update()

        except:
            abort(400)

        return jsonify({
            'success': True,
            'document': doc.format()
        })

    #DELETE DOCUMENT
    @app.route('/documents/<int:document_id>', methods=['DELETE'])
    @requires_auth('delete:documents')
    def delete_document(payload, document_id):
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
    @requires_auth('get:documents')
    def get_car_documents(payload, car_id):
        try:
            docs = Document.query.filter(Document.car_id == car_id)
            data = [doc.format() for doc in docs]
            if data is None:
                abort(400)
        except:
            abort(400)
        

        return jsonify({
            'success': True,
            'documents': data
        })

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'message': 'Not found',
            'status_code': 404,
            'success': False
        }), 404

    @app.errorhandler(400)
    def request_error(error):
        return jsonify({
            'message': 'Request error',
            'status_code': 400,
            'success': False
        }), 400

    @app.errorhandler(AuthError)
    def permissions_error(AuthError):
        return jsonify({
            'message': 'Auth error',
            'status_code': 401,
            'success': False
        }), 401

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'message': 'Method not allowed',
            'status_code': 405,
            'success': False
        }), 405

    return app

app = create_app()

if __name__ == '__main__':
    app.run()