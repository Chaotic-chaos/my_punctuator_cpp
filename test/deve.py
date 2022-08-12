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

from ctypes import *

if __name__ == '__main__':
    pSo = CDLL("bind/build/punctuator.cpython-38-x86_64-linux-gnu.so")

    punc = pSo.Punctuator()

    print(punc)
