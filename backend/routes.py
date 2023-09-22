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
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if 0 <= id < len(data):
        return jsonify({"id": id, "url": data[id]})
    else:
        return jsonify({"error": "Invalid ID"}), 404



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture_data = request.get_json()

    if not picture_data:
        return {"message": "Picture data not provided"}, 400

    # Check if a picture with the same ID already exists
    for picture in data:
        if picture.get("id") == picture_data.get("id"):
            return {"Message": f"picture with id {picture_data['id']} already present"}, 302

    try:
        data.append(picture_data)
    except NameError:
        return {"message": "data not defined"}, 500

    return jsonify({"id": picture_data['id']}), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # get data from the json body
    picture_in = request.json
    for index, picture in enumerate(data):
        if picture["id"] == id:
            data[index] = picture_in
            return picture, 201
    return {"message": "picture not found"}, 404
    

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            # Delete the item from the list
            data.remove(picture)
            return "", 204  # Return an empty body with HTTP status 204 (No Content)

    # If the picture with the specified ID was not found, return a 404 error
    return jsonify({"message": "picture not found"}), 404

