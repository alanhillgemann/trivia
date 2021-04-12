import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.database_path = 'postgresql://{}/{}'.format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_success_get_categories(self):
        """Test success GET /categories"""
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance((data['categories']), dict)

    def test_success_get_categories_by_id(self):
        """Test success GET /categories/<category_id>/questions"""
        category_id = 1
        response = self.client().get('/categories/'+ str(category_id) +'/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual((data['current_category']), category_id)
        self.assertIsInstance((data['questions']), list)
        self.assertIsInstance(data['total_questions'], int)

    def test_error_get_categories_by_id_not_valid_range(self):
        """Test error GET /categories/<category_id>/questions when category not valid range"""
        response = self.client().get('/categories/999/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_success_get_questions(self):
        """Test success GET /questions"""
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance((data['questions']), list)
        self.assertIsInstance(data['total_questions'], int)

    def test_error_get_questions_none_found(self):
        """Test error GET /questions when none found"""
        response = self.client().get('/questions?page=999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_success_post_questions(self):
        """Test success POST /questions"""
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': '5',
            'category': '6'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['created'], int)

    def test_success_post_questions_for_search_term(self):
        """Test success POST /questions for search term"""
        search_term = {
            'searchTerm': 'Question'
        }
        response = self.client().post('/questions', json=search_term)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance((data['questions']), list)
        self.assertIsInstance(data['total_questions'], int)

    def test_success_post_questions_for_search_term_none_found(self):
        """Test success POST /questions for search term when none found"""
        search_term = {
            'searchTerm': 'QQuestion'
        }
        response = self.client().post('/questions', json=search_term)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual((data['questions']), [])
        self.assertEqual(data['total_questions'], 0)

    def test_success_post_questions_for_blank_search_term(self):
        """Test success POST /questions for blank search term"""
        search_term = {
            'searchTerm': ''
        }
        response = self.client().post('/questions', json=search_term)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance((data['questions']), list)
        self.assertIsInstance(data['total_questions'], int)

    def test_success_post_questions_search_term_not_valid_type(self):
        """Test success POST /questions when search term not valid type"""
        search_term = {
            'searchTerm': []
        }
        response = self.client().post('/questions', json=search_term)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_request_body_missing(self):
        """Test error POST /questions when request body not JSON"""
        response = self.client().post('/questions', json=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # type
    # range
    # blank
    # missing

    # search not str
    # question not str
    # answer not str

    def test_error_post_questions_question_not_valid_type(self):
        """Test error POST /questions when question not valid type"""
        new_question = {
            'question': [],
            'answer': 'answer',
            'difficulty': '1',
            'category': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_question_blank(self):
        """Test error POST /questions when question blank"""
        new_question = {
            'question': '',
            'answer': 'answer',
            'difficulty': '1',
            'category': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_question_missing(self):
        """Test error POST /questions when question missing"""
        new_question = {
            'answer': 'answer',
            'difficulty': '1',
            'category': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_answer_not_valid_type(self):
        """Test error POST /questions when answer not valid type"""
        new_question = {
            'question': 'question',
            'answer': [],
            'difficulty': '1',
            'category': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_answer_blank(self):
        """Test error POST /questions when answer blank"""
        new_question = {
            'question': 'question',
            'answer': '',
            'difficulty': '1',
            'category': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_answer_missing(self):
        """Test error POST /questions when answer missing"""
        new_question = {
            'question': 'question',
            'difficulty': '1',
            'category': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_difficulty_missing(self):
        """Test error POST /questions when difficulty missing"""
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'category': '999'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_difficulty_not_valid_type(self):
        """Test error POST /questions when difficulty not valid type"""
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': [],
            'category': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_difficulty_not_valid_range(self):
        """Test error POST /questions when difficulty not valid range"""
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': '6',
            'category': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_difficulty_blank(self):
        """Test error POST /questions when difficulty blank"""
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': '',
            'category': ''
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_category_not_valid_type(self):
        """Test error POST /questions when category not valid type"""
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': '1',
            'category': []
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_category_not_valid_range(self):
        """Test error POST /questions when category not valid range"""
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': '1',
            'category': '999'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_category_blank(self):
        """Test error POST /questions when category blank"""
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': '1',
            'category': ''
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_questions_category_missing(self):
        """Test error POST /questions when category missing"""
        new_question = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_success_delete_questions_by_id(self):
        """Test success DELETE /questions/<question_id>"""
        last_question = Question.query.order_by(Question.id.desc()).first()
        response = self.client().delete('/questions/' + str(last_question.id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], last_question.id)

    def test_error_delete_questions_by_id_not_valid(self):
        """Test error DELETE /questions/<question_id> when question not valid"""
        response = self.client().delete('/questions/999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_success_post_quizzes_for_all_categories(self):
        """Test success POST /quizzes for all categories"""
        quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'All',
                'id': '0'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['question'], dict)

    def test_success_post_quizzes_for_category(self):
        """Test success POST /quizzes for a category"""
        quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Science',
                'id': '1'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['question'], dict)

    def test_success_post_quizzes_no_questions_remain(self):
        """Test success POST /quizzes when no questions remain"""
        quiz = {
            'previous_questions': [20, 21, 22],
            'quiz_category': {
                'type': 'Science',
                'id': '1'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)

    def test_error_post_quizzes_request_body_missing(self):
        """Test error POST /quizzes when request body not JSON"""
        response = self.client().post('/quizzes', json=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_error_post_quizzes_previous_questions_not_valid_type(self):
        """Test success POST /quizzes when previous questions not valid type"""
        quiz = {
            'previous_questions': {},
            'quiz_category': {
                'type': 'Other',
                'id': '1'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_quizzes_previous_questions_blank(self):
        """Test success POST /quizzes when previous questions blank"""
        quiz = {
            'previous_questions': '',
            'quiz_category': {
                'type': 'Other',
                'id': '1'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_quizzes_previous_questions_missing(self):
        """Test success POST /quizzes when previous questions missing"""
        quiz = {
            'quiz_category': {
                'type': 'Other',
                'id': '1'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_quizzes_category_not_valid_type(self):
        """Test success POST /quizzes when category not valid type"""
        quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Other',
                'id': []
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_quizzes_category_not_valid_range(self):
        """Test success POST /quizzes when category not valid range"""
        quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Other',
                'id': '999'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_quizzes_category_blank(self):
        """Test success POST /quizzes when category blank"""
        quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Other',
                'id': ''
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_error_post_quizzes_category_missing(self):
        """Test success POST /quizzes when category missing"""
        quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Other'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()