/*
Project:       ~/projects/Pythons/cpp_punctuator/src
File Name:     deve.cc
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/08/11
Software:      Vscode
*/

// development use only

#include <torch/script.h>
#include <iostream>

int main(int argc, const char* argv[]){
    if (argc != 2){
        std::cout << "usage: example-app <path-to-exported-script-module>" << "\n";
        return -1;
    }

    torch::jit::script::Module model;

    // load model
    model = torch::jit::load(argv[1]);

    //build input
    at::Tensor input;
    input = torch::tensor({{2, 3, 55, 56}}).to(torch::kLong);
    std::vector<torch::jit::IValue> inputs;
    std::cout << input << "\n";
    inputs.push_back(input);

    // inference
    at::Tensor res = model.forward(inputs).toTensor();
    std::cout << res << "\n";

    // decode
    res = torch::argmax(res.squeeze(0), 1);
    // std::cout << res[1] << std::endl;
    // build label dict
    std::map<int, std::string> label_dict = {
        {1, "，COMMA"},
        {2, "。PERIOD"},
        {3, "？QUESTIONMARK"},
        {4, "_SPACE"}
    };
    for (int i=0; i<res.size(0); i++) {
        int j = res[i].item().toInt();
        std::cout << label_dict[j] << std::endl;
    }

    std::cout << "All Done!" << "\n";
}