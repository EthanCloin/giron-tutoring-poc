from flask import Flask, render_template, request
import database

app = Flask(__name__)
app.secret_key = b"ooh what a secure key we have secretly here in version control"


@app.route("/")
def home():
    return render_template("google-vs-custom.html", request={"request": request})


if __name__ == "__main__":
    app.run(debug=True)
