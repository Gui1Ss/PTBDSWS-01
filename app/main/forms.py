from flask_wtf import FlaskForm
from wtforms import (
    EmailField, PasswordField, SelectField, StringField, SubmitField
)
from wtforms.validators import DataRequired, Regexp


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


class CadastroForm(NameForm):
    email = EmailField(
        "Qual é o seu email (Envio de notificação do novo usuário)?",
        validators=[
            DataRequired(),
            Regexp(
                r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                message="Informe um e-mail válido.",
            ),
        ],
    )


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
