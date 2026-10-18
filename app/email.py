import requests
from flask import current_app


def send_email(destinatarios, assunto, corpo):
    config = current_app.config

    try:
        resposta = requests.post(
            config["API_URL"],
            auth=("api", config["API_KEY"]),
            data={
                "from": config["API_FROM"],
                "to": destinatarios,
                "subject": (
                    config["FLASKY_MAIL_SUBJECT_PREFIX"] + " " + assunto
                ),
                "text": corpo,
            },
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
