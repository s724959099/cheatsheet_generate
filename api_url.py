from flask_cors import CORS
from rest_api import *

restapi = Blueprint('api', __name__)
CORS(restapi)
api = Api(
    restapi, api_version='1.0', title="all topic lodash",
    description=""
)
api.add_resource(TableREST, '/api/table')
