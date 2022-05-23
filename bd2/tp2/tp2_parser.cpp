#include <cstring>
#include <fstream>
#include <iostream>
#include<algorithm>
#include<vector>
#include "tp2_header.h"

using namespace std;

int set_block_size(){//função apra descobrir o taanho da pagina/bloco do SO;
    int block_size;
    ifstream tempfile;//arquivo feito como variavel, se é que isto existe.
    string temp;
    system("stat -fc %s . > blocksize.txt");//copiando o buffer dos terminal para o arquivo.
    std::ifstream("blocksize.txt").rdbuf();
    tempfile.open("blocksize.txt", ios::out);
    getline(tempfile,temp);
    char cvet[] = {temp[0],temp[1],temp[2],temp[3]};//há apenas 4 casas porque eu considerei o maximo 4096bytes por bloco/pagina.
    block_size = atoi(cvet);
    return block_size;
}

void string_to_vet_char(string source, char data[],int tam){//passa uma string para um vetor de char.
    for(int i = 0; i < tam; i++){
        data[i] = source[i];
    }
}

void buffer_to_file(artigo buffer[], int tam){//função para gravação de resgistro individual;
    FILE* myfile;
    myfile = fopen("dados.bin","ab");
    fwrite(buffer,sizeof(artigo),tam,myfile);
    fclose(myfile);
}

void upload(string arquivo) {//função que faz o load no arquivo de dados.
    string line;
    ifstream myfile;
    size_t pos = 0;
    std::string delimiter = "\";";//decidi usar este delimitador porque foi o que mais achei unico na divisão dos campos;
    string filename = arquivo;
    myfile.open(filename, ios::out);
    std::string token;
    int cont_campo, cont_posicao = 0;
    artigo *buffer = (artigo*)malloc(700*sizeof(artigo));//700 porque é o numero maximo de registro por blocos é 7 então eu quis gravar 100 blocos por vez.(700*584=408.800).
    char cvet[19];//"19" porque como a maior entrada esta na casa do milhoes, ele supre a necessidade;
    while ( getline (myfile,line) )
    {
        size_t pos = 0;
        cont_campo = 0;
        while ((pos = line.find(delimiter)) != std::string::npos) {
            token = line.substr(0, pos);//token é onde fica o campo atual.
            token.erase(remove(token.begin(), token.end(), '\"'), token.end());//esta função tira o (") da string facilitando permitindo o uso do atoi().
           // std::cout << token << std::endl;
           if(cont_campo == 0){
               string_to_vet_char(token,cvet,13);
               buffer[cont_posicao].id = atoi(cvet);
           }
           if(cont_campo == 1){
               string_to_vet_char(token,buffer[cont_posicao].titulo,300) ;
           }
           else if(cont_campo == 2){
               string_to_vet_char(token,cvet,13);
               buffer[cont_posicao].ano = atoi(cvet);
           }
           else if(cont_campo == 3){
               string_to_vet_char(token,buffer[cont_posicao].autores,150) ;
           }
           else if(cont_campo == 4){
               string_to_vet_char(token,cvet,13);
               buffer[cont_posicao].citacoes = atoi(cvet);
           }
           else if(cont_campo == 5){
               string_to_vet_char(token,buffer[cont_posicao].data,20) ;
           }
            line.erase(0, pos + delimiter.length());
            cont_campo++;
        }
        token = line;
        token.erase(remove(token.begin(), token.end(), '\"'), token.end());

       // std::cout << token << std::endl;
       string_to_vet_char(token,buffer[cont_posicao].snippet,100) ;
       cont_posicao++;
       if(cont_posicao == 700){
           buffer_to_file(buffer,700);
           cont_posicao = 0;
       }
    }
    buffer_to_file(buffer,cont_posicao);
    free(buffer);
}