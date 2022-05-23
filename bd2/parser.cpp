#include <cstring>
#include <fstream>
#include <iostream>
#include<algorithm>

class Artigo {
    public:
    int id;
    char titulo[300];
    int ano;
    char autores[150];
    int citacoes;
    char atualizacao[15];
    char snippet[1024];
};

using namespace std;

int main(int argc, char* argv[]) {
    string line;
    ifstream myfile;
    size_t pos = 0;
    std::string delimiter = ";";
    string filename = argv[1];
    myfile.open(filename, ios::out);
    std::string token;
    int i;
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

    cout << "ACABOU!!!" << endl;

}




/*#include <string.h>
#include <stdio.h>

int main () {
   char str[80] = "This is - www.tutorialspoint.com - website";
   const char s[2] = "-";
   char *token;
   
   /* get the first token 
   token = strtok(str, s);
   
   /* walk through other tokens 
   while( token != NULL ) {
      printf( " %s\n", token );
    
      token = strtok(NULL, s);
   }
   
   return(0);
}*/