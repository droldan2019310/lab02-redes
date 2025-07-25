#include <iostream>
#include <string>

std::string encode_block(const std::string &d){ // d: 4 bits
    int d1=d[0]-'0', d2=d[1]-'0', d3=d[2]-'0', d4=d[3]-'0';
    int p1 = d1 ^ d2 ^ d4;
    int p2 = d1 ^ d3 ^ d4;
    int p4 = d2 ^ d3 ^ d4;
    std::string code;
    code.push_back('0' + p1);
    code.push_back('0' + p2);
    code.push_back('0' + d1);
    code.push_back('0' + p4);
    code.push_back('0' + d2);
    code.push_back('0' + d3);
    code.push_back('0' + d4);
    return code;
}

int main(){
    std::string msg;
    if(!(std::cin >> msg)) return 0;

    // padding a múltiplo de 4
    int pad = (4 - (int(msg.size()) % 4)) % 4;
    msg.append(pad,'0');

    std::string out;
    for(size_t i=0;i<msg.size(); i+=4)
        out += encode_block(msg.substr(i,4));

    // imprimimos código y padding en la misma línea separados por espacio
    std::cout << out << " " << pad << "\n";
    return 0;
}