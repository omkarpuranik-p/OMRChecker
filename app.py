
# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from main import process_dir, args
import werkzeug
import cv2
import numpy

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)


class UploadImage(Resource):
    def post(self):
        test_img = cv2.imdecode(numpy.frombuffer(request.files['file'].read(), numpy.uint8), cv2.IMREAD_GRAYSCALE)
        temp_out = process_dir('inputs', '', args['template'], test_img)
        print("IMAGE RESPONSE>>>>>", temp_out)
        return temp_out


# adding the defined resources along with their corresponding urls
api.add_resource(UploadImage, '/upload')


port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=False)
