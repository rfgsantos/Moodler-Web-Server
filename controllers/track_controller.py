import sys
sys.path.append("../utils")
sys.path.append("../dao")
from flask import Flask, jsonify, request
from track_dao import TrackDao
database_connector = DatabaseConnector()
trackdao = TrackDao(database_connector)

@app.route('/track', methods=['GET'])
def get_all_track():
    return jsonify(trackdao.get_all_track())

@app.route('/track/<int:id>', methods=['GET'])
def get_track_by_id(id):
    return jsonify(trackdao.get_track_by_id(id))

@app.route('/track/insert', methods=['GET'])
def insert_track():
    return jsonify(trackdao.insert_track(request.json))

@app.route('/track/delete/<int:id>', methods=['GET'])
def delete_track(id):
    return jsonify(trackdao.delete_track(id))