from flask import Flask
from catalogo import bp as catalogo_bp
from auth import bp as auth_bp
from usuarios import bp as usuarios_bp
from reportes import bp as reportes_bp
from inicio import pagina_inicio

app = Flask(__name__)
app.secret_key = "cambiar-en-produccion"
app.register_blueprint(catalogo_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(reportes_bp)


@app.route("/")
def index():
    return pagina_inicio()


if __name__ == "__main__":
    app.run(debug=True)
