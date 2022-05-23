#ifndef tp2_lib
#define tp2_lib

using namespace std;


struct artigo{
    int id;
    char titulo[300];
    int ano;
    char autores[150];
    int citacoes;
    char data[20];
    char snippet[100];

};//nao segui o pedido na especificação por achar que os campos que nao tem indices, ou vai ver o professor queria que implementassemos o tamanho variavel dos registros.
//################ Structs para hash #############################
struct keyPointer{
    int key;
    long int pointer;
};

typedef struct keyPointer keysAndPointers;//campos com a chave seguindo do endereço.

struct bucket
{
    vector <keysAndPointers> vetor;
};
typedef struct bucket Bucket;//onde acumulo as chaves;


typedef struct bucketNode
{
    Bucket bucket;
    long int este;
    long int prox;
}bucketNode;//essa é a representação de uma celula da hash.



int set_block_size();//função que define o tamanho da hash dinamicamente.



void upload(string arquivo) ;//preparação do arquivo de registros.

void buffer_to_file(artigo buffer[], int tam);//copiando o buffer para o arquivo.

void string_to_vet_char(string source, char data[],int tam);


//##################################### funçoes Hash #############################

void criaArquivoHash(int hash_size,int block_size);//inicializa o arquivo com valores que eu considero como vazio.

int setHashSize(int block_size);//gera o tamanho da hash dinamicamente, tendo como parametro a maior chave dos registros.

bool insereNobucket(keysAndPointers key);//procura um espaço vazio onde possa gravar o registro.

void loadHash(int tamHash);//faz a carga das chaves dos registros com seus respectivos endereços no arquivo de indice.

artigo findrec(int key);//função de busca solicitada na especificação.




#endif