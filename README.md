# JAC Home - FSND Capstone Project

JAC is a chinese automotive company which sells new cars in the mexican market. JAC Home is a RESTful API which allows admins to create cars and documents asociated to it. This API will be used in the future with a front end which will allow users to see all cars on sale and all public documents asociated to it like images, manuals, etc.

## Runing the Development Server

JAC Home was developed with Python 3.7.9 and Flask.

Key project dependencies:

* SQLALCHEMY
* Flask

### Step 1: Install Requirements

```bash
pip3 install -r requirements.txt
```

### Step 2: Export env variables
```bash
sh setup.sh
```

### Step 3: Run app.py from /jac-home
```bash
python3 app.py
```

## API Reference

For local development testing, base url is:

```url
localhost:5000/
```

Heroku deployed application base url is:

```url
https://jac-home.herokuapp.com
```

### Authentication:

Test tokens are stored in the **setup.sh** file. They are valid for 24 hours.

All API endpoints need authentication through the Authentication header in the request in the form of a JWT Bearer token. The API uses two user roles:

* **Admin** has the following permissions:
  * get:cars
  * post:cars
  * patch:cars
  * delete:cars
  * get:documents
  * post:documents
  * patch:documents
  * delete:documents
* **User** has the following permissions:
  * get:cars
  * get:documents

### Endpoints

### GET /cars

Returns all cars. Requires **get:cars** permission. Replace **token** with valid Bearer token.

#### Sample Request
```bash
curl --location --request GET 'localhost:5000/cars' \
--header 'Authorization: Bearer token'
```

#### Sample Response
```json
{
    "data": [
        {
            "endpoint": "/j7",
            "id": 6,
            "image_url": "j7.com",
            "name": "T9"
        },
        {
            "endpoint": "/t9",
            "id": 7,
            "image_url": "t9.com",
            "name": "T9"
        }
    ],
    "success": true
}
```

### POST /cars

Creates new car. Requires **post:cars** permission. Replace **token** with valid Bearer token.

#### Sample Request

```bash
curl --location --request POST 'localhost:5000/cars' \
--header 'Authorization: Bearer token' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "E Sei4",
"image_url": "esei4.com",
"endpoint": "/esei4"
}'
```
#### Sample Response

```json
{
    "new_car": {
        "endpoint": "/esei4",
        "id": 13,
        "image_url": "esei4.com",
        "name": "E Sei4"
    },
    "success": true
}
```

### PATCH /cars/car_id

Edits existing car by id. Requires **patch:cars** permission. Replace **token** with valid Bearer token. **car_id** must be a integer and existing car_id.

#### Sample Request

```bash
curl --location --request PATCH 'localhost:5000/cars/6' \
--header 'Authorization: Bearer token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Sei8",
    "image_url": "sei8.com",
    "endpoint": "/sei8"
}'
```

#### Sample Response
```json
{
    "car": [
        {
            "endpoint": "/sei8",
            "id": 6,
            "image_url": "sei8.com",
            "name": "Sei8"
        }
    ],
    "success": true
}
```

### DELETE /cars/car_id

Deletes existing car by id. Requires **delete:cars** permission. Replace **token** with valid Bearer token. **car_id** must be a integer and existing car_id.

#### Sample Request
```bash
curl --location --request DELETE 'localhost:5000/cars/6' \
--header 'Authorization: Bearer token'
```

#### Sample Response
```json
{
    "message": "Car successfully deleted",
    "success": true
}
```

### POST /documents

Creates document. Requires **post:documents** permission. Replace **token** with valid Bearer token. **car_id** in body must be an integer and valid car_id.

#### Sample Request

```bash
curl --location --request POST 'localhost:5000/documents' \
--header 'Authorization: Bearer token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Cover",
    "doc_type": "PNG",
    "image_url": "https://PNG.jpg",
    "url": "https://PNG.com",
    "doc_type": "Image",
    "car_id": 10
}'
```
#### Sample Response

```json
{
    "document": {
        "car_id": 10,
        "doc_type": "Image",
        "id": 17,
        "image_url": "https://PNG.jpg",
        "name": "Cover",
        "url": "https://PNG.com"
    },
    "success": true
}
```

### GET /documents

Gets all documents. Requires **get:documents** permission. Replace **token** with valid Bearer token.

#### Sample Request
```bash
curl --location --request GET 'localhost:5000/documents' \
--header 'Authorization: Bearer token'
```

#### Sample Response
```json
{
    "data": [
        {
            "car_id": 7,
            "doc_type": "PDF",
            "id": 5,
            "image_url": "https://image.jpg",
            "name": "JPG",
            "url": "https://url.com"
        },
        {
            "car_id": 8,
            "doc_type": "PDF",
            "id": 6,
            "image_url": "https://image.jpg",
            "name": "PNG",
            "url": "https://url.com"
        }
    ],
    "success": true
}
```

### PATCH /documents/document_id

Edits existing document by id. Requires **patch:documents** permission. Replace **token** with valid Bearer token. **document_id** must be a integer and existing document_id. **car_id** in request body must be an integer and valid car_id.

#### Sample Request

```bash
curl --location --request PATCH 'localhost:5000/documents/15' \
--header 'Authorization: Bearer token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "car_id": 8,
    "image_url": "https://document.com",
    "name": "PDF",
    "url": "https://twitter.com",
    "doc_type": "JPG"
}'
```

#### Sample Response
```json
{
    "document": {
        "car_id": 8,
        "doc_type": "JPG",
        "id": 15,
        "image_url": "https://document.com",
        "name": "PDF",
        "url": "https://twitter.com"
    },
    "success": true
}
```

### DELETE /documents/document_id

Deletes existing document by id. Requires **delete:documents** permission. Replace **token** with valid Bearer token. **document_id** must be a integer and existing document_id.

#### Sample Request
```bash
curl --location --request DELETE 'localhost:5000/documents/15' \
--header 'Authorization: Bearer token'
```

#### Sample Response
```json
{
    "message": "Document successfully deleted",
    "success": true
}
```

### GET /cars/car_id/documents

Gets all documents by car_id. Requires **get:documents** permission. Replace **token** with valid Bearer token. **car_id** must be a integer and existing car_id.

#### Sample request
```bash
curl --location --request GET 'localhost:5000/cars/7/documents' \
--header 'Authorization: Bearer token'
```

#### Sample response
```json
{
    "documents": [
        {
            "car_id": 7,
            "doc_type": "PDF",
            "id": 5,
            "image_url": "https://image.jpg",
            "name": "JPG",
            "url": "https://url.com"
        }
    ],
    "success": true
}
```

## Error Handling

Errors are returned as a JSON with the following status codes:

#### 404
```json
{
    "message": "Not found",
    "status_code": 404,
    "success": "false"
}
```
#### 401
```json
{
    "message": "Auth error",
    "status_code": 401,
    "success": "false"
}
```
#### 400
```json
{
    "message": "Request error",
    "status_code": 400,
    "success": "false"
}
```
#### 405
```json
{
    "message": "Method not allowed",
    "status_code": 405,
    "success": "false"
}
```



