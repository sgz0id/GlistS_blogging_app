from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# solving time issue
datetime_today = datetime.now()
date_time_india = datetime_today.astimezone(pytz.timezone('Asia/Calcutta'))

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String, nullable=False, default='unknown')
    dateposted = db.Column(db.DateTime, nullable=False, default=date_time_india)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        new_author = request.form['author']
        new_blog_post = BlogPost(title=new_title, content=new_content, author=new_author)
        db.session.add(new_blog_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_post = BlogPost.query.order_by(BlogPost.dateposted).all()
        return render_template("posts.html", posts=all_post)


@app.route('/posts/delete/<int:id>') #specify the blog post to be deleted by UNIQUE_ID
def delete(id):
    #we will fetch the blog post id and if id is not there we do not want to break with 404
    delete_post = BlogPost.query.get_or_404(id)
    db.session.delete(delete_post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        edit_post.title = request.form['title']
        edit_post.author = request.form['author']
        edit_post.content = request.form['content']
        # after over writing commit the changes to DB
        db.session.commit()
        return redirect('/posts')
    else:
        # render the edit.html
        return render_template('edit.html', post=edit_post)

@app.route('/posts/new', methods=['GET', 'POST'])
def newPost():
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        new_author = request.form['author']
        new_blog_post = BlogPost(title=new_title, content=new_content, author=new_author)
        db.session.add(new_blog_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_post = BlogPost.query.order_by(BlogPost.dateposted).all()
        return render_template("newpost.html")


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts/author', methods=["POST", "GET"])
def authorWise():
    if request.method == "POST":
        author_name = request.form["author"]
        name_wise_post = BlogPost.query.filter_by(author=author_name).all()
        return render_template("author.html", posts=name_wise_post)

