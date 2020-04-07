from flask import Flask, render_template      
import udemy

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", data=udemy.coupon_data())


if __name__ == '__main__':
    app.run()