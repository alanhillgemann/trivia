import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# Return list of question objects as pagated list of dicts
def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in questions]
    page_questions = formatted_questions[start:end]
    return page_questions


# Return categories object as dict
def categories_as_dict(categories):
    categories_as_dict = {}
    for category in categories:
        categories_as_dict[category.id] = category.type
    return categories_as_dict


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set CORS.
    CORS(app, resources={'/': {'origins': '*'}})

    # Set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    # Handle GET requests for categories
    @app.route('/categories')
    def categories():
        categories = Category.query.all()
        if len(categories) > 0:
            return jsonify({
                'success': True,
                'categories': categories_as_dict(categories)
            })
        else:
            abort(404)


    # Handle GET requests for questions
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        page_questions = paginate_questions(request, questions)
        if len(page_questions) > 0:
            categories = Category.query.all()
            return jsonify({
                'success': True,
                'categories': categories_as_dict(categories),
                'questions': page_questions,
                'total_questions': len(questions)
            })
        else:
            abort(404)


    # Handle DELETE requests for questions by question ID
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is not None:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        else:
            abort(404)


    # Handle POST requests for questions
    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        if (body.get('searchTerm')):
            # Return questions by search term
            search_term = body.get('searchTerm')
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            page_questions = paginate_questions(request, questions)
            if (len(page_questions) > 0):
                return jsonify({
                    'success': True,
                    'questions': page_questions,
                    'total_questions': len(questions)
            })
            else:
                abort(404)
        else:
            question = Question(
                question = body.get('question'),
                answer = body.get('answer'),
                difficulty = body.get('difficulty'),
                category = body.get('category')
            )
            if (
                (question.question is None) or
                (question.answer is None) or
                (question.difficulty is None) or
                (question.difficulty not in [1, "1", "2", "3", "4", "5"]) or
                (question.category is None) or
                (Category.query.get(question.category) is None)
            ):
                abort(422)
            question.insert()
            return jsonify({
                'success': True,
                'created': question.id,
            })


    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''


    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''


    # Handle errors
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
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 422

    return app
