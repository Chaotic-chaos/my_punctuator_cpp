#ifndef PUNCTUATOR_H
#define PUNCTUATOR_H

#include <torch/script.h>
#include <iostream>
#include <map>
#include <fstream>
#include <string>

class Punctuator
{
public:
    std::map<int, std::string> label_dict = {
        {1, "，COMMA"},
        {2, "。PERIOD"},
        {3, "？QUESTIONMARK"},
        {4, "_SPACE"}};
    // std::map<std::string, int> input_dict;
    torch::jit::script::Module model;

    // void setup_input_dict(std::string input_dict_path);
    Punctuator();
    void setup_model(std::string model_path);
    std::string decode(int *sentence, int size);
};

#endif