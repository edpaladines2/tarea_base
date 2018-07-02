import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "estudiantes.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Estudiante(db.Model):
    """
    """
    cedula = db.Column(db.String(10), unique=True, nullable=False, primary_key=True)
    nombre = db.Column(db.String(60), unique=True, nullable=False)
    apellido = db.Column(db.String(60), unique=True, nullable=False)
    def __repr__(self):
        return "<Cedula: {}>".format(self.cedula)

# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        estudiante = Estudiante(ced=request.form.get("txtcedula"), name=request.form.get("txtnombre"), last=request.form.get("txtapelliido"))
        db.session.add(estudiante)
        db.session.commit()
    
    estu = Estudiante.query.all()
    return render_template("home.html", estu=estu)
    # return render_template("home.html")
    
@app.route("/update", methods=["POST"])
def update():
    ced = request.form.get("txtcedula")
    nombre = request.form.get("txtnombre")
    apellido = request.form.get("txtapellido")
    est = Estudiante.query.get(ced)
    est.nombre = nombre
    est.apellido = apellido
    db.session.commit()
    return redirect("/")  

@app.route("/delete", methods=["POST"])
def delete():
    ced = request.form.get("txtcedula")
    est = Estudiante.query.filter_by(ced=ced).first()
    db.session.delete(ced)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



