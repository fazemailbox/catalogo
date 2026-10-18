from flask import Flask, redirect, url_for
from catalogo import bp as catalogo_bp

app = Flask(__name__)
app.secret_key = "cambiar-en-produccion"
app.register_blueprint(catalogo_bp)


@app.route("/")
def index():
    return redirect(url_for("catalogo.listar_libros"))


if __name__ == "__main__":
    app.run(debug=True)
