from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="./templates")

username = 'root'#nome do seu usuario mysql
senha = '532637'#senha do seu usuario mysql
server= 'localhost'#servidor sendo usado
db = 'my_flask'#nome do seu banco de dados

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{senha}@{server}/{db}'

db = SQLAlchemy(app)

class Funcionario(db.Model):
    __tablename__ ='funcionario'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")

        dados = Funcionario(email=email , nome=nome)
        db.session.add(dados)
        db.session.commit()
        return redirect(url_for('lista'))

    return render_template("lista.html")


@app.route("/lista")
def lista():
    funcionarios = Funcionario.query.all()
    return render_template("lista.html", funcionarios=funcionarios)

@app.route("/<int:_id>/excluir")
def excluir(_id):
    user = Funcionario.query.filter_by(_id=_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('lista'))


@app.route("/<int:_id>/atualizar", methods=['GET', 'POST'])
def atualizar(_id):
    funcionario = Funcionario.query.filter_by(_id=_id).first()
    if request.method == 'POST':
        nome = request.form.get("nome")
        email = request.form.get("email")

        Funcionario.query.filter_by(_id=_id).update({"nome": nome,
                                                     "email": email})
        db.session.commit()
        return redirect(url_for('lista'))

    return render_template("atualizar.html", funcionario=funcionario)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)