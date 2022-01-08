from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)

    #Optional: this will allow each Movie object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


# # CREATE RECORD
# movie_data = Movies(title="Phone Booth", year=2002, description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.", rating=7.3, ranking=10, review="My favourite character was the caller.", image_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")   
# db.session.add(movie_data)
# db.create_all()    
# db.session.commit()

#CREATE UPDATE FORM
class UpdateForm(FlaskForm):
    rating = FloatField('Your Rating out of 10 e.g. 7.5)', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')

#CREATE ADD FORM
class AddForm(FlaskForm):
    add = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    #Read all books from the database
    all_movies = db.session.query(Movies).all()
    # print(all_movies)
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = UpdateForm()
    movie_id = request.args.get('id')
    if form.validate_on_submit():
        movie_rating = request.form["rating"]
        movie_review = request.form["review"]
        movie_to_update = Movies.query.get(movie_id)
        movie_to_update.rating = movie_rating
        movie_to_update.review = movie_review
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form)


@app.route("/delete")
def delete():
    #DELETE A PARTICULAR RECORD BY PRIMARY primary_key
    movie_id = request.args.get('id')
    movie_to_delete = Movies.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add")
def add():
    form = AddForm()
    return render_template('add.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
