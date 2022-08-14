# -*- coding: utf-8 -*-
'''
Project:       ~/projects/Pythons/cpp_punctuator/test
File Name:     deve.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/08/12
Software:      Vscode
'''

'''
Test the complie
'''

import sys
sys.path.append("/root/projects/Pythons/cpp_punctuator/")
sys.path.append("../")

import punctuator

if __name__ == '__main__':
    model = punctuator.Punctuator()

    model.setup_model("models/punctuator/punctuator.pth")

    s = "55 56 77"

    print(model.decode(s, 3))
