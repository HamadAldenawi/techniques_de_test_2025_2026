from flask import Flask, request, jsonify, Response
from TP.point_set_manager.storage import Storage
from TP.triangulator.binary import encode_pointset

app = Flask(__name__)
storage = Storage()

@app.route("/")
def home():
    return jsonify({"status": "PointSetManager OK"})

@app.route("/pointset", methods=["POST"])
def create_pointset():
    data = request.get_json()
    if not data or "points" not in data:
        return jsonify({"error": "missing points"}), 400

    try:
        pid = storage.add_pointset(data["points"])
        return jsonify({"id": pid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/pointset/<int:pid>", methods=["GET"])
def get_pointset(pid):
    ps = storage.get_pointset(pid)
    if ps is None:
        return jsonify({"error": "not found"}), 404

    binary = encode_pointset(ps)
    return Response(binary, content_type="application/octet-stream")

if __name__ == "__main__":
    app.run(port=5001)
