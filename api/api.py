import status
from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import Message
from pytz import utc


class MessageManager():
    """Репозиторий для работы с сообщениями"""
    last_id = 0

    def __init__(self):
        self.messages = {}

    def insert_message(self, message):
        """Добавляет сообщение"""
        self.__class__.last_id += 1
        message.id = self.__class__.last_id
        self.messages[self.__class__.last_id] = message

    def get_message(self, id):
        """Возвращает сообщение"""
        return self.messages[id]

    def delete_message(self, id):
        """Удаляет сообщение"""
        del self.messages[id]


message_fields = {
    'id': fields.Integer,
    'uri': fields.Url('message_endpoint'),
    'message': fields.String,
    'duration': fields.Integer,
    'creation_date': fields.DateTime,
    'message_category': fields.String,
    'printed_times': fields.Integer,
    'printed_once': fields.Boolean
}

message_manager = MessageManager()


class Message(Resource):
    """Единичное сообщение"""
    
    def abort_if_message_doesnt_exist(self, id):
        """Отмена если сообщение не существует"""
        if id not in message_manager.messages:
            abort(status.HTTP_404_NOT_FOUND, 
                  message="Message {0} doesn't exist".format(id))
    
    @marshal_with(message_fields)
    def get(self, id):
        """Возвращает сообщение"""
        self.abort_if_message_doesnt_exist(id)
        return message_manager.get_message(id)
    
    def delete(self, id):
        """Удаляет сообщение"""
        self.abort_if_message_doesnt_exist(id)
        message_manager.delete_message(id)
        return '', status.HTTP_204_NO_CONTENT
    
    @marshal_with(message_fields)
    def patch(self, id):
        """Обновляет сообщение"""
        self.abort_if_message_doesnt_exist(id)
        message = message_manager.get_message(id)
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str)
        parser.add_argument('duration', type=int)
        parser.add_argument('printed_times', type=int)
        parser.add_argument('printed_once', type=bool)
        
        args = parser.parse_args()
        if 'message' in args:
            message.message = args['message']
        if 'duration' in args:
            message.duration = args['duration']
        if 'printed_times' in args:
            message.printed_times = args['printed_times']
        if 'printed_once' in args:
            message.printed_once = args['printed_once']
        return message


class MessageList(Resource):
    """Список сообщений"""

    @marshal_with(message_fields)
    def get(self):
        """Возвращает список сообщений"""
        return [v for v in message_manager.messages.values()]
    
    @marshal_with(message_fields)
    def post(self):
        """Добавляет сообщение"""
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, 
                            required=True, help='Message cannot be blank!')
        parser.add_argument('duration', type=int,
                            required=True, help='Duration cannot be blank!')
        parser.add_argument('message_category', type=str,
                            required=True, 
                            help='Message category cannot be blank!')
        args = parser.parse_args()
        message = Message(message=args['message'], 
                               duration=args['duration'],
                               creation_date=datetime.now(utc),
                               message_category=args['message_category'])
        message_manager.insert_message(message)
        return message, status.HTTP_201_CREATED


app = Flask(__name__)
api = Api(app)
api.add_resource(MessageList, '/api/messages/')
api.add_resource(Message, '/api/messages/<int:id>',
                 endpoint='message_endpoint')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
