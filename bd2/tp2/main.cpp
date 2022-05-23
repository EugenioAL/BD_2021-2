#include <cstring>
#include <fstream>
#include <iostream>
#include <vector>
#include "tp2_header.h"

using namespace std;

int main(int argc, char *argv[]){
    int escolha,chave;
    artigo tmp;
    upload(argv[1]);//Faz o principal arquivo onde os dados estão armazenados.
    cout << "Escolha uma opção:" << endl;
    cout << "\t1 --> Busca ID no arquivo de indexação Hash:" << endl;
    cout << "\t2 --> Busca ID no arquivo de indexação B+:" << endl;
    cout << "\t3 --> Busca Titulo no arquivo de indexação B+:" << endl;
    cin >> escolha;
    switch (escolha)
    {
    case 1:
            cout << "Digite uma Chave:" << endl;
            cin >> chave;
            criaArquivoHash(setHashSize(set_block_size()),set_block_size());//cria o arquivo indexado pro hash em si, setando os valores para "-1" o qual eu considerei como vazio.
            loadHash(setHashSize(set_block_size()));//faz a carga dos registros nos arquivo da hash;
            tmp = findrec(chave);
            cout <<  tmp.id << endl;
            cout <<  tmp.titulo << endl;
            cout <<  tmp.ano << endl;
            cout <<  tmp.autores << endl;
            cout <<  tmp.citacoes << endl;
            cout <<  tmp.data << endl;
            cout <<  tmp.snippet << endl;;
        break;
    case 2:
        cout <<  "Não implementado!" << endl;
        break;
    case 3:
        cout <<  "Não implementado!" << endl;
        break;
    
    default:
        break;
    }
}