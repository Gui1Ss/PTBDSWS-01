import requests
from flask import current_app, render_template


def send_email(destinatarios, assunto, corpo, html=None):
    config = current_app.config

    if not config.get("API_URL") or not config.get("API_KEY"):
        print("[MAIL] API_URL/API_KEY não configuradas; e-mail não enviado.")
        return False

    dados = {
        "from": config["API_FROM"],
        "to": destinatarios,
        "subject": (
            config["FLASKY_MAIL_SUBJECT_PREFIX"] + " " + assunto
        ),
        "text": corpo,
    }
    if html:
        dados["html"] = html

    try:
        resposta = requests.post(
            config["API_URL"],
            auth=("api", config["API_KEY"]),
            data=dados,
            timeout=10,
        )
        print(
            f"[MAIL] status={resposta.status_code} "
            f"resposta={resposta.text}"
        )
        return resposta.ok
    except requests.RequestException as erro:
        print(f"[MAIL] erro de conexao: {erro}")
        return False


def send_email_template(destinatario, assunto, template, **kwargs):
    """Envia e-mail usando os templates .txt/.html (ex.: auth/email/confirm)."""
    corpo = render_template(template + ".txt", **kwargs)
    html = render_template(template + ".html", **kwargs)
    return send_email([destinatario], assunto, corpo, html=html)


def corpo_novo_usuario(usuario):
    config = current_app.config
    funcao = usuario.role.name if usuario.role else ""

    return f"""
Aluno: {config['FLASKY_NAME']} / Prontuario: {config['FLASKY_PRONTUARIO'].lower()}
Novo usuário cadastrado.

Prontuário: {config['FLASKY_PRONTUARIO']}
Nome do aluno: {config['FLASKY_NAME']}
Usuário cadastrado: {usuario.username}
Função: {funcao}
"""
