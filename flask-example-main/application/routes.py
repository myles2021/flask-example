from flask import Flask, render_template, url_for, redirect, request
from application import app, db, bcrypt
from application.models import Post, User
from application.forms import PostForm, RegisterForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def post_create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            first_name=form.first_name.data,
            last_name=form.last_name.data, title=form.title.data, content=form.content.data
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("post.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/post/delete/<id>')
@login_required
def delete_post_by_id(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))
