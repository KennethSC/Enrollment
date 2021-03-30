from application import app, db
from flask import Flask, render_template, request, Response, flash, redirect, url_for, session, jsonify
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from application.course_list import course_list

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if not user:
            flash("Sorry, we could not find an active user with your credntials. Try registering first.", "danger") 
        elif user and not user.get_password(password):
            flash(f"Incorrect password for {user.email}", "danger") 
        elif user and user.get_password(password):
            flash(f"{user.first_name}, you have successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")

    return render_template("login.html", title="Login", form=form, login=True)
    

@app.route('/logout')
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "Spring 2021"
    
    classes = Course.objects.order_by("+courseID")

    return render_template("courses.html", courseData=classes, courses=True, term=term)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
        

    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        flash("You have succesfully registered!", "success") 
        return redirect(url_for('index'))

    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/enrollment", methods=['GET', 'POST'])
def enrollment():
    if not session.get('username'):
        flash("You must be logged in to enroll in classes.", "danger") 
        return redirect(url_for('login'))
        
    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"You are already registered in this course: {courseTitle} ", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You have succesfully enrolled in {courseTitle}!", "success") 

    classes = course_list(user_id)

    return render_template(
        "enrollment.html", 
        enrollment=True, 
        title="Enrollment",
        classes=classes
    )
    

@app.route("/unenroll", methods=['POST'])
def unenroll():
    if not session.get('username'):
        flash("You must be logged in to enroll in classes.", "danger") 
        return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id') 

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            Enrollment.objects(user_id=user_id, courseID=courseID).delete()
            flash(f"You have successfully unenrolled in course: {courseTitle} ", "success")
            
    classes = course_list(user_id)

    return render_template(
        "enrollment.html", 
        enrollment=True, 
        title="Enrollment",
        classes=classes
    )

@app.route("/user")
def user():
    users = User.objects.all()
    return render_template("user.html", users=users)
