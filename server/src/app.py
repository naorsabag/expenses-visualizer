from flask import Flask, jsonify, request
from esHandler import ESHandler
import asyncio
import os
import json

ES_PORT = os.environ['ES_PORT']
ES_HOST = os.environ['ES_HOST']
ES_INDEX_NAME = "expenses"
SHEET_LOC = "expences.xlsx"

app = Flask(__name__)
es = ESHandler(ES_HOST,ES_PORT,ES_INDEX_NAME)

@app.route('/hello/', methods=['GET'])
def index():
    return jsonify(ping='Hello i\'m at your service')


@app.route('/get-all-categories/', methods=['GET'])
def get_all_categories():
    return jsonify(categories = ['category1','category2','category3'])


@app.route('/<category>/get-all-sub-categories/', methods=['GET'])
def get_all_sub_categories(category=None):
    return jsonify(sub_categories = [category+'-sub-category1',category+'-sub-category2',category+'-sub-category3'])


@app.route('/<subCategory>/get-all-items/', methods=['GET'])
def get_all_items(subCategory=None):
    return jsonify(items=[subCategory+'-item1',subCategory+'-item2',subCategory+'-item3'])


@app.route('/add-transaction/', methods=['POST'])
def add_transaction():
	res = es.insert_form_data(request.form)
	return json.dumps({'success':True, 'data':res}), 200, {'ContentType':'application/json'}

async def main():
	await es.init()
	es.insert_sheet(SHEET_LOC)
	app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
	print("start server")
	asyncio.run(main())

