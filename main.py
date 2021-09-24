from flask import Flask
import time

app = Flask(__name__)


@app.route('/wait_5_sec/')
def index():
    time.sleep(5)
    return "Hello Shubham"


if __name__ == "__main__":
    app.run(debug=True)
