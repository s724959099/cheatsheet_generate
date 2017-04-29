from flask_restful_swagger_2 import Api
from flask_cors import CORS
from rest_api import *


restapi = Blueprint('api', __name__)
CORS(restapi)
api = Api(
    restapi, api_version='1.0', title="all topic lodash",
    description=""
)
api.add_resource(TopicREST, '/api/topic')
api.add_resource(TopicIdREST, '/api/topic/<TopicId>')