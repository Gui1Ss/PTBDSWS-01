from flask import (
    Flask, request, Response, redirect, abort,
    render_template, session, url_for
)
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


# ==========================================
# Configuração da aplicação
# ==========================================

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = "Chave forte"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(basedir, "data.sqlite")
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# ==========================================
# Banco de dados
# ==========================================

db = SQLAlchemy(app)

# Flask-Migrate
migrate = Migrate(app, db)


# ==========================================
# Formulários
# ==========================================

class NameForm(FlaskForm):
    name = StringField(
        "What is your name?",
        validators=[DataRequired()]
    )

    submit = SubmitField("Submit")


class HomeForm(FlaskForm):
    nome = StringField(
        "Informe o seu nome",
        validators=[DataRequired()]
    )

    sobrenome = StringField(
        "Informe o seu sobrenome",
        validators=[DataRequired()]
    )

    instituicao = StringField(
        "Informe a sua Instituição de ensino",
        validators=[DataRequired()]
    )

    disciplina = SelectField(
        "Informe a sua disciplina",
        choices=[
            ("dswa5", "DSWA5"),
            ("dwba4", "DWBA4"),
            ("GPSA5", "Gestão de Projetos"),
        ],
    )

    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    usuario = StringField(
        "Usuário ou e-mail",
        validators=[DataRequired()]
    )

    senha = PasswordField(
        "Informe a sua senha",
        validators=[DataRequired()]
    )

    submit = SubmitField("Enviar")


# ==========================================
# Modelos do banco
# ==========================================

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(64),
        unique=True
    )

    users = db.relationship(
        "User",
        backref="role",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Role '{self.name}'>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(64),
        unique=True,
        index=True,
        nullable=False
    )

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id")
    )

    def __repr__(self):
        return f"<User '{self.username}'>"


# ==========================================
# Contexto automático do Flask Shell
# ==========================================

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Role": Role
    }


# ==========================================
# Rotas
# ==========================================

@app.route("/", methods=["GET", "POST"])
def index():

    form = HomeForm()

    if form.validate_on_submit():

        session["nome"] = form.nome.data
        session["sobrenome"] = form.sobrenome.data
        session["instituicao"] = form.instituicao.data
        session["disciplina"] = form.disciplina.data

        return redirect(url_for("index"))

    agora = datetime.now()

    return render_template(
        "index.html",
        form=form,
        nome=session.get("nome"),
        instituicao=session.get("instituicao"),
        disciplina=session.get("disciplina"),
        ip=session.get("ip"),
        host=session.get("host"),
        data_hora=agora.strftime(
            "A data e hora local é %d/%m/%Y às %H:%M."
        ),
        tempo="Atualizado há poucos segundos.",
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for("login"))

    agora = datetime.now()

    return render_template(
        "login.html",
        form=form,
        data_hora=agora.strftime(
            "A data e hora local é %d/%m/%Y às %H:%M."
        ),
        tempo="Atualizado há poucos segundos.",
    )


@app.route("/user/<nome>/<prontuario>/<curso>")
def usuario(nome, prontuario, curso):

    return render_template(
        "identificacao.html",
        nome=nome,
        prontuario=prontuario,
        curso=curso,
    )


@app.route("/contextorequisicao/<nome>")
def contexto_requisicao(nome):

    return render_template(
        "contexto.html",
        nome=nome,
        navegador=request.headers.get("User-Agent"),
        ip=request.remote_addr,
        host=request.host,
    )


@app.route("/codigostatusdiferente")
def codigo_status_diferente():

    return "Requisição inválida!", 400


@app.route("/objetoresposta")
def objeto_resposta():

    return Response(
        "Resposta criada usando o objeto Response.",
        status=200,
        mimetype="text/html",
    )


@app.route("/redirecionamento")
def redirecionamento():

    return redirect("/")


@app.route("/abortar")
def abortar():

    abort(404)


@app.route("/form/<nome>", methods=["GET", "POST"])
def form(nome):

    form = NameForm()

    if form.validate_on_submit():

        session["name"] = form.name.data

        return redirect(
            url_for("form", nome=nome)
        )

    return render_template(
        "form.html",
        form=form,
        name=session.get("name"),
        nome=nome,
    )


# ==========================================
# Execução
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
