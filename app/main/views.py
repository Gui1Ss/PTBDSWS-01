from datetime import datetime

from flask import (
    Response, abort, current_app, flash, redirect,
    render_template, request, session, url_for
)

from . import main
from .forms import CadastroForm, LoginForm, NameForm
from .. import db
from ..email import corpo_novo_usuario, send_email
from ..models import Role, User


@main.route("/", methods=["GET", "POST"])
def index():

    form = CadastroForm()

    if form.validate_on_submit():

        nome = form.name.data

        usuario = User.query.filter_by(username=nome).first()

        if usuario is None:
            papel = Role.query.filter_by(name=form.role.data).first()
            usuario = User(username=nome, role=papel)
            db.session.add(usuario)
            db.session.commit()

            corpo = corpo_novo_usuario(usuario)
            destinatarios = [
                current_app.config["FLASKY_ADMIN"],
                current_app.config["FLASKY_GRUPO"],
            ]

            email_informado = form.email.data.strip()
            if email_informado.lower() not in (
                d.lower() for d in destinatarios
            ):
                destinatarios.append(email_informado)

            # Um envio por destinatário: se um for recusado, os outros saem
            for destinatario in destinatarios:
                if send_email([destinatario], "Novo usuário cadastrado", corpo):
                    flash(f"E-mail enviado para {destinatario}.")
                else:
                    flash(
                        f"Não foi possível enviar o e-mail para {destinatario}."
                    )

        session["name"] = nome

        return redirect(url_for("main.index"))

    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        usuarios=User.query.all(),
        papeis=Role.query.all(),
    )


@main.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for("main.login"))

    agora = datetime.now()

    return render_template(
        "login.html",
        form=form,
        data_hora=agora.strftime(
            "A data e hora local é %d/%m/%Y às %H:%M."
        ),
        tempo="Atualizado há poucos segundos.",
    )


@main.route("/user/<nome>/<prontuario>/<curso>")
def usuario(nome, prontuario, curso):

    return render_template(
        "identificacao.html",
        nome=nome,
        prontuario=prontuario,
        curso=curso,
    )


@main.route("/contextorequisicao/<nome>")
def contexto_requisicao(nome):

    return render_template(
        "contexto.html",
        nome=nome,
        navegador=request.headers.get("User-Agent"),
        ip=request.remote_addr,
        host=request.host,
    )


@main.route("/codigostatusdiferente")
def codigo_status_diferente():

    return "Requisição inválida!", 400


@main.route("/objetoresposta")
def objeto_resposta():

    return Response(
        "Resposta criada usando o objeto Response.",
        status=200,
        mimetype="text/html",
    )


@main.route("/redirecionamento")
def redirecionamento():

    return redirect("/")


@main.route("/abortar")
def abortar():

    abort(404)


@main.route("/form/<nome>", methods=["GET", "POST"])
def form(nome):

    form = NameForm()

    if form.validate_on_submit():

        session["name"] = form.name.data

        return redirect(
            url_for("main.form", nome=nome)
        )

    return render_template(
        "form.html",
        form=form,
        name=session.get("name"),
        nome=nome,
    )
