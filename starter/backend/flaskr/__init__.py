import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={"r/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add("Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = {category.id: category.type for category in Category.query.all()}

        return jsonify({"success": True, "categories": categories}), 200

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/questions", methods=["GET"])
    def get_questions():
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return (
            jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection)
                }
            ),
            200,
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<question_id>", methods=['DELETE'])
    def delete_question(question_id):
        question_data = Question.query.get(question_id)
        if question_data:
            Question.delete(question_data)
            result = {
                "success": True,
            }
            return jsonify(result), 200
        abort(404)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=["POST"])
    def create_question():
        data = request.get_json()
        question = (data.get("question"),)
        answer = (data.get("answer"),)
        category = (data.get("category"),)
        difficulty = data.get("difficulty")

        if not(question and answer and category and difficulty):
            abort(400)

        try:
            question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty,
            )
            question.insert()
        except BaseException:
            abort(400)

        return jsonify({"success": True, "question": question.format()}), 201

    """
    @TODO
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions/search", methods=["POST"])
    def search_question():
        data = request.get_json()
        search_term = data.get("searchTerm")
        search_results = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")
        ).all()
        questions = paginate_questions(request, search_results)
        num_of_questions = len(questions)

        if num_of_questions == 0:
            abort(404)

        return (
            jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": num_of_questions,
                    "current_category": None,
                }
            ),
            200,
        )

    """
    @TODO:
    Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/api/categories/<int:category_id>/questions', methods=["GET"])
    def get_questions_by_category(category_id):
        """Get questions based on category"""
        selection = Question.query.filter_by(category=category_id).all()
        questions = paginate_questions(request, selection)
        num_of_questions = len(selection)

        if num_of_questions == 0:
            abort(404)

        return (
            jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": num_of_questions,
                    "current_category": category_id,
                }
            ),
            200,
        )

       


    """
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  """

    @app.route("/quizzes", methods=["POST"])
    def get_quizzes():
        data = request.get_json()
        previous_questions = data.get("previous_questions")
        quiz_category = data.get("quiz_category")
        quiz_category_id = int(quiz_category["id"])

        question = Question.query.filter(
            Question.id.notin_(previous_questions)
        )

        # quiz category id is 0 if All is selected
        if quiz_category_id:
            question = question.filter_by(category=quiz_category_id)

        # show only one question 
        question = question.first().format()

        return jsonify({"success": True, "question": question, }), 200
        abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {"success": False, "error": 400, "message": "Bad Request"}
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Not Found"}),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 405,
                    "message": "Method Not Allowed",
                }
            ),
            405,
        )

    @app.errorhandler(422)
    def uprocessible_entity(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "Unprocessible Entity",
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 500,
                    "message": "Internal Server Error",
                }
            ),
            500,
        )

    return app