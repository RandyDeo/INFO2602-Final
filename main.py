import json
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required, UserMixin
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, User, Post #add application models

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
#   app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) # uncomment if using flsk jwt
  CORS(app)
  login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here (if using flask JWT)'''
# def authenticate(uname, password):
#   pass

# #Payload is a dictionary which is passed to the function by Flask JWT
# def identity(payload):
#   pass

# jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/app')
@login_required
def client_app():
    asgs = Post.query.all()
    users = User.query.all()
    return render_template('app.html', allPosts=asgs, owner=users)

@app.route('/app', methods=(["POST"]))
@login_required
def submitPost():
    if request.method == "POST":
        postData=request.form.to_dict()

        if postData["textBox"] == "":
            flash("Please enter message to post!")
            return redirect('/app')

        newPost = Post(userid=current_user.id, text=postData["textBox"])
        db.session.add(newPost)
        db.session.commit()

    return redirect('/app')

@app.route("/app/<id>", methods=(["GET"])) #This was referenced from Extra Lab
@login_required
def deletePost(id):
    currPost = Post.query.filter_by(userid=current_user.id, id=id).first()
    if currPost == None:
        flash ("Invalid ID or You did not Post this!")
        return redirect('/app')
    db.session.delete(currPost)
    db.session.commit()
    return redirect('/app')

''' LIKE AND DISLIKE ROUTES DON'T WORK

@app.route("/like/<id>", methods=(["GET"]))
@login_required
def likePost(id):
    addLike = UserReact(userid=current_user.id, postid=id, react=true)
    db.session.add(addLike)
    db.session.commit()
    return redirect('/app')
    
@app.route("/dislike/<id>", methods=(["GET"]))
@login_required
def likePost(id):
    addLike = UserReact(userid=current_user.id, postid=id, react=faLse)
    db.session.add(addLike)
    db.session.commit()
    return redirect('/app')
'''

@app.route("/login", methods=(['GET', 'POST'])) #This was referenced from my group Project and Lab 5
def login():
    if request.method == 'GET':
        return render_template('index.html')
        
    elif request.method == 'POST':
        userInfo = request.form.to_dict()
        username = userInfo["user"]
        password = userInfo["password"]
        currUser = User.query.filter_by(username=username).first()
        if currUser and currUser.check_password(password):
            login_user(currUser)
            return redirect('/app')
        if currUser is None:
            flash("Invalid Username or Password.")
            return redirect("/")

@app.route("/logout", methods=(['GET']))
@login_required
def logout():
    logout
    return redirect("/")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
