from flask import Flask
import time

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Everyone"


@app.route('/wait_5_sec/')
def test():
    time.sleep(5)
    return "Hello Shubham"


if __name__ == "__main__":
    app.run(debug=True)
