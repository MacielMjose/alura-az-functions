import logging
import azure.functions as func
import json
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.queue import QueueServiceClient
from azure.storage.queue import QueueClient


##Computer Vision
endpoint = 'https://imagedetectionpython.cognitiveservices.azure.com/'
key = 'c721a2ea67414790a3e00a3c8d998b82'
credentials = CognitiveServicesCredentials(key)
client = ComputerVisionClient(endpoint, credentials)

##Storage Accounts
account_key='ymcOHHeGgTeN/85RJFhsSoUdS7ZJ+3aFGKXff63TXWFZg7hl8oYwS4rMZEbDn+7RxToQQcdkH2zQ+AStNXKcUg=='

##Queue URL
queue_url = 'https://imagerecognitionpy.queue.core.windows.net/analised-images'

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="images",
                               connection="StorageAccountConnection") 

def blob_trigger(myblob: func.InputStream):
    start_function_calls(myblob)

def start_function_calls(myblob: func.InputStream):
    logging.info(f'Python blob trigger function processed blob: {myblob.name}')
    url = myblob.uri

    arquivo = myblob.name.split("/")[1]

    json_data = analisa_image(url,arquivo)
    try: 
        envia_para_fila(json_data)
    except:
        logging.info('um erro ocorreu e mensagem não foi enviada')

def analisa_image(url,arquivo):
    language = "pt"
    max_descriptions = 3
    descricao =[]

    analise = client.describe_image(url, max_descriptions, language)

    for item in analise.captions:
        descricao.extend((item.text, round(item.confidence,2)))
    
    json_data = {
            'imagem': arquivo,
            'descricao' : descricao
        }
    print(json.dumps(json_data))
    
    return json_data
    
def envia_para_fila(json_data):
    client_queue = QueueClient.from_queue_url(queue_url=queue_url,credential=account_key)
    client_queue.send_message(str(json_data))