from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/cars")
def index():
    return render_template("cars.html")

@app.route("/car/new")
def index():
    return render_template("new_car.html")
