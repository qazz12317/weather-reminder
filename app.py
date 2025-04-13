from flask import Flask, request, render_template
from weather import get_weather

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather = get_weather(city)
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)