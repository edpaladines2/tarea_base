import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "studentdb.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Student(db.Model):
    """
    """
    ced = db.Column(db.String(10), unique=True, nullable=False,primary_key=True)
    name = db.Column(db.String(45), unique=False, nullable=False)
    last = db.Column(db.String(45), unique= False, nullable=False)

    def __repr__(self):
        return "<Name: {}>".format(self.name)
        
# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        try:
            print(request.form)
            est = Student(ced=request.form.get("newced"), name=request.form.get("newname"), last=request.form.get("newlast"))
            db.session.add(est)
            db.session.commit()
        except Exception as e:
            print("No se puede añadir")
            print(e)
    
    stu = Student.query.all()
    return render_template("home.html", stu=stu)
    # return render_template("home.html")
    
@app.route("/update", methods=["POST"])
def update():
    try:
        c = request.form.get("newced")
        newname = request.form.get("newname")
        lastname = request.form.get("newlast")
        est = Student.query.get(c)
        est.name = newname
        est.last = lastname
        db.session.commit()
    except Exception as e:
        print("No se puede modificar")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    c = request.form.get("newced")
    est = Student.query.get(c)
    db.session.delete(est)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



