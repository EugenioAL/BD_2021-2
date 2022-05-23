#include <cstring>
#include <fstream>
#include <iostream>
#include<algorithm>
#include "tp2Header.h"

using namespace std;

int BlockSizeValue(){
    int size_block ;
    ifstream tempfile;
    string temp;
    system("stat -fc %s . > blocksize.txt");
    std::cout << std::ifstream("blocksize.txt").rdbuf();
    tempfile.open("blocksize.txt", ios::out);
    getline(tempfile,temp);
    char cvet[] = {temp[0],temp[1],temp[2],temp[3]};
    size_block = atoi(cvet);
    return size_block;
}

void escreveBuffer(artigos vetor[], int block_size, FILE* dados){
    
}

void coletaDados(string fileName, int block_size) {
    string line;
    ifstream myfile;
    FILE *arquivoDados; 
    size_t pos = 0;
    std::string delimiter = ";";
    myfile.open(fileName, ios::out);
    std::string token;
    int i;
    artigos buffer_dados[block_size];
    arquivoDados = fopen("dados.bin","wb");
    while ( getline (myfile,line) )
    {
        size_t pos = 0;
        while ((pos = line.find(delimiter)) != std::string::npos) {
            token = line.substr(0, pos);
            token.erase(remove(token.begin(), token.end(), '\"'), token.end());
            std::cout << token << std::endl;
            line.erase(0, pos + delimiter.length());
        }
        token = line;
        token.erase(remove(token.begin(), token.end(), '\"'), token.end());

        std::cout << token << std::endl;
    }

}
