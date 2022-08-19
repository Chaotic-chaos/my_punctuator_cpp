# -*- coding: utf-8 -*-
'''
Project:       ~/projects/Pythons/cpp_punctuator/punctuator_installer/src/use_sample
File Name:     use_sample.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/08/19
Software:      Vscode
'''

import argparse
import re
import punctuator


parser = argparse.ArgumentParser()

parser.add_argument("--model", default="models/punctuator/punctuator.pth")
parser.add_argument("--input-vocab", default="punctuator_installer/src/use_sample/utils/input.dict.txt")
parser.add_argument("--output-vocab", default="punctuator_installer/src/use_sample/utils/label.dict.tsv")
parser.add_argument("--sentence", default="是谁创造了人类世界是我们劳动群众")

args = parser.parse_args()

if __name__ == '__main__':
    # Read dictionaries
    input_vocab = {}
    output_vocab = {}
    with open(args.input_vocab, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
        for index, line in enumerate(lines):
            input_vocab[line] = index
    with open(args.output_vocab, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
        for line in lines:
            output_vocab[line.split("\t")[0]] = line.split("-t")[-1]

    # init model
    model = punctuator.Punctuator()
    model.setup_model(args.model)
    

    # tokenize sentence
    sentence = args.sentence
    sentence = re.sub("[a-z,A-Z,0-9]", "", sentence)
    sentence = sentence.replace(" ", "")
    sentence = list(sentence)
    ids = [input_vocab.get(c, input_vocab.get("[UNK]")) for c in sentence]
    size = len(ids)
    ids = " ".join([str(i) for i in ids])

    # decode
    res_label = model.decode(ids, size)
    res_label = res_label.split(" ")
    res_sentence = []
    for c, l in zip(sentence, res_label):
        if l == "_SPACE":
            res_sentence.append(c)
        else:
            res_sentence.append(f"{c}{l[0]}")
    res_sentence = "".join(res_sentence)

    # for debug
    # print(res_sentence)
