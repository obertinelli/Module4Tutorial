from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data['publisher']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully!'}), 201


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = [
        {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher} for book in
        books]
    return jsonify(result)


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'book_name': book.book_name,
        'author': book.author,
        'publisher': book.publisher
    })


@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.book_name = data.get('book_name', book.book_name)
    book.author = data.get('author', book.author)
    book.publisher = data.get('publisher', book.publisher)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully!'})


@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
