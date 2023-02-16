from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'kldjfe98ujsfdlf098ejfds0f9dsjfj'
Bootstrap(app)

all_books = []


class BookForm(FlaskForm):
    title = StringField('Book Name', validators=[DataRequired()])
    author = StringField('Book Author', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Add Book')


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BookForm()
    if form.validate_on_submit():
        print(form.title.data)
        print(form.author.data)
        print(form.rating.data)

    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run(port=8000, debug=True)

