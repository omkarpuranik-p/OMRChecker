
# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from main import process_dir, args

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

class OMRResponse(Resource):

    def get(self):
        temp_out = process_dir('inputs', '', args['template'])
        return temp_out


# adding the defined resources along with their corresponding urls
api.add_resource(OMRResponse, '/')


app.run(debug = True)
