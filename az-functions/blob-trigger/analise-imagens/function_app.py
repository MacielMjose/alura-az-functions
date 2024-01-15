import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()


@app.blob_trigger(arg_name="myblob", path="analise-imagens",
                               connection="DefaultEndpointsProtocol=https;AccountName=jomacaimagens;AccountKey=EeUyj9lgc75jPtHZdfYVY51W4pEImrhkudvVv0JNMTl4/LotbF58cNMgggpfgDTHzkR24GFmSE36+ASt7u0Ihg==;EndpointSuffix=core.windows.net") 
def BlobTrigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob: {myblob.name}")
