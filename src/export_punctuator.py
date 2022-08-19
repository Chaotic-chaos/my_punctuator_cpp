# -*- coding: utf-8 -*-
'''
Project:       ~/projects/Pythons/correct+punc-server/export_model
File Name:     export_punctuator.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/08/04
Software:      Vscode
'''

'''
Export Punctuator Model via Wenet's script
'''

import argparse
import os

import torch
import torch.nn as nn
from transformers import BertModel
import torch.nn.functional as F

class BERTForPunctuator(nn.Module):
    def __init__(self, label_size=5, device=torch.device("cpu"), bert_path="/root/projects/Pythons/correct+punc-server/Punctuator/pretrained_bert"):
        super(BERTForPunctuator, self).__init__()
        # self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.bert = BertModel.from_pretrained(bert_path, torchscript=False)
        self.linear = nn.Linear(768, label_size)
        self.device = device

    def forward(self, sentences):
        attention_mask = torch.sign(sentences)
        attention_mask = attention_mask.to(self.device)
        input = {
            "input_ids": sentences,
            "attention_mask": attention_mask
        }

        x = self.bert(**input)
        # x = self.bert(input_ids=input["input_ids"], attention_mask=input["attention_mask"])
        x = self.linear(x.last_hidden_state)

        pred = F.log_softmax(x, dim=-1)

        return pred


parser = argparse.ArgumentParser()

parser.add_argument("--ckp", default="/root/projects/Pythons/correct+punc-server/checkpoints/punctuation/epoch2.pt")
parser.add_argument("--bert-path", default="/root/projects/Pythons/correct+punc-server/Punctuator/pretrained_bert")
parser.add_argument("--out-path", default="/root/projects/Pythons/correct+punc-server/export_model/exported")

args = parser.parse_args()

if __name__ == '__main__':
    model = BERTForPunctuator(label_size=5, device=torch.device("cpu"), bert_path=args.bert_path)
    # model = torch.nn.DataParallel(model, device_ids=-1)

    ckp_state_dict = torch.load(args.ckp, map_location=torch.device("cpu"))["model"]
    ckp_state = {}
    for k, v in ckp_state_dict.items():
        k = k.replace("module.", "")
        ckp_state[k] = v

    model.load_state_dict(ckp_state, strict=True)

    model.eval()

    # for debug
    # print(111)

    # Transformer does not support this type
    # script_model = torch.jit.script(model)

    # script_model.save(os.path.join(args.out_path, "punctuator", "punctuator.zip"))

    # ----------------- NEW TYPE --------------------
    # traced_model = torch.jit.trace(model, torch.randint(21128, (1, 512)))
    
    # if not os.path.exists(os.path.join(args.out_path, "punctuator")):
    #     os.mkdir(os.path.join(args.out_path, "punctuator"))

    # traced_model.save(os.path.join(args.out_path, "punctuator", "punctuator.pth"))

    # print("Exported!")

    # test exported model
    inputs = torch.tensor([[2, 3, 55, 56]], dtype=torch.long)
    res = model(inputs)

    print(res)
