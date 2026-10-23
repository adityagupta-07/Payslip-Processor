from flask import Flask, jsonify, request

app = Flask(__name__, static_folder="static", static_url_path="")

@app.get("/")
def home():
    return app.send_static_file("index.html")


@app.get("/api/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)