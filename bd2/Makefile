bd1_tp2: main.o meuParser.o tp2Hash.o tp2BplusTree.o
		g++ -o db1_tp2 main.cpp meuparser.cpp tp2BplusTree.cpp

main.o: main.cpp meuParser.cpp tp2Hash.cpp tp2BplusTree.cpp
		g++ -c main.cpp

	
meuParser.o: meuParser.cpp tp2Header.h 
			g++ -c meuParser.cpp

tp2Hash.o: tp2Hash.cpp tp2Header.h 
			g++ -c tp2Hash.cpp 

tp2BplusTree.o: tp2BplusTree.cpp tp2Header.h 
				g++ -c tp2BplusTree.cpp 

run:
	./bd1_tp2 entrada.csv

