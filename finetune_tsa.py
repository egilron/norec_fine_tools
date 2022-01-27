#! /bin/env python3

import sys
from simpletransformers.ner import NERModel, NERArgs
import torch
import pandas as pd
import pickle as pk
import os
import random
import json
import time, datetime
random.seed(64)
import re
from helpers import *

print(f"Cuda: {torch.cuda.is_available()}")



# Originally made for multiple datasets
datasets = [('data/spaceseparated/norec_fine/norec_fine_train.conll', 'data/spaceseparated/norec_fine/norec_fine_dev.conll', ['I-targ-negative', 'I-targ-positive',
 'B-targ-negative', 'B-targ-positive', 'O'])]
train_path, dev_path, tags = datasets[0]
# Check that the tags are consistent
# You may delete the following, and the notebook will then run without the helpers.py
for path in [dev_path,train_path]:
    with open (path) as rf:
        text = rf.read()
        assert tagsset(text, separator = " ") == set(tags), tagsset(text, separator = " ")
print("Tags checked OK")



# Run bert with the data from previous lines
parent = {
    'bert-base-multilingual-cased': "bert",
    'NbAiLab/nb-bert-base' : "bert",
    'ltgoslo/norbert' : "bert" ,
    'xlm-roberta-base' : 'xlmroberta'
}

transformersmodels = sys.argv[1:]
print("models from args:", transformersmodels)
if len(transformersmodels) == 0:
    transformersmodels = ['bert-base-multilingual-cased'  ] #,  'ltgoslo/norbert', 'NbAiLab/nb-bert-base'
print("about to run models:", transformersmodels)
assert len( set(transformersmodels) - set(parent)) == 0, "We have a model without parent"

results = []
for transformersmodel in transformersmodels:
    model_args = NERArgs()
    model_args.train_batch_size = 12
    model_args.num_train_epochs = 8
    model_args.weight_decay = 0.001
    model_args.overwrite_output_dir = True
    model_args.silent = True
    model_args.save_model_every_epoch = False
    model_args.save_eval_checkpoints = True
    model_args.save_steps = -1
    model_args.warmup_ratio = 0

    model = NERModel(parent[transformersmodel],transformersmodel , labels = tags,args=model_args, use_cuda=True)

    out_d = "outputs/simpletransformers/"+transformersmodel+"_"+train_path.split("/")[-2]

    model.train_model(train_path, output_dir= out_d)
    print(transformersmodel, "Done training")

    result, model_outputs, predictions = model.eval_model(dev_path)
    result["transformer_model"] = transformersmodel
    for k, v in result.items():
        print(transformersmodel, k, v)
    predictions, raw_outputs = model.predict (["Mannen på scenen synger stygt", "Damen på scenen synger stygt" , "Disse bilene har et fantastisk veigrep"])
    for sentence in predictions:
        print(sentence)
    results.append(result)


df = pd.DataFrame.from_dict(results)

print(df)