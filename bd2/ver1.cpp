#include <stdio.h>
#include <string.h>
#include <stdlib.h>
 #include <locale.h>

typedef struct {
  char descricao[50];
  float preco;
} tipoProduto;



int main() {
  tipoProduto *vet;
  FILE *f;
  char linha[1000];
  char *tok;
  int cont = 0;
  char teste[10]="teste";
  int x, tam;
  // setlocale(LC_ALL,"")
  // PROCURE MAIS INFO SOBRE ISSO. NAO SERÁ COBRADA EM PROVA
  // MOSTRADA APENAS PARA QUE SAIBAM QUE ELA EXISTE
  // MUDA A CONFIGURACAO DE DIVERSAS FUNCOES PARA A LINGUA CORRENTE
  // EXEMPLO: imprime virgulas ao inves de ponto em numeros reais
  // 3,5 ao invés de 3.5


  setlocale(LC_ALL,"");

  f = fopen("listadeProdutos","r");


  // AQUI EXEMPLO DE SCANF LENDO NUMERO DIRETO DE ARQUIVO. O ARQUIVO DEVE SER ASCII
  // NOTEM QUE O \n É NECESSÁRIO. DO CONTRARIO ELE NAO LERIA O \n após o número
  fscanf(f,"%d\n",&tam);
  //  fread(&tam,sizeof(char),1,f);
  printf("Numero de itens: %d\n",tam);
  vet = malloc(sizeof(tipoProduto)*tam);

  // AQUI MOSTRO COMO SCANF PODE SER USADA PARA LER INCLUSIVE STRINGS COM ESPACOS. %[] lê strings aceitando letras que estão especificadas dentro dos []. Pode-se especificar intervalos. Ela para de ler assim que achar algo fora da especificacao.
  // Notem que o %f é usado para ler um número. Em minha máquina, o setlocale faz os números serem tratados com vígulas ao invés de pontos
  // Notem o uso do %* para "pular" o separador (:) e espaços que existam nele
  // Retorno da fscanf é EOF se o arquivo já acabou. EOF é uma constante definida no stdio.h
  // Se nao está no fim de arquivo, retorna o número de simbolos convertidos. No exemplo abaixo seria 2 (%* nao conta na conversao)

  while(fscanf(f,"%[ A-Za-z0-9áéíóúãõôâêà]%*[: ]%f\n",vet[cont].descricao,&vet[cont].preco)!=EOF ) {
    printf("[%s] %.2f\n",vet[cont].descricao,vet[cont].preco);
    cont++;
  }
}