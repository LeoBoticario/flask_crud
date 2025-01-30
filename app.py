from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db' # This will create a 'books.db' file in your project folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To turn off a feature we don't need

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Book {self.title}>'

# create the database tables
with app.app_context():
    db.create_all()

# Create a book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json() # get JSON data from the request
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'id': new_book.id, 'title': new_book.title, 'author': new_book.author}), 201 # return the created book and a http status 201 (created)

# Read all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all() # Get all books from the database
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author} for book in books]), 200 # return the list of books

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get(book_id) # find the book by its id
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    book.title = data['title']
    book.author = data['author']
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author}), 200

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id) # find the book by its id
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)