from flask import Flask, render_template, request
import database as db

app = Flask(__name__)
app.secret_key = b"ooh what a secure key we have secretly here in version control"
db.init_app(app)


@app.route("/")
def home():
    return render_template("google-vs-custom.html", request={"request": request})


if __name__ == "__main__":
    app.run(debug=True)
