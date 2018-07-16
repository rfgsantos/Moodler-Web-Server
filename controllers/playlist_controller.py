from flask import Flask, jsonify, request
from dao.playlist_dao import PlaylistDao
from main_app import app

playlistdao = PlaylistDao()

@app.route('/playlist', methods=['GET'])
def get_all_playlist():
    return jsonify(playlistdao.get_all_playlist())

@app.route('/playlist/<int:id>', methods=['GET'])
def get_playlist_by_id(id):
    return jsonify(playlistdao.get_playlist_by_id(id))

@app.route('/playlist/insert', methods=['POST'])
def insert_playlist():
    return jsonify(playlistdao.insert_playlist(request.json))

@app.route('/playlist/delete/<int:id>', methods=['GET'])
def delete_playlist(id):
    return jsonify(playlistdao.delete_playlist(id))