from elasticsearch import Elasticsearch 
import xlrd
import asyncio
import logging; 
import datetime
logging.getLogger('elasticsearch').level = logging.ERROR

ES_DOC_TYPE = "log"
DATES_COL_BEGIN_INDEX = 3

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


    def __sheet_rows_to_dicts(self, sheet, wb):
        first_row = sheet.row_values(0)
        dates = []
        catalogTitles = []

        for catalogIndex in range(DATES_COL_BEGIN_INDEX):
            catalogTitles.append(first_row[catalogIndex])
        
        for colIndex in range(DATES_COL_BEGIN_INDEX,len(first_row)):
            date = datetime.datetime(*xlrd.xldate_as_tuple(first_row[colIndex], wb.datemode)).strftime("%Y-%m-%d")
            dates.append(date)
        
        for rowIndex in range(1,sheet.nrows):
            currentRow = sheet.row_values(rowx=rowIndex)
            dic = {}
            for catalogIndex in range(DATES_COL_BEGIN_INDEX):
                dic[catalogTitles[catalogIndex]] = currentRow[catalogIndex]
            
            for colIndex in range(DATES_COL_BEGIN_INDEX,len(first_row)):
                dic['date'] = dates[colIndex-DATES_COL_BEGIN_INDEX]
                dic['cost'] = currentRow[colIndex]
                yield (dic)


    def __insert_dict(self, dic):
        return self.es.index(index=self.indexName,doc_type=ES_DOC_TYPE,id=None,body=dic)


    def insert_sheet(self, location):
        wb = xlrd.open_workbook(location)
        sheet = wb.sheet_by_index(0)

        for dic in self.__sheet_rows_to_dicts(sheet,wb):		
            print(dic,flush=True)
            res = self.__insert_dict(dic)
    

    def insert_form_data(self, formData):
        dic = {}
        for k, v in formData.items():
            dic[k] = v
        return self.__insert_dict(dic)