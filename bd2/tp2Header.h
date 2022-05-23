struct artigos
{
    int id;
    char titulo[300];
    int ano;
    char autores[150];
    int citacoes;
    char atualizacao;
    char snippet[100];
};


int BlockSizeValue();

void escreveBuffer(artigos vetor[], int block_size, FILE* dados);

void coletaDados(string fileName, int block_size);
void nada2();
void nada();
