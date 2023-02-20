from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'kldjfe98ujsfdlf098ejfds0f9dsjfj'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new_books_collection.db"
db = SQLAlchemy(app)


class BookForm(FlaskForm):
    title = StringField('Book Name', validators=[DataRequired()])
    author = StringField('Book Author', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Add Book')


class EditRatingForm(FlaskForm):
    rating = FloatField(validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Change Rating')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.title


@app.route('/')
def home():
    all_books = db.session.query(Book).all()

    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(title=form.title.data, author=form.author.data, rating=form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html', form=form)


@app.route("/edit_rating/<book_id>", methods=["GET", "POST"])
def edit_rating(book_id):
    form = EditRatingForm()
    book_to_update = db.session.get(Book, book_id)
    if form.validate_on_submit():
        book_to_update.rating = form.rating.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit_rating.html', form=form, book=book_to_update)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
