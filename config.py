import os

DATABASE_URL='postgres://jeffreysorsby@localhost:5432/jac_home'
AUTH0_DOMAIN='jacmx.us.auth0.com'
ALGORITHMS=['RS256']
API_AUDIENCE='jac-home'
FLASK_ENV='development'
SECRET_KEY=os.urandom(32)