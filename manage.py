from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy



# Sql bağlantısı yapılan kısım
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/odoo/Desktop/FlaskProject/movieapp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.init_app(app)

# Routing yapılan kısım 
@app.after_request
def add_header(response):
    response.headers['Location'] = '*'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route("/")
def index():
    data = Movie.query.all()   
    
    return render_template("index.html",data = data)

@app.route("/add",methods = ["POST", "GET"])
def addMovie():
    filmName = request.form.get("filmName")
    explanation = request.form.get("explanation")
    image = request.form.get("image")
    homepage = request.form.get("homepage")

    newMovie = Movie(filmName =filmName,explanation =explanation, image =image,homepage =bool(homepage))
    db.session.add(newMovie)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<id>", methods = ["DELETE"])
def delMovie(id):
    delMovie = db.session.get(Movie,id)
    db.session.delete(delMovie)
    db.session.commit()    
    return redirect(url_for("index"))



#Models oluşturulan kısım
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filmName = db.Column(db.String, nullable=False)
    explanation = db.Column(db.String)
    image = db.Column(db.String)
    homepage = db.Column(db.Boolean, default=False, server_default="false")





if __name__=="__main__":
    app.run(debug=True)