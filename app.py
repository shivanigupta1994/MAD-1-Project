from flask import Flask, render_template

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign-in")
def sign():
    return render_template("sign-in.html")

@app.route("/sign-up")
def sig():
    return render_template("sign-up.html")


if __name__== "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


