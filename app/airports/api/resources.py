from flask import current_app
from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import csv
import os
import pika
import json

from ..models import Airport
from .schemas import airport_schema


api = Namespace('airports', description='Airports API')
airport = api.model('Airport', airport_schema)


@api.route('/')
class AirportListResource(Resource):
    '''Shows a list of all airports, and lets you POST to add new airports'''
    @api.doc('list_airports')
    @api.marshal_list_with(airport)
    def get(self):
        '''List all tasks'''
        return Airport.get_all(), 200

    @api.doc('create_airport')
    @api.expect(airport)
    @api.marshal_with(airport, code=201)
    def post(self):
        '''Create a new airport'''
        data = api.payload
        airport_object = Airport(**data)
        airport_object.save()
        return airport_object, 201


@api.route('/<int:id>')
@api.response(404, 'Airport not found')
@api.param('id', 'Airport identifier')
class AirportResource(Resource):
    '''Show a single airport'''
    @api.doc('get_airport')
    @api.marshal_with(airport)
    def get(self, id):
        '''Fetch a given resource'''
        airport_object = Airport.get_by_id(id)
        if airport_object is None:
            api.abort(404, "Airport {} doesn't exist".format(id))
        return airport_object, 200

    @api.doc('delete_airport')
    @api.response(204, 'Airport deleted')
    def delete(self, id):
        '''Delete an airport given its identifier'''
        airport_object = Airport.get_by_id(id)
        Airport.delete(airport_object)
        return '', 204

    @api.doc('update_aiport')
    @api.expect(airport)
    @api.marshal_with(airport, code=201)
    def put(self, id):
        '''Update a task given its identifier'''
        airport_object = Airport.update(id, **api.payload)
        return airport_object, 201


upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@api.route('/upload')
class UploadAirports(Resource):
    @api.doc('upload_csv_file')
    @api.expect(upload_parser)
    @api.expect(airport)
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']

        filename = secure_filename(uploaded_file.filename)
        if uploaded_file:
            uploaded_file.save(os.path.join(current_app.config['UPLOADS'],
                                            filename))

            with open(os.path.join(current_app.config['UPLOADS'],
                                   uploaded_file.filename), 'r') as f:
                data = csv.DictReader(f)
                Airport.save_many(Airport, list(data))
            return '', 201
        return '', 404


@api.route('/add-task/<cmd>')
@api.param('cmd', 'Job to be done')
class CreateTasks(Resource):
    @api.doc('send task to queue')
    @api.expect(airport)
    def post(self, cmd):
        data = dict()
        data['cmd'] = cmd
        data['data'] = api.payload
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST')))
        channel = connection.channel()
        channel.queue_declare(queue='cmd_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='cmd_queue',
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        connection.close()
        return 'Task sent to the worker', 200


@api.route('/webhook')
class Webhook(Resource):
    @api.doc('Receive data from worker')
    @api.expect(airport)
    def post(self):
        data = api.payload
        print("DATA", data)
        return f"Data received {data}", 200
