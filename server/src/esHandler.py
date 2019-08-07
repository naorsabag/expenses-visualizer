from elasticsearch import Elasticsearch 
import xlrd
import asyncio
import logging; 
logging.getLogger('elasticsearch').level = logging.ERROR

ES_DOC_TYPE = "expense_log"

class ESHandler:
    def __init__(self, host, port, indexName):
        self.host = host
        self.port = port
        self.indexName = indexName
        self.es = Elasticsearch([{'host':self.host,'port':self.port}])

    async def init(self):
        print("start es init")
        await asyncio.sleep(40)

        connected = False
        while not connected:
            try:
                connected = self.es.cluster.health()
            except:
                await asyncio.sleep(10)

        print("finish es init")


    def __sheet_rows_to_dicts(self, sheet):
        first_row = sheet.row_values(0)

        for row in range(1,sheet.nrows):
            dic = {}
            i = 0;		
            for col in sheet.row_values(rowx=row):
                dic[first_row[i]] = col
                i+=1
            
            yield (dic)


    def insert_dict(self, data):
        return self.es.index(index=self.indexName,doc_type=ES_DOC_TYPE,id=None,body=data)


    def insert_sheet(self, location):
        wb = xlrd.open_workbook(location)
        sheet = wb.sheet_by_index(0)

        for dic in self.__sheet_rows_to_dicts(sheet):		
            res = self.insert_dict(dic)

#TODO: make it module, wait for init es