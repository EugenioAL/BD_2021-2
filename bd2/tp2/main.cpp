#include <cstring>
#include <fstream>
#include <iostream>
#include <vector>
#include "tp2_header.h"

using namespace std;

int main(int argc, char *argv[]){
    int escolha = 5,chave;
    artigo tmp;
    upload(argv[1]);//Faz o principal arquivo onde os dados estão armazenados.
    criaArquivoHash(setHashSize(set_block_size()),set_block_size());//cria o arquivo indexado pro hash em si, setando os valores para "-1" o qual eu considerei como vazio.
    loadHash(setHashSize(set_block_size()));//faz a carga dos registros nos arquivo da hash;
    while(escolha != 0){    
        cout << "Escolha uma opção:" << endl;
        cout << "\t1 --> Busca ID no arquivo de indexação Hash:" << endl;
        cout << "\t2 --> Busca ID no arquivo de indexação B+:" << endl;
        cout << "\t3 --> Busca Titulo no arquivo de indexação B+:" << endl;
        cout << "\t0 --> Sair!" << endl;
        cin >> escolha;
        switch (escolha)
        {
        case 1:
                cout << "Digite uma Chave:" << endl;
                cin >> chave;
                tmp = findrec(chave);
                cout << "\tID:\t" << tmp.id << endl;
                cout << "\tTitulo:\t" << tmp.titulo << endl;
                cout << "\tAno:\t" << tmp.ano << endl;
                cout << "\tAutores:\t" << tmp.autores << endl;
                cout << "\tCitacoes:\t" << tmp.citacoes << endl;
                cout << "\tAtualizacao:\t" << tmp.data << endl;
                cout << "\tSnippet:\t" << tmp.snippet << endl;;
            break;
        case 2:
            cout <<  "Não implementado!" << endl;
            break;
        case 3:
            cout <<  "Não implementado!" << endl;
            break;
        case 0:
            cout <<  "Sair!" << endl;
            break;
        default:
            break;
        }
    }
}