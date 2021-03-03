Directory structure and files

bookA.py		-> it is the main program
books.db		-> internal sql based db
models.py		-> contains classes
config.py		-> contains general parameters like db, auth
build_database.py	-> creates the database tables and inserts 3 sample books in the table



endpoints and used methods

endpoint		method

api/users		->GET,POST	-> displays users and creates a new user
api/users/[int]		->GET		-> displays the user with that <int> id
api/books		->GET,POST	-> displays list of books and creates a new book
api/books/[int]		->GET,PUT,POST	-> GET(displays a single book),PUT(borrows a book),POST(returns a book)
api/logs		->GET		-> displays logs of books with book id and a movement id(0 for borrowing,1 for returning) and time



used libraries

os
connexion
flask_sqlalchemy
flask_marshmallow
flask_httpauth
datetime
werkzeug.security
jwt
time
flask


For program execution:

1- 	Program needs authentication in order to execute, all endpoints are normally protected with authentication, but to test the program they are initially disabled.
	"@app.route('/api/users/<int:id>')
	#@auth.login_required"
	in the example above @auth.login_required is commented and thus has no effect,they should be turned on manually to test the authentication system

2-	At the beginning you may want to run build_database.py first so that the database clears itself and begins with 3 sample books

3-	Then you can create a user with POST to endpoint api/users via Postman or another program uses Json format, to create user ["username": "name", "password": "pass"} json is used

4-	To create a book POST method to endpoint api/books is used, book attributes are : title,author,publisher and description. Each book is created with amount=1, and amount attribute is used
	to see if that book is borrowed, if 0 it means borrowed, when it is returned amount becomes 1 again

5-	To borrow a book PUT method to the endpoint api/books/[book id] is used, if it is already borrowed it gives a warning, 
	if borrowing is successful it creates a log in moves table with book id and move atribute 0 indicating it is an borrowing process

6-	To return back a book POST method to the endpoint api/books/[book id] is used, if successfull it creates a log in moves table with book id and move attribute =1 indicating it is a returning	

7-	To reach the logs GET methot to endpoint api/logs is used