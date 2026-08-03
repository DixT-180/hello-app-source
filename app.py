from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()

    a = data.get("a")
    b = data.get("b")

    if a is None or b is None:
        return jsonify({
            "error": "Both 'a' and 'b' are required"
        }), 400

    result = a + b

    return jsonify({
        "a": a,
        "b": b,
        "result": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)