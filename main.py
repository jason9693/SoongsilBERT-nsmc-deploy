import sentencepiece

from transformers import RobertaTokenizer, RobertaForSequenceClassification
import logging

from flask import Flask, request, render_template
import torch
from torch.nn import functional as F
import traceback

import os
from queue import Queue, Empty
from threading import Thread
import time

category_map = {
    "0": "부정",
    "1": "긍정",
}

category_map_logits = {
    "0": "neg",
    "1": "pos",
}

os.system('ls')
app = Flask(__name__)

tokenizer = RobertaTokenizer.from_pretrained('jason9693/SoongsilBERT-nsmc-base')
model = RobertaForSequenceClassification.from_pretrained('jason9693/SoongsilBERT-nsmc-base')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
app.logger.info("Model load finished")


requests_queue = Queue()    # request queue.
BATCH_SIZE = 100              # max request size.
CHECK_INTERVAL = 0.1

##
# Request handler.
# GPU app can process only one request in one time.
def handle_requests_by_batch():
    while True:
        request_batch = []
        text_list = []

        while not (len(request_batch) >= BATCH_SIZE):
            try:
                request = requests_queue.get(timeout=CHECK_INTERVAL)
                request_batch.append(request)
            except Empty:
                break

        if len(request_batch) == 0:
           continue
        # outputs = mk_predict(text_list)
        valid_requests = []
        valid_texts = []
        for idx, request in enumerate(request_batch):
            types = request["input"][0]
            txt = request["input"][1]
            valid_texts.append(txt)
            valid_requests.append(request)
        request_batch = []
            # except Exception as e:
            #     request["output"] = e
            #     return
        
        outputs = mk_predict(valid_texts)[0]
        for idx, request in enumerate(valid_requests):
            try:
                if request["input"][0] == "logits":
                    request["output"] = {
                        "num_req": len(valid_requests),
                        "result": {
                            category_map_logits[str(k)]:v for k, v 
                            in enumerate(outputs[idx].softmax(-1).tolist())}
                    }
                else:
                    request["output"] = str(torch.argmax(outputs[idx], -1).item())
            except Exception as e:
                request["output"] = e
    return


handler = Thread(target=handle_requests_by_batch).start()


##
# GPT-2 generator.
def mk_predict(text_array: list):
    try:
        inputs = tokenizer(text_array, return_tensors="pt")
        outputs = model(**inputs)[0]

        return outputs, 200

    except Exception as e:
        traceback.print_exc()
        return {'error': e}, 500


##
# Get post request page.
@app.route('/everytime/<types>', methods=['POST'])
def generate(types):
    if types not in ['logits', 'class']:
        return {'Error': 'Invalid types'}, 404

    # GPU app can process only one request in one time.
    if requests_queue.qsize() > BATCH_SIZE:
        return {'Error': 'Too Many Requests'}, 429

    try:
        args = []

        text = request.form['text']

        args.append(types)
        args.append(text)

    except Exception as e:
        return {'message': 'Invalid request'}, 500

    # input a request on queue
    req = {'input': args}
    requests_queue.put(req)

    # wait
    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    return req['output']


##
# Queue deadlock error debug page.
@app.route('/queue_clear')
def queue_clear():
    while not requests_queue.empty():
        requests_queue.get()

    return "Clear", 200


##
# Sever health checking page.
@app.route('/healthz', methods=["GET"])
def health_check():
    return "Health", 200


##
# Main page.
@app.route('/')
def main():
    return render_template('main.html'), 200


if __name__ == '__main__':
    from waitress import serve
    app.logger.info("server start")
    serve(app, port=80, host='0.0.0.0')
