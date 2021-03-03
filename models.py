from datetime import datetime
from config import db, app, ma
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import time

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])

class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    author = db.Column(db.String(32))
    publisher = db.Column(db.String(32))
    description = db.Column(db.String(32))
    amount = db.Column(db.Integer)

#to keep track of book borrowings this class will be used
class Moves(db.Model):
    __tablename__ = "moves"
    move_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    move = db.Column(db.Integer) #0 for borrowing, 1 for returning back
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )    

class UserSchema(ma.SQLAlchemyAutoSchema ):
    class Meta:
        model = User
        sqla_session = db.session
        
class BookSchema(ma.SQLAlchemyAutoSchema ):
    class Meta:
        model = Book
        sqla_session = db.session

class MovesSchema(ma.SQLAlchemyAutoSchema ):
    class Meta:
        model = Moves
        sqla_session = db.session

