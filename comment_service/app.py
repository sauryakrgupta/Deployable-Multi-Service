from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(80), nullable=False)

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# Create a comment
@app.route('/comments', methods=['POST'])
@jwt_required()
def create_comment():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_comment = Comment(blog_id=data['blog_id'], content=data['content'], author=current_user)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully!'})

# Get comments for a blog
@app.route('/comments/<int:blog_id>', methods=['GET'])
def get_comments(blog_id):
    comments = Comment.query.filter_by(blog_id=blog_id).all()
    return jsonify([{'id': comment.id, 'content': comment.content, 'author': comment.author} for comment in comments])

if __name__ == '__main__':
    app.run(debug=True, port=5002)
