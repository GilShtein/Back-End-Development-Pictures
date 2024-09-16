from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures"""
    if data:
        response = jsonify(data)
        response.headers["Content-Type"] = "application/json"
        return response, 200
    else:
        return jsonify({"message": "No pictures found"}), 404

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for item in data:
        if item["id"] == id:
            return jsonify(item), 200
    return jsonify({"message": "No pictures found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.get_json()
    print(new_pic)
    if not new_pic:
        # Return a JSON response indicating that the request data is invalid or missing
        # with a status code of 400 (Bad Request)
        return {"message": "Invalid input, no data provided"}, 400
    for item in data:
        if item["id"] == new_pic["id"]:
            return {"Message": f"picture with id {new_pic['id']} already present"}, 302
    data.append(new_pic)
    return jsonify(new_pic), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_pic = request.get_json()
    if not new_pic:
        # Return a JSON response indicating that the request data is invalid or missing
        # with a status code of 400 (Bad Request)
        return {"message": "Invalid input, no data provided"}, 400
    for item in data:
        if item["id"] == new_pic["id"] and item["id"] == id:
            data.remove(item)
            data.append(new_pic)
            return jsonify(new_pic), 201

    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for item in data:
        if item["id"] == id:
            data.remove(item)
            return jsonify(), 204

    return {"message": "picture not found"}, 404
