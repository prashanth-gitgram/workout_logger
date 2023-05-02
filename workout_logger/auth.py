from flask import Blueprint,render_template,url_for,request,redirect,flash
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from flask_login import LoginManager,login_user,logout_user,login_required
from . import db

auth= Blueprint('auth',__name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html',title='SignUp')


@auth.route('/signup',methods=['GET','POST'])
def signup_post():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')

    user= User.query.filter_by(email=email).first()
    if user:
        flash('email already registerd !','danger')
        
    else:
        new_user=User(email=email,name=name,password=generate_password_hash(password,method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for Signing Up','success')
    
    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html',title='LogIn')

@auth.route('/login',methods=['GET','POST'])
def login_post():
    email=request.form.get('email')
    password=request.form.get('password')
    

    user= User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password,password):
        flash('Check your email and password!','danger')
        return redirect(url_for('auth.login'))
    
    login_user(user)
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
