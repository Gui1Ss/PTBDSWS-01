from flask import Flask, request, Response, redirect, abort, render_template, session, url_for
#from flask import Flask, render_template, session, redirect, url_for
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField(
        'What is your name?',
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Chave forte'


@app.route("/")
def index():
    agora = datetime.now()
    data_hora = agora.strftime(
        "A data e hora local é %d/%m/%Y às %H:%M."
    )
    tempo = "Atualizado há poucos segundos."

    return render_template(
        "index.html",
        data_hora=data_hora,
        tempo=tempo
    )


@app.route("/user/<nome>/<prontuario>/<curso>")
def usuario(nome, prontuario, curso):
    return render_template(
        "identificacao.html",
        nome=nome,
        prontuario=prontuario,
        curso=curso
    )


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



@app.route('/form/<nome>', methods=['GET', 'POST'])
def form(nome):
  form = NameForm()
  if form.validate_on_submit():
    session['name'] = form.name.data
    return redirect(url_for('form'))
  return render_template('form.html', form=form, name=session.get('name'), nome=nome)




if __name__ == "__main__":
    app.run(debug=True)