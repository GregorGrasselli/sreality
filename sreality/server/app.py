from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("sreality.settings")

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Flat(db.Model):
    __tablename__ = "flats"

    flat_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image_url = db.Column(db.String)
    original_id = db.Column(db.BigInteger, unique=True, nullable=False)


@app.route("/", methods=["GET"])
def get_flats():
    flats = db.session.execute(
        db.select(Flat.image_url, Flat.title).order_by(Flat.flat_id)
    )
    return render_template("flats.html", flats=flats)


if __name__ == "__main__":
    app.run(debug=True)
