import datetime
from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db 
from models import User , Candidate , Company
import views

auth = Blueprint('auth', __name__)

@auth.route('/login')
def signup():
    return render_template('login.html')

@auth.route('/signup-candidate')
def signup_candidate():
    return render_template('signupcandidate.html')

@auth.route('/signup-candidate', methods=['POST'])
def signup_candidate_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    firstname = request.form.get('firstname')
    middlename = request.form.get('middlename')
    lastname = request.form.get('lastname')
    resume = request.files.get('resume')
    linkedin = request.form.get('linkedin')
    github = request.form.get('github')

    user = User.query.filter_by(username=username).first()

    if user:
        flash('Username already exist.')
        return redirect(url_for('auth.login_candidate'))
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    new_candidate = Candidate(email=email, username=username, password=generate_password_hash(password, method='sha256'), firstname=firstname , middlename=middlename, lastname=lastname , resume=resume, linkedin=linkedin, github=github)

    db.session.add(new_user)
    db.session.add(new_candidate)
    db.session.commit()

    return redirect('app.personality_test')

@auth.route('/signup-company')
def signup_company():
    return render_template('signupcompany.html')

@auth.route('/signup-company', methods =['POST'])
def signup_company_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    companyname = request.form.get('companyname')
    website = request.form.get('website')
    desc = request.form.get('desc')
    founder = request.form.get('founder')
    founded_on = datetime.datetime.strptime(request.form.get('founded_on'), '%Y-%m-%d').date()

    user = User.query.filter_by(username=username).first()

    if user:
        flash('Username already exist.')
        return redirect(url_for('auth.login_candidate'))

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    new_company = Company(email=email, username=username, password=generate_password_hash(password, method='sha256'), companyname=companyname, website=website, desc=desc , founder=founder, founded_on=founded_on)
    
    db.session.add(new_user)
    db.session.add(new_company)
    db.session.commit()
    return redirect('auth.login_company')

@auth.route('/login-candidate')
def login_candidate():
    return render_template('logincandidate.html')

@auth.route('/login-candidate', methods=['POST'])
def login_candidate_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login-candidate'))

    login_user(user, remember=remember)

    return redirect(url_for('app.candidateprofile'))


@auth.route('/login-company')
def login_company():
    return render_template('logincompany.html')

@auth.route('/login-company', methods=['POST'])
def login_company_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login-company'))

    login_user(user, remember=remember)

    return redirect(url_for('app.companyprofile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.home'))
