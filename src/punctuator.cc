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

#include <iostream>
#include <map>

class Punctuator {
    public:
        std::string input_dict_path;
        std::map<int, std::string> label_dict = {
            {1, "，COMMA"},
            {2, "。PERIOD"},
            {3, "？QUESTIONMARK"},
            {4, "_SPACE"}
        };
        std::map<int, std::string> input_dict;
};

int main(){
    Punctuator punctuator;
    std::map<int, std::string>::iterator iter;
    for(iter=punctuator.label_dict.begin(); iter != punctuator.label_dict.end(); iter++){
        std::cout << iter->first << " : " << iter->second << "\n";
    }
    return 0;
}