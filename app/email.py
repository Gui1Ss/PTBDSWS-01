import requests
from flask import current_app, render_template


def _dica(status, texto):
    """Sugere a correção para os erros mais comuns do Mailgun."""
    texto = texto.lower()
    if "authorized recipients" in texto or "not allowed to send" in texto:
        return (
            " → Conta gratuita (sandbox) do Mailgun: adicione este endereço "
            "em Authorized Recipients no painel do Mailgun e confirme pelo "
            "e-mail que o Mailgun enviar."
        )
    if status == 401:
        return " → Confira a API_KEY no .env."
    if status == 404:
        return " → Confira a API_URL no .env (deve terminar em /messages)."
    return ""


def _enviar(destinatarios, assunto, corpo, html=None):
    """Envia pelo Mailgun. Retorna (ok, motivo_da_falha)."""
    config = current_app.config

    faltando = [
        nome for nome in ("API_URL", "API_KEY", "API_FROM")
        if not config.get(nome)
    ]
    if faltando:
        motivo = "faltam no .env as variáveis " + ", ".join(faltando) + "."
        print(f"[MAIL] {motivo} E-mail não enviado.")
        return False, motivo

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
    except requests.RequestException as erro:
        print(f"[MAIL] erro de conexao: {erro}")
        return False, f"erro de conexão com o Mailgun ({erro})."

    print(
        f"[MAIL] para={destinatarios} status={resposta.status_code} "
        f"resposta={resposta.text}"
    )
    if resposta.ok:
        return True, ""

    try:
        motivo = resposta.json().get("message") or resposta.text
    except (ValueError, AttributeError):
        motivo = resposta.text
    motivo = (motivo or "").strip()[:300]
    return False, (
        f"o Mailgun recusou (status {resposta.status_code}): {motivo}"
        + _dica(resposta.status_code, motivo)
    )


def send_email(destinatarios, assunto, corpo, html=None):
    ok, _ = _enviar(destinatarios, assunto, corpo, html=html)
    return ok


def send_email_template(destinatario, assunto, template, **kwargs):
    """Envia e-mail usando os templates .txt/.html (ex.: auth/email/confirm).

    Retorna (ok, motivo_da_falha).
    """
    corpo = render_template(template + ".txt", **kwargs)
    html = render_template(template + ".html", **kwargs)
    return _enviar([destinatario], assunto, corpo, html=html)


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
