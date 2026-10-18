from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField(
        "What is your name?",
        validators=[DataRequired()]
    )

    role = SelectField(
        "Role?:",
        choices=[
            ("Administrator", "Administrator"),
            ("Moderator", "Moderator"),
            ("User", "User"),
        ],
        default="User",
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
