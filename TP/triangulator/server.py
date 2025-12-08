from flask import Flask, jsonify, Response
from TP.triangulator.client_psm import PointSetManagerClient
from TP.triangulator.triangulation import triangulate
from TP.triangulator.binary import encode_triangles

app = Flask(__name__)

PSM_URL = "http://localhost:5001"
client = PointSetManagerClient(PSM_URL)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "Triangulator running"}), 200


@app.route("/triangulate/<int:ps_id>", methods=["GET"])
def triangulate_endpoint(ps_id):
    try:
        ps = client.get_pointset(ps_id)
    except Exception as e:
        return jsonify({
            "error": "cannot fetch pointset",
            "detail": str(e)
        }), 502

    # إذا الـ PointSetManager رجّع None
    if ps is None:
        return jsonify({
            "error": "cannot fetch pointset",
            "detail": "PointSetManager returned None"
        }), 502

    triangles = triangulate(ps.points)
    data = encode_triangles(ps, triangles)

    return Response(
        data,
        status=200,
        content_type="application/octet-stream"
    )


