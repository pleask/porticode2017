from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/browser")
def browser():
    return render_template("browser.html")

@app.route("/sentiment")
def sentiment():
    return render_template("sentiment.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
