from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def create_app(config_filename='app.config.Config'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_filename) 
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Register routes (we'll import them from routes.py)
    with app.app_context():
        from . import routes
        app.add_url_rule('/', 'index', routes.index, methods=['GET'])
        app.add_url_rule('/books', 'get_books', routes.get_books, methods=['GET'])
        app.add_url_rule('/books/new', 'create_book', routes.create_book, methods=['GET', 'POST'])
        app.add_url_rule('/books/<int:book_id>', 'update_book', routes.update_book, methods=['PUT'])
        app.add_url_rule('/books/<int:book_id>', 'delete_book', routes.delete_book, methods=['DELETE'])
        
        return app