import os
from flask import Flask, abort, request, jsonify, g, url_for, json
from models import User, UserSchema, Book, BookSchema, Moves, MovesSchema
from config import auth, app, db

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/users', methods=['GET','POST'])
@auth.login_required
def handle_users():
    if request.method == 'GET':
        user = User.query.order_by(User.id).all()

        user_schema = UserSchema(many=True)
        data = user_schema.dump(user)
        return jsonify(data)

    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            abort(400)    # missing arguments
        if User.query.filter_by(username=username).first() is not None:
            abort(400)    # existing user
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return (jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
#@auth.login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400, "User not found for Id: {id}".format(id=id),)
    return jsonify({'username': user.username,'password': user.password_hash})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    #return jsonify({'token': token.decode('ascii'), 'duration': 600})
    return jsonify({'token': token, 'duration': 600})


@app.route('/api/books', methods=['GET','POST'])
#@auth.login_required
def handle_books():
    #GET method is used to display all the books
    if request.method == 'GET':
        book = Book.query.order_by(Book.book_id).all()

        book_schema = BookSchema(many=True)
        data = book_schema.dump(book)
        return jsonify(data)

    #POST method is used to add a new book
    elif request.method == 'POST':
        ntitle = request.json.get('title')
        nauthor = request.json.get('author')
        npublisher = request.json.get('publisher')
        ndescription = request.json.get('description')
        namount = 1;

        #We check whether all the book attributes are given or not
        if ntitle is None or nauthor is None or npublisher is None or ndescription is None:
            abort(400, "at least one book argument is missing!") 
        
        #book title must be unique, so we check it
        if Book.query.filter_by(title=ntitle).first() is not None:
            abort(400, "this book already in the system!")  
            
        book = Book(title=ntitle, author=nauthor, publisher=npublisher, description=ndescription, amount=namount)
        db.session.add(book)
        db.session.commit()
        return 'book added'        

@app.route('/api/books/<int:id>', methods=['GET','PUT','POST'])
#@auth.login_required
def handle_book(id):
    # Find the book with the given id
    book = Book.query.get(id)    

    # didn't find that book
    if book is None:
        abort(404, "Book not found for Id: {book_id}".format(book_id=id),)

    #GET method is used to display a single book
    elif request.method == 'GET':
        # Serialize the data for the response
        book_schema = BookSchema()
        data = book_schema.dump(book)
        return data
    
    #PUT method is used for borrowing books
    elif request.method == 'PUT':
        # Is the book already borrowed?
        if (book.amount == 0):
            abort(409, "Book already have been borrowed!",)
        # Otherwise update
        else:
            book.amount = 0
            book.book_id = id
            #db.session.commit()
            
            nmove = Moves(book_id=id, move=0)
            db.session.add(nmove)
            db.session.commit()
            return 'book borrowed'

    #POST method is used to return back a book
    elif request.method == 'POST':
        # Is the book already returned?
        if (book.amount == 1):
            abort(409, "Book already have been returned back!",)
        # Otherwise update
        else:
            book.amount = 1
            book.book_id = id
            #db.session.commit()
            
            nmove = Moves(book_id=id, move=1)
            db.session.add(nmove)
            db.session.commit()
            return 'book returned!'

#used by Librarian to watch the book logs
@app.route('/api/logs', methods=['GET'])
#@auth.login_required
def get_logs():
    #GET method is used to display all the books
    if request.method == 'GET':
        move = Moves.query.order_by(Moves.move_id).all()

        move_schema = MovesSchema(many=True)
        data = move_schema.dump(move)
        return jsonify(data)

if __name__ == '__main__':
    if not os.path.exists('books.db'):
        db.create_all()
    app.run(debug=True)
