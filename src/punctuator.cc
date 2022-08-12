/*
Project:       ~/projects/Pythons/cpp_punctuator/src
File Name:     punctuator.cc
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2022/08/11
Software:      Vscode
*/

// Main Punctuator Decoder
/*
Input: !
*/

#include <torch/script.h>
#include <iostream>
#include <map>
#include <fstream>
#include <string>
#include "punctuator.h"

// Functions defination
// void Punctuator::setup_input_dict(std::string input_dict_path){
//     // load input_dict
//     std::string line;
//     std::ifstream infile;
//     infile.open(input_dict_path);

//     for (int i=0; getline(infile, line); i++){
//         input_dict[line] = i;
//     }

//     return;
// }

Punctuator::Punctuator(){
    return;
}

void Punctuator::setup_model(std::string model_path)
{
    // setup the model
    model = torch::jit::load(model_path);

    return;
}

std::string Punctuator::decode(int *sentence, int size)
{
    // main decode function
    // 1. convert all words into id(Departured due to C++'s limited with Chinese string)
    // 2. build Tensor from ids-array
    // 3. check input length: return [ERROR] if more than 512
    // 4. forward the model
    // 5. decode the tensor
    // 6. return the labels string

    if (size > 512){
        std::cout << "Max input(512) length HIT!";
        return "[ERROR]";
    }

    // build input
    torch::Tensor input_tensor = torch::zeros({size}).to(torch::kLong);
    std::vector<torch::jit::IValue> input_final;
    for(int i=0; i<size; i++){
        input_tensor[i] = sentence[i];
    }
    input_tensor = input_tensor.unsqueeze(0);
    input_final.push_back(input_tensor);
    std::cout << input_tensor << "\n";
    std::cout << input_final << "\n";

    // inference
    torch::Tensor res = model.forward(input_final).toTensor();

    // decode res
    res = torch::argmax(res.squeeze(0), 1);
    std::string final_res;
    for (int i=0; i<res.size(0); i++){
        int j = res[i].item().toInt();
        final_res.append(label_dict[j]);
        final_res.append(" ");
    }
    std::cout << final_res << "\n";

    return final_res;
}

int main()
{
    Punctuator punctuator;
    std::map<int, std::string>::iterator iter;
    for (iter = punctuator.label_dict.begin(); iter != punctuator.label_dict.end(); iter++)
    {
        std::cout << iter->first << " : " << iter->second << "\n";
    }

    // punctuator.setup_input_dict("/root/projects/Pythons/cpp_punctuator/src/utils/vocab.txt");

    // std::map<std::string, int>::iterator input_dict_it;
    // input_dict_it = punctuator.input_dict.begin();
    // while(input_dict_it != punctuator.input_dict.end()){
    //     std::cout << input_dict_it->first << " : " << input_dict_it->second << "\n";
    //     input_dict_it++;
    // }

    punctuator.setup_model("/root/projects/Pythons/cpp_punctuator/models/punctuator/punctuator.pth");

    // at::Tensor input;
    // input = torch::tensor({{2, 3, 55, 56}}).to(torch::kLong);
    // std::vector<torch::jit::IValue> inputs;
    // std::cout << input << "\n";
    // inputs.push_back(input);
    // std::cout << punctuator.model.forward(inputs).toTensor();

    // std::cout << punctuator.decode("你好");

    int s[] = {55, 56, 90};
    int input_size = sizeof(s) / sizeof(int);
    punctuator.decode(s, input_size);

    // for development only
    // int s[] = {55, 56, 90};
    // int s_size = sizeof(s)/sizeof(int);
    // for (int i=0; i<s_size; i++){
    //     std::cout << s[i] << "\n";
    // }

    return 0;
}