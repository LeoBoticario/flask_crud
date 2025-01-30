from . import db
from .models import Book
from flask import render_template, request, redirect, url_for, jsonify


# @app.route('/')
def index():
    # Render the index.html page
    return render_template('index.html')

# Read all books
# @app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all() # Get all books from the database
    return render_template('books.html', books=books)
    # return jsonify([{'id': book.id, 'title': book.title, 'author': book.author} for book in books]), 200 # return the list of books

# Create a new book (POST)
# @app.route('/books', methods=['POST'])
def create_book():
    if(request.method == 'POST'):
        data = request.get_json() # get JSON data from the request
        new_book = Book(title=request.form['title'], author=request.form['author'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('get_books'))
    return render_template('new_book.html')
    # return jsonify({'id': new_book.id, 'title': new_book.title, 'author': new_book.author}), 201 # return the created book and a http status 201 (created)

# Update a book
# @app.route('/books/<int:book_id>', methods=['PUT'])
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
# @app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id) # find the book by its id
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'}), 200
