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
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

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

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    return app
