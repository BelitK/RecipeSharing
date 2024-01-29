# app.py
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from environs import Env

env = Env()
env.read_env()

DATABASE_URL = env("DATABASE_STRING")
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://belit:12897@173.212.221.185:5555/BelitPersonel"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    recipes = db.relationship("Recipe", back_populates="author")


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.PickleType, nullable=False)
    instructions = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("User", back_populates="recipes")
    timestamp = db.Column(db.Text)


with app.app_context():
    db.create_all()


def check_user(user):
    a = User.query.filter_by(username=user).first()
    if a:
        return a
    return User(username=user)


@app.route("/")
def index():
    result = Recipe.query.all()
    return render_template("index.html", recipes=result)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        title = request.form["title"]
        username = check_user(request.form["username"])
        instructions = request.form["instructions"]
        ingredients = [x for x in request.form.getlist("ingredients")]
        weights = [x for x in request.form.getlist("weight")]
        final = [x for x in zip(ingredients, weights)]

        new_recipe = Recipe(
            title=title,
            instructions=instructions,
            ingredients=final,
            author=username,
            timestamp=datetime.now().strftime("%d-%m-%y"),
        )
        db.session.add(new_recipe)
        # try:
        db.session.commit()
        # except e as Exception

        return redirect(url_for("index"))

    return render_template("add_recipe.html")


@app.route("/recipe/<id>")
def show_recipe(id):
    result = Recipe.query.filter_by(id=id).first()
    return render_template("show_recipe.html", recipe=result)

@app.route("/search", methods=["GET"])
def search():
    if request.method == "GET":
        value = f"%{request.form['search']}%"
        return Recipe.query.filter(Recipe.title.like(value)).first().title
    
    return 'a'
        
@app.route("/delete/<id>")
def delete_recipe(id):
    result = Recipe.query.filter_by(id=id).first()
    if result is None:
        return "No Record"
    db.session.delete(result)
    db.session.commit()
    return f"{id} numbered record has been deleted"

if __name__ == "__main__":
    app.run(debug=True)
