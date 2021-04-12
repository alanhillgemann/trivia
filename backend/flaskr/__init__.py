'''
App module
'''

import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(questions):
    '''Return list of question objects as paginated list of dicts'''
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    page_questions = [question.format() for question in questions[start:end]]
    return page_questions


def categories_as_dict(categories):
    '''Return categories object as dict'''
    as_dict = {}
    for category in categories:
        as_dict[category.id] = category.type
    return as_dict


def create_app(test_config=None):
    '''Create and configure the app'''
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        '''Set Access-Control-Allow'''
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS'
        )
        return response

    @app.route('/categories')
    def get_categories():
        '''Handle GET requests for categories'''
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'categories': categories_as_dict(categories)
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        '''Handle GET requests for questions by category ID'''
        questions = Question.query.filter(
            Question.category == category_id).all()
        page_questions = paginate_questions(questions)
        if len(page_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'current_category': category_id,
            'questions': page_questions,
            'total_questions': len(questions)
        })

    @app.route('/questions')
    def get_questions():
        '''Handle GET requests for questions'''
        questions = Question.query.all()
        page_questions = paginate_questions(questions)
        if len(page_questions) == 0:
            abort(404)
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'categories': categories_as_dict(categories),
            'questions': page_questions,
            'total_questions': len(questions)
        })

    @app.route('/questions', methods=['POST'])
    def post_question():
        '''
        Handle POST requests for questions
        Optionally return questions by search term
        '''
        body = request.get_json()
        if not isinstance(body, dict):
            abort(400)
        if 'searchTerm' in body:
            # Return questions by search term
            search_term = body.get('searchTerm')
            if not isinstance(search_term, str):
                abort(422)
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            page_questions = paginate_questions(questions)
            return jsonify({
                'success': True,
                'questions': page_questions,
                'total_questions': len(questions)
            })
        try:
            question = Question(
                question = body.get('question'),
                answer = body.get('answer'),
                difficulty = int(body.get('difficulty')),
                category = int(body.get('category'))
        )
        except (TypeError, ValueError):
            abort(422)
        if (
            not isinstance(question.question, str) or
            question.question in ['', None] or
            not isinstance(question.answer, str) or
            question.answer in ['', None] or
            question.difficulty not in range(1, 6) or
            Category.query.get(question.category) is None
        ):
            abort(422)
        question.insert()
        return jsonify({
            'success': True,
            'created': question.id,
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''Handle DELETE requests for questions by question ID'''
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        question.delete()
        return jsonify({
            'success': True,
            'deleted': question_id
        })

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        '''Handle POST requests for quizzes'''
        body = request.get_json()
        if not isinstance(body, dict):
            abort(400)
        previous_questions = body.get('previous_questions')
        if not isinstance(previous_questions, list):
            abort(422)
        try:
            category_id = int(body.get('quiz_category').get('id'))
        except (TypeError, ValueError):
            abort(422)
        if category_id == 0:
            questions = Question.query.all()
        elif Category.query.get(category_id) is not None:
            questions = Question.query.filter(
                Question.category == category_id).all()
        else:
            abort(422)
        remaining_questions = [question for question in questions \
            if question.id not in previous_questions]
        random_question = None
        if len(remaining_questions) > 0:
            random_question = random.choice(remaining_questions).format()
        return jsonify({
            'success': True,
            'question': random_question
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
