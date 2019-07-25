from elasticsearch import Elasticsearch 
import time
import os
import xlrd
from flask import Flask

ES_PORT = os.environ['ES_PORT']
ES_HOST = os.environ['ES_HOST']
ES_INDEX_NAME = "naor_expenses"
ES_DOC_TYPE = "expense_log"
SHEET_LOC = "expences.xlsx"

app = Flask(__name__)
es={}

@app.route('/')
def index():
    return 'Hello i\'m at your service'

def sheet_rows_to_dics():
	print("start-parse")
	wb = xlrd.open_workbook(SHEET_LOC)
	sheet = wb.sheet_by_index(0)

	first_row = sheet.row_values(0)

	for row in range(1,sheet.nrows):
		dic = {}
		i = 0;		
		for col in sheet.row_values(rowx=row):
			dic[first_row[i]] = col
			i+=1
 		
		yield (dic)
	print("finish-parse")


def init_es():
	print("start-init")
	es=Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])

	isEsUp = False
	while not isEsUp:
		time.sleep(.100)
		try:
			isEsUp = es.cluster.health()
		except:
			print("##########################################################")
			print("not yet")
			print("##########################################################")
	
	print("finish-init")
	return es;


def add_doc_to_index(es, doc):
	return es.index(index=ES_INDEX_NAME,doc_type=ES_DOC_TYPE,id=None,body=doc)


def load_sheet_to_es():
	for dic in sheet_rows_to_dics():		
		res = add_doc_to_index(es, dic)
		print(res)

if __name__ == "__main__":
	print("start")
	es = init_es()
	app.run(debug=True, host='0.0.0.0')
	load_sheet_to_es()
	print("finish")

