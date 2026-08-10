from flask import Flask, request, Response, redirect, abort, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    agora = datetime.now()
    data_hora = agora.strftime("A data e hora local é %d/%m/%Y às %H:%M.")
    tempo = "Atualizado há poucos segundos."
    return render_template("index.html", data_hora=data_hora, tempo=tempo)

@app.route("/user/<nome>/<prontuario>/<curso>")
def usuario(nome, prontuario, curso):
    return render_template("identificacao.html", nome=nome, prontuario=prontuario, curso=curso)

@app.route("/contextorequisicao/<nome>")
def contexto_requisicao(nome):
    return render_template(
        "contexto.html",
        nome=nome,
        navegador=request.headers.get("User-Agent"),
        ip=request.remote_addr,
        host=request.host
    )

@app.route("/codigostatusdiferente")
def codigo_status_diferente():
    return "Requisição inválida!", 400

@app.route("/objetoresposta")
def objeto_resposta():
    return Response(
        "Resposta criada usando o objeto Response.",
        status=200,
        mimetype="text/html"
    )

@app.route("/redirecionamento")
def redirecionamento():
    return redirect("/")

@app.route("/abortar")
def abortar():
    abort(404)

if __name__ == "__main__":
    app.run(debug=True)
