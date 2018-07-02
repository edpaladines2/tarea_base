import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Book(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()
    
    books = Book.query.all()
    return render_template("home.html", books=books)
    # return render_template("home.html")
    
@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    idlibro = request.form.get("idlibro")
    book = Book.query.get(idlibro)
    book.title = newtitle
    db.session.commit()
    return redirect("/")  

@app.route("/delete", methods=["POST"])
def delete():
    idlibro = request.form.get("idlibro")
    book = Book.query.get(idlibro)
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



