from flask import flash, redirect, render_template, request, url_for
from flask_login import (
    current_user, login_required, login_user, logout_user
)

from . import auth
from .. import db
from ..email import send_email_template
from ..models import User
from .forms import (
    ChangeEmailForm, ChangePasswordForm, LoginForm,
    PasswordResetForm, PasswordResetRequestForm, RegistrationForm
)


def _link(texto, url):
    return f'<p>{texto} <a href="{url}">clique aqui</a></p>'


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != "auth" \
            and request.endpoint != "static":
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/") \
                    or next.startswith("//"):
                next = url_for("main.index")
            return redirect(next)
        flash("E-mail ou senha inválidos.")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email_template(user.email, "Confirme sua conta",
                            "auth/email/confirm", user=user, token=token)
        flash("Um e-mail de confirmação foi enviado para você.")
        flash(_link("Para confirmar sua conta",
                    url_for("auth.confirm", token=token, _external=True)))
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        db.session.commit()
        flash("Conta confirmada. Obrigado!")
    else:
        flash("O link de confirmação é inválido ou expirou.")
    return redirect(url_for("main.index"))


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email_template(current_user.email, "Confirme sua conta",
                        "auth/email/confirm", user=current_user, token=token)
    flash("Um novo e-mail de confirmação foi enviado para você.")
    flash(_link("Para confirmar sua conta",
                url_for("auth.confirm", token=token, _external=True)))
    return redirect(url_for("auth.unconfirmed"))


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Sua senha foi atualizada.")
            return redirect(url_for("main.index"))
        flash("Senha inválida.")
    return render_template("auth/change_password.html", form=form)


@auth.route("/reset", methods=["GET", "POST"])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        flash("Um e-mail com instruções para redefinir sua senha "
              "foi enviado para você.")
        if user:
            token = user.generate_reset_token()
            send_email_template(user.email, "Redefinir sua senha",
                                "auth/email/reset_password",
                                user=user, token=token)
            flash(_link("Para redefinir sua senha",
                        url_for("auth.password_reset", token=token,
                                _external=True)))
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)


@auth.route("/reset/<token>", methods=["GET", "POST"])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash("Sua senha foi atualizada.")
            return redirect(url_for("auth.login"))
        flash("O link de redefinição é inválido ou expirou.")
        return redirect(url_for("main.index"))
    return render_template("auth/reset_password.html", form=form)


@auth.route("/change_email", methods=["GET", "POST"])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email_template(new_email, "Confirme seu novo e-mail",
                                "auth/email/change_email",
                                user=current_user, token=token)
            flash("Um e-mail com instruções para confirmar seu novo "
                  "endereço foi enviado para você.")
            flash(_link("Para confirmar seu novo e-mail",
                        url_for("auth.change_email", token=token,
                                _external=True)))
            return redirect(url_for("auth.change_email_request"))
        flash("E-mail ou senha inválidos.")
    return render_template("auth/change_email.html", form=form)


@auth.route("/change_email/<token>")
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash("Seu endereço de e-mail foi atualizado.")
    else:
        flash("Solicitação inválida.")
    return redirect(url_for("main.index"))
