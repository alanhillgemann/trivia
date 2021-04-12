# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## API REFERENCE

### Getting Started

- Base URL: ```http://localhost:5000/```
- Authentication: None

### Error Handling

- HTTP Status Codes:
-- 400 - Bad Request
-- 404 - Not Found
-- 422 - Unprocessable Entity
-- 500 - Internal Server Error

- Response Body:
```
    {
        "error": 400,
        "message": "Bad Request",
        "success": false
    }
```

### Endpoints

### GET '/categories'
Returns all categories
- Path Parameters: None
- Request Parameters: None
- Query String Parameters: None
- CURL: ```curl http://localhost:5000/categories```
- Response Body:
```
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "success": true
    }
```

### GET '/categories/:category_id/questions'
Returns all questions and total for a category
- Path Parameters: ```category_id (integer)```
- Request Parameters: None
- Query String Parameters: None
- CURL: ```curl http://localhost:5000/categories/1/questions```
- Response Body:
```
    {
        "current_category": 1,
        "questions": [
            {
                "answer": "Answer",
                "category": 1,
                "difficulty": 1,
                "id": 1,
                "question": "Question"
            }
        ],
        "success": true,
        "total_questions": 1
    }
```

### GET '/questions'
Returns all categories, 10 questions per page and total
Defaults to page 1 when query string parameter is missing
- Path Parameters: None
- Query String Parameters: ```page (integer)```
- Request Parameters: None
- CURL: ```curl http://localhost:5000/questions?page=1```
- Response Body:
```
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "questions": [
            {
                "answer": "Answer",
                "category": 1,
                "difficulty": 1,
                "id": 1,
                "question": "Question"
            }
        ],
        "success": true,
        "total_questions": 19
    }
```

### POST '/questions'
Creates a new question and returns the ID
Alternatively returns all questions and total for a search term
- Path Parameters: None
- Query String Parameters: None
- Request Parameters:
```
    answer (string)
    category (integer)
    difficulty (integer)
    question (string)

    Alternatively:
    searchTerm (string)
```
- CURL:
```
    curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"answer": "answer", "category": "1", "difficulty": "1", "question": "question"}'

    Alternatively:
    curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "a"}'
```
- Response Body:
```
    {
        "created": 24,
        "success": true
    }

    Alternatively:
    {
        "questions": [
            {
                "answer": "Answer",
                "category": 1,
                "difficulty": 1,
                "id": 1,
                "question": "Question"
            }
        ],
        "success": true,
        "total_questions": 1
    }
```

### DELETE '/questions/:question_id'
Deletes a question and returns the ID
- Path Parameters: question_id (int)
- Query String Parameters: None
- Request Parameters: None
- CURL: ```curl http://localhost:5000/questions/1 -X DELETE```
- Response Body:
```
    {
        "deleted": 1,
        "success": true
    }
```

POST '/quizzes'
Returns a random unanswered question for one or all categories
- Path Parameters: None
- Query String Parameters: None
- Request Parameters:
```
    previous_questions (array of question_ids)
    quiz_category (object)
        id (integer, 0 = all categories)
```
- CURL:
```
    curl http://localhost:5000/quizzes -X POST /
    -H "Content-Type: application/json" /
    -d '{"previous_questions": [2], "quiz_category": {"id": 1}}'
```
- Response Body:
```
    {
        "question": {
            "answer": "Answer",
            "category": 1,
            "difficulty": 1,
            "id": 1,
            "question": "Question"
        },
        "success": true
    }
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```