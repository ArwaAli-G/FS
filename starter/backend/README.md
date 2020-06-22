# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

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

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
GET 'api/categories/<int: category_id>/questions'
POST '/questions'
POST '/questions/search'
POST '/quizzes'
DELETE '/questions'



GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a list of paginated questions, and the total number of questions
- Request Arguments: page, the defualt value is 1
- Returns: A list of questions and the total number of questions. 
{
    "questions":[
        {
          "question": "What is the heaviest organ in the human body?  ",
          "answer": "The liver", 
          "category": 1, 
          "difficulty": 4, 
          "id": 20
        },{...},
    ],
    "total_questions": 20
}
- when no questions are available or invalid page is selected, the following error is generated
{
  "error": 404, 
  "message": "Not Found", 
  "success": false
}

GET 'api/questions/<int:category_id>/questions'
- Get questions that belong to speciic category based on its id
- Returns: if the category does exist, then a list of questions of selected category is generated
 {
    "questions": [{question ..}, {...}],
    "total_questions": num_of_questions,
    "current_category": category_id,
}
- Returns: if the category does not exist, then error 404 is generated
{
  "error": 404,
  "message": "Not Found",
  "success": false
}

POST '/questions'

- It creates a new questiion
- Request Body: question details to be created
  {
      "answer": "King Salman", 
      "category": 3, 
      "difficulty":1, 
      "question": "Who is the king of Saudi Arabia?"
     
  }
- Returns: The newly created question if the information provided are valid
  {
  "question": {
    "answer": "King Salman", 
      "category": 3, 
      "difficulty":1, 
      "question": "Who is the king of Saudi Arabia?"
      "id":21
   },
  "success": True
   }  
- Return: if the information provided are not valid an error is generated
  {
  "error": 400, 
  "message": "Bad Request", 
  "success": false
  }


POST '/question/search'
- Apply a search for questions that contain the search term supplied by the user input
- Request Body: searchTerm {"searchTerm": "search term"}
- Returns: if there exist at least one question that the search term is part of, then a success message is generated
    {
    "questions": [{question ..}],
    "total_questions": "number_of_questions",
    "success": true
    }
- Returns: if the search term is not a part of any question, then 404 error is generated
    {
  "error": 404,
  "message": "Not Found",
  "success": false
    }

POST '/quizzes'
 - Fetches questions to be played as a quiz. quiz for speciic category of for all categories
 - Request Body: 
    - previous_questions constains a list of questions ids for previously attempted questions
    - quiz_category contains the id of the question category for the quiz
    {
        "previous_questions": [],
        "quiz_category": {  "id": "1"}
    }
- Returns a question to play the quiz
   {
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
    },
  "success": true
   }


DELETE '/questions/<int:question_id>'

- Delete a question based on its question id
- Request Arguments: question_id that belongs to the question to be deleted
- Returns: if the question id is valid then a success message is generated , on success
{
  "message": "Question deleted successfully",
  "success": true
}
- Returns: if the question id does not exist, then an error 404 is generated: 
{
  "error": 404,
  "message": "Not Found",
  "success": false
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