from elasticsearch import Elasticsearch 
import time
import os
import xlrd

ES_PORT = os.environ['ES_PORT']
ES_HOST = os.environ['ES_HOST']
ES_INDEX_NAME = "naor_expenses"
ES_DOC_TYPE = "expense_log"
SHEET_LOC = "expences.xlsx"

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
	es = init_es()
	for dic in sheet_rows_to_dics():		
		res = add_doc_to_index(es, dic)
		print(res)


if __name__ == "__main__":
	print("start")
	load_sheet_to_es()
	print("finish")

