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

import punctuator

model = punctuator.Punctuator()

model.setup_model("models/punctuator/punctuator.pth")

print(model.decode("55 56 70", 3))


