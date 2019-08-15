from flask import Flask, jsonify, request
from werkzeug import secure_filename
from esHandler import ESHandler
import asyncio
import os
import json

ES_PORT = os.environ['ES_PORT']
ES_HOST = os.environ['ES_HOST']
ES_INDEX_NAME = "expenses"
SHEET_FORM_DATA_NAME = "file"

app = Flask(__name__)
es = ESHandler(ES_HOST,ES_PORT,ES_INDEX_NAME)

@app.route('/hello/', methods=['GET'])
def index():
    return jsonify(ping='Hello i\'m at your service')


@app.route('/get-all-categories/', methods=['GET'])
def get_all_categories():
	res = es.get_all_categories()
	return json.dumps({'success':True, 'categories': res}), 200, {'ContentType':'application/json'}


@app.route('/<category>/get-all-sub-categories/', methods=['GET'])
def get_all_sub_categories(category=None):
	res = es.get_all_sub_categories(category)
	return json.dumps({'success':True, 'sub_categories': res}), 200, {'ContentType':'application/json'}


@app.route('/<category>/<subCategory>/get-all-items/', methods=['GET'])
def get_all_items(category=None,subCategory=None):
	res = es.get_all_items(category,subCategory)
	return json.dumps({'success':True, 'items': res}), 200, {'ContentType':'application/json'}


@app.route('/add-transaction/', methods=['POST'])
def add_transaction():
	res = es.insert_form_data(request.form)
	return json.dumps({'success':True, 'data':res}), 200, {'ContentType':'application/json'}


@app.route('/add-transactions-from-sheet/', methods=['POST'])
def add_transactions_from_sheet():
	f = request.files.get(SHEET_FORM_DATA_NAME)
	res = es.insert_sheet(f)
	return json.dumps({'success':True, 'data':f.filename}), 200, {'ContentType':'application/json'}

@app.errorhandler(500)
def internal_error(error):
	print(error, flush=True)
	return 'error', 500

async def main():
	await es.init()
	app.run(host='0.0.0.0')

if __name__ == "__main__":
	print("start server")
	asyncio.run(main())

