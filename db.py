from flask_sqlalchemy import SQLAlchemy

class data():
    def __init__(self,app) -> None:
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

        with app.app_context():
            db.create_all()

    def abc(self):
        return 