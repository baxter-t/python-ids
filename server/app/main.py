from flask import Flask, send_file
import time

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world"


@app.route("/large_file")
def largeFile():
    return send_file("static/large.html")


@app.route("/medium_file")
def mediumFile():
    return send_file("static/medium.html")


@app.route("/small_file")
def smallFile():
    return send_file("static/small.html")


@app.route("/loaderio-5f3ff86bbddd530dd5680755941a65c3.html")
def loader():
    return send_file('static/loaderio-5f3ff86bbddd530dd5680755941a65c3.html')

@app.route("/test_server", methods=["GET", "POST"])
def testEndpoint():
    return "{'output': 100, 'outpu2': 200}"

@app.route("/slow_endpoint", methods=['POST'])
def testSlowEndpoint():
    time.sleep(2)
    return "{'output': 100, 'outpu2': 200}"
     

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
