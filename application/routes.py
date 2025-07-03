from application import app,api
from flask import render_template,request,redirect,flash,url_for,session,jsonify
from application.models import User,Course,Enrollment
from application.forms import LoginForm,RegisterForm
from flask_restx import Resource

##################################################################
@api.route('/api','/api/')
class GetAndPost(Resource):
    #GET ALL
    def get(self):
        return jsonify(User.objects.all())
    
    #POST
    def post(self):
        data=api.payload
        user=User(user_id=data['user_id'],email=data['email'],first_name=data['first_name'],last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))
    
@api.route('/api/<idx>')
class GetUpdateDelete(Resource):
    #GET 1 (idx)
    def get(self,idx):
        return jsonify(User.objects.all(user_id=idx))
    
    #PUT
    def put(self,idx):
        data=api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))
    
    #DELETE
    def delete(self,idx):
        User.objects(user_id=idx).delete()
        return jsonify("User is deleted!")

##################################################################







@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html",index=True)

@app.route("/login",methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for("index"))

    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data

        user=User.objects(email=email).first()

        if user and user.get_password(password):
            flash(f"{user.first_name},You are successfully logged in!","success")
            session['user_id']=user.user_id
            session['username']=user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong","danger")

    return render_template("login.html",title="Login",form=form ,login=True)

@app.route("/courses")
def courses(term=None):
    if term is None:
        term="Spring 2026"
    classes=Course.objects.order_by("courseID")
    return render_template("courses.html",courseData=classes,courses=True,term=term)

@app.route("/register",methods=["GET","POST"])
def register():
    if session.get('username'):
        return redirect(url_for("index"))

    form=RegisterForm()
    if form.validate_on_submit():
        user_id=User.objects.count()
        user_id+=1
        email=form.email.data
        password=form.password.data
        first_name=form.first_name.data
        last_name=form.last_name.data

        user=User(user_id=user_id,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        flash(f"{user.first_name},You are succesfully registered","success")
        return redirect(url_for('index'))
    return render_template("register.html",title="Register",form=form,register=True)

@app.route("/enrollment",methods=["GET","POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for("login"))

    courseID=request.form.get('courseID')
    courseTitle=request.form.get('title')
    user_id=session.get('user_id')

    if courseID:
        if Enrollment.objects(user_id=user_id,courseID=courseID):
            flash(f"OOPS! You are already registered in this course {courseTitle}!","danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id,courseID=courseID).save()
            flash(f"You are successfully enrolled in {courseTitle}!","success")

    classes=list(User.objects.aggregate(*[
    {
        '$lookup': {
            'from': 'enrollment', 
            'localField': 'user_id', 
            'foreignField': 'user_id', 
            'as': 'r1'
        }
    }, {
        '$unwind': {
            'path': '$r1', 
            'includeArrayIndex': 'r1_id', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$lookup': {
            'from': 'course', 
            'localField': 'r1.courseID', 
            'foreignField': 'courseID', 
            'as': 'r2'
        }
    }, {
        '$unwind': {
            'path': '$r2', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'user_id': user_id
        }
    }, {
        '$sort': {
            'courseID': 1
        }
    }
]))
    
    return render_template("enrollment.html",enrollment=True,title="Enrollment",classes=classes)

@app.route("/user")
def user():
    users=User.objects.all()
    return render_template("user.html",users=users)
@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('index'))