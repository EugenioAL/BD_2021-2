#include <cstring>
#include <fstream>
#include <iostream>
#include <vector>
#include "tp2_header.h"

int funcaoHash(int tamHash, int key){//basicamente pegando o resto da divisao pelo tamanho da hash.
    int pos;
    pos = key%tamHash;
    return pos;
}

int setHashSize(int block_size){//setando um tamanho para hash.
    int greatest_key;
    FILE* myfile;
    myfile = fopen("dados.bin","r");//abri o file de arquivos pq vi que esta ordenado.
    fseek(myfile,-584,SEEK_END);//resolvi pegar o ultimo registro.
    fread(&greatest_key,1,sizeof(int),myfile);
    fclose(myfile);
    int tam ;
    if(greatest_key > ((block_size/sizeof(keysAndPointers))-2)){//percebi que do modo que fiz a hash fica muito ruim para um numero de registros menor que a quantidade de chaves pro blocos.
    tam =  greatest_key/((block_size/sizeof(keysAndPointers))-2);
    }
    else{
        tam = greatest_key;
    }
    tam = tam + tam*10;//infelizmente pensei em grandes quantidades de registros, quando tem um numero de registro menor que a quantidade de chaves por bloco o arquivod e index fica muito maior que o de registros.
    return tam;
}

void criaArquivoHash(int hash_size,int block_size){//aqui tentei fazer uma aglutinação de variaveis para que fosse do tamanho de um bloco.
    int qtKeys = (block_size/sizeof(keysAndPointers))-1;//no total um bloco de 4096bytes como do meu sistema cabe 256 blocos, pensei em retirar uma chave para caso haja overflow.
    int a = qtKeys;
    FILE* hashfile;
    hashfile = fopen("hash_index.bin", "wb+");
    int i,j,p =-3;
    keysAndPointers aux;
    aux.key = -1;
    aux.pointer = -1;//inicializei chaves com valores padrões signficando o vazio como "-1".
    Bucket keys;
    for(i=0; i < qtKeys; i++){
        keys.vetor.push_back(aux);
    }
    for(i=0; i < hash_size; i++){
        for(j=0; j < qtKeys; j++){
        fwrite(&keys.vetor.at(j),1,sizeof(keysAndPointers),hashfile);
        }
        fwrite(&p,1,sizeof(long int),hashfile);
    }

    fclose(hashfile);
}


bool insereNobucket(keysAndPointers key){//para inserir a cahve no bucket.
    FILE *hashfile;
    int block_size = set_block_size();
    int hash_size = setHashSize(block_size);
    int qt_keys = (block_size/sizeof(keysAndPointers))-1;
    hashfile = fopen("hash_index.bin","rb+");
    int i= 0,posBucket = funcaoHash(hash_size,key.key);
    keysAndPointers *vetor;
    vetor = (keysAndPointers*)malloc(qt_keys*sizeof(keysAndPointers));
    if(vetor == NULL){
        cout << "Erro de memoria!" << endl;
    }
    int flag = 0,indice = posBucket * block_size;//o indice é a multiplicação do que vem da função hash com o tamanho da pagina/bloco, fazendo assim eu acessar o bloco correto.
    fseek(hashfile,indice,SEEK_SET);//posicionando o pronteiro do file no inicio de um bloco;
    fread(vetor,1,qt_keys*sizeof(keysAndPointers),hashfile);
    while( i < qt_keys && flag==0){
        if(vetor[i].key == -1){
            vetor[i].key = key.key;
            vetor[i].pointer = key.pointer;
            flag = 1;// flag para marcar quando eu achei um espaço vazio para escrever minha chave e parar de procurar no resto do bucket.
        } 
        i++;
    }

    fseek(hashfile,indice + i*sizeof(keysAndPointers),SEEK_SET);//posicionando o ponteiro para gravar a chave na posição vazia do bucket.
    fwrite(&vetor[i-1],1,sizeof(keysAndPointers),hashfile);
    free(vetor);
    fclose(hashfile);
    if(flag == 0){
        cout << "precisa de overflow" << vetor[i].key << endl;
        return false;
    }
    else{
        return true;
    }
}


void loadHash(int tamHash){//carregando as chaves do arquivo de registros para o arquivo de indexação por hash.
    FILE *datafile;
    keysAndPointers *vetorChaves;
    int i=0,j;
    artigo id;
    vetorChaves = (keysAndPointers*)malloc(tamHash*sizeof(keysAndPointers));
    datafile = fopen("dados.bin","r");
    fseek(datafile,0,SEEK_END);
    long int fim = ftell(datafile);
    rewind(datafile);


    while(i < tamHash && fim!=ftell(datafile)){
        vetorChaves[i].pointer = ftell(datafile);
        fread(&id,1,sizeof(artigo),datafile);
        vetorChaves[i].key = id.id;
        if(i == tamHash-1){
            for(j=0;j< tamHash;j++){//utilizei o tamanho da hash como buffer.
                insereNobucket(vetorChaves[j]);
                i=0;
            }
        }
        i++;
    }
    for(j=0;j< i;j++){//esse "for" é para gravar os resto dos registros que nao foram capazes de preencher o buffer;
                insereNobucket(vetorChaves[j]);
            }

    fclose(datafile);
}


artigo findrec(int key){//muito similar a de alocação.
    int block_size = set_block_size();
    int hash_size = setHashSize(block_size);
    int qt_keys = (block_size/sizeof(keysAndPointers))-1;
    int bucket = funcaoHash(hash_size,key);
    FILE* hashfile;
    FILE* datafile;
    artigo tmp;//criando uma variavel temporaria para receber os dados recuperados.
    hashfile = fopen("hash_index.bin","rb");
    int i= 0,posBucket = funcaoHash(hash_size,key);
    keysAndPointers *vetor;
    vetor = (keysAndPointers*)malloc(qt_keys*sizeof(keysAndPointers));
    if(vetor == NULL){
        cout << "Erro de memoria!" << endl;//verificando se o SO me entregou a memoria pedida;
    }
    int flag = 0,indice = posBucket * block_size;
    fseek(hashfile,indice,SEEK_SET);
    fread(vetor,1,qt_keys*sizeof(keysAndPointers),hashfile);
    while( i < qt_keys && flag==0){
        if(vetor[i].key == key){
            datafile = fopen("dados.bin","rb");
            fseek(datafile,vetor[i].pointer,SEEK_SET);
            fread(&tmp,1,sizeof(artigo),datafile);
            fclose(datafile);
            return tmp;//se eu achei minha chave não tem  mais o porquê de continuar a contar.
            flag = 1;
        } 
        i++;
    }

    fseek(hashfile,indice + i*sizeof(keysAndPointers),SEEK_SET);
    cout << indice + i*sizeof(keysAndPointers) << endl;
    fwrite(&vetor[i-1],1,sizeof(keysAndPointers),hashfile);
    free(vetor);
    tmp.id = -1;//caso eu não ache a chave set o id para "-1" siginificando que nao achei.
    return tmp;

    /*TODO
    Tratar overflowno bucket

    */
}
