import pymongo

from bson import ObjectId
from datetime import datetime
from flask import Flask, jsonify, request

db = pymongo.MongoClient('mongodb://127.0.0.1')['coinbase']

if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/setData', methods=['POST'])
    def set_data():
        data = request.get_json()
        if 'results' not in data:
            return jsonify({
                "error": "Invalid Data"
            }), 400
        data = data['results']
        sync_doc = {'syncedAt': datetime.utcnow()}
        sync_doc_id = db['synced_data'].insert(sync_doc)
        for doc in data:
            doc['sync_doc_id'] = ObjectId(sync_doc_id)
        db['currency_data'].insert_many(data)
        return jsonify({
            "success": True
        }), 200

    @app.route('/getData', methods=['GET'])
    def get_data():
        latest_sync = db['synced_data'].find().sort('_id', -1).limit(1)
        latest_sync = latest_sync[0]
        if not latest_sync:
            return jsonify({
                "error": "No Data Found"
            }), 400
        data = db['currency_data'].find({
            'sync_doc_id': ObjectId(latest_sync['_id']),
            'deleted': {'$ne': True}
            })
        toReturn = []
        for doc in data:
            del doc['_id']
            del doc['sync_doc_id']
            toReturn.append(doc)
        return jsonify({
            "results": toReturn
        }), 200

    app.run()
