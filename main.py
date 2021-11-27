from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json', 'r') as f:
    params = json.load(f)["params"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params['localserver']

db = SQLAlchemy(app)


class Contacts(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ph = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Post(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(12), nullable=False)
    slug = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    owner = db.Column(db.String(20), nullable=False)



@app.route("/")
def home():
    post = Post.query.filter_by().all()[0:6]
    return render_template('index.html', params=params, post=post)


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/add-post", methods = ['GET','POST'])
def AddPost():
    if request.method == "POST":
        title = request.form.get('Title')
        owner = request.form.get('Owner')
        slug = request.form.get('Slug')
        content = request.form.get('Content')
        entry = Post(title=title, owner=owner, slug=slug, date=datetime.now(), content=content)
        db.session.add(entry)
        db.session.commit()
    return render_template('add-post.html', params=params, post=Post)

@app.route("/post/<string:post_slug>/", methods=['GET'])
def post_route(post_slug):
      post = Post.query.filter_by(slug=post_slug).first()
      return render_template('post.html', params=params, post=post)

@app.route("/logout", methods=['GET', 'POST'])
def Logout():
    return redirect('/dashboard')

@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def Delete(sno):
    post = Post.query.filter_by(sno=sno).first()
    db.session.delete(post)
    db.session.commit()
    return  "post number" + post.title + "deleted succesfully"



@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == "POST":
        username = request.form.get('username')
        userpass = request.form.get('password')
        if username == params['admin_user'] and userpass == params['admin_password']:
            post = Post.query.all()
            return render_template('dashboard.html', params=params, post=post)
    else:
        return render_template("login.html", params=params)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():

    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, ph = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

@app.route("/edit/<string:sno>/", methods = ['GET','POST'])
def Edit(sno):
    post = Post.query.filter_by(sno=sno).first()
    if request.method == "POST":
        title = request.form.get('Title')
        owner = request.form.get('Owner')
        slug = request.form.get('Slug')
        content = request.form.get('Content')

        post.title = title
        post.owner = owner
        post.slug = slug
        post.content = content
        db.session.commit()
        return redirect('/edit/'+sno)
    return render_template('edit.html', params=params,post =post )


app.run(debug=True)




