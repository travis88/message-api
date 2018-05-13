from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from models import db, Category, CategorySchema, Message, MessageSchema
from sqlalchemy.exc import SQLAlchemyError
import status


api_bp = Blueprint('api', __name__)
category_schema = CategorySchema()
message_schema = MessageSchema()
api = Api(api_bp)


class MessageResource(Resource):
    """Ресурс сообщение"""

    def get(self, id):
        """Возвращает сообщение"""
        message = Message.query.get_or_404(id)
        result = message_schema.dump(message).data
        return result

    def patch(self, id):
        """Обновляет сообщение"""
        message = Message.query.get_or_404(id)
        message_dict = request.get_json(force=True)
        if 'message' in message_dict:
            message.message = message_dict['message']
        if 'duration' in message_dict:
            message.duration = message_dict['duration']
        if 'printed_times' in message_dict:
            message.printed_times = message_dict['printed_times']
        if 'printed_once' in message_dict:
            message.printed_once = message_dict['printed_once']
        dumped_message, dump_errors = message_schema.dump(message)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = message_schema.validate(dumped_message)
        # errors = message_schema.validate(data)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            message.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error': str(e)})
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        """Удаляет сообщение"""
        message = Message.query.get_or_404(id)
        try:
            delete = message.delete(message)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error': str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class MessageListResource(Resource):
    """Список сообщений"""

    def get(self):
        """Возвращает список сообщений"""
        messages = Message.query.all()
        result = message_schema.dump(messages, many=True).data
        return result

    def post(self):
        """Добавляет новое сообщение"""
        request_dict = request.get_json()
        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = message_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            category_name = request_dict['category']['name']
            category = Category.query.filter_by(name=category_name).first()
            if category is None:
                # create a new category
                category = Category(name=category_name)
                db.session.add(category)
            # now that we are sure we have a category
            # create a new message
            message = Message(message=request_dict['message'],
                              duration=request_dict['duration'],
                              category=category)
            message.add(message)
            query = Message.query.get(message.id)
            result = message_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error': str(e)})
            return resp, status.HTTP_400_BAD_REQUEST


class CategoryResource(Resource):
    """Категория"""

    def get(self, id):
        """Возвращает категорию"""
        category = Category.query.get_or_404(id)
        result = category_schema.dump(category).data
        return result
    
    def patch(self, id):
        """Обновляет категорию"""
        category = Category.query.get_or_404(id)
        category_dict = request.get_json()
        if not category_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = category_schema.validate(category_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if 'name' in category_dict:
                category.name = category_dict['name']
            category.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error': str(e)})
            return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        """Удаляет категорию"""
        category = Category.query.get_or_404(id)
        try:
            category.delete(category)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error': str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED


class CategoryListResource(Resource):
    """Список категорий"""

    def get(self):
        """Возвращает список категорий"""
        categories = Category.query.all()
        result = category_schema.dump(categories, many=True).data
        return result
    
    def post(self):
        """Добавляте категорию"""
        request_dict = request.get_json()
        if not request_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = category_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            category = Category(request_dict['name'])
            category.add(category)
            query = Category.query.get(category.id)
            result = category_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error': str(e)})
            return resp, status.HTTP_400_BAD_REQUEST
