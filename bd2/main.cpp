#include <cstring>
#include <fstream>
#include <iostream>

using namespace std;

int main(int argc, char *argv[]){
    int size_block = 5;
    ifstream tempfile;
    string temp;
    system("stat -fc %s . > blocksize.txt");
    std::cout << std::ifstream("blocksize.txt").rdbuf();
    tempfile.open("blocksize.txt", ios::out);
    getline(tempfile,temp);
    char cvet[] = {temp[0],temp[1],temp[2],temp[3]};
    size_block = atoi(cvet);
    cout << size_block << endl;
}