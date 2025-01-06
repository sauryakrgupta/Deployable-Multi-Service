from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Blog model
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(80), nullable=False)

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

# Create a new blog
@app.route('/blogs', methods=['POST'])
@jwt_required()
def create_blog():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_blog = Blog(title=data['title'], content=data['content'], author=current_user)
    db.session.add(new_blog)
    db.session.commit()
    return jsonify({'message': 'Blog created successfully!'})

# Get all blogs
@app.route('/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return jsonify([{'id': blog.id, 'title': blog.title, 'content': blog.content, 'author': blog.author} for blog in blogs])

# Get a specific blog
@app.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog:
        return jsonify({'id': blog.id, 'title': blog.title, 'content': blog.content, 'author': blog.author})
    return jsonify({'message': 'Blog not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
