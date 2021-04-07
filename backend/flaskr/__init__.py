import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# Return list of question objects as paginated list of dicts
def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    page_questions = [question.format() for question in questions[start:end]]
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
    def get_categories():
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


    # Handle GET requests for questions by category ID
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        page_questions = paginate_questions(request, questions)
        if len(page_questions) > 0:
            return jsonify({
                'success': True,
                'current_category': category_id,
                'questions': page_questions,
                'total_questions': len(questions)
            })
        else:
            abort(404)


    # Handle POST requests for quizzes
    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        category_id = body.get('quiz_category')['id']
        if category_id == "0":
            questions = Question.query.all()
        elif Category.query.get(category_id) is not None:
            questions = Question.query.filter(Question.category == category_id).all()
        else:
            abort(422)
        remaining_questions = [question for question in questions if question.id not in previous_questions]
        random_question = None
        if len(remaining_questions) > 0:
            random_question = random.choice(remaining_questions).format()
        return jsonify({
            'success': True,
            'question': random_question
        })


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
        }), 500

    return app
