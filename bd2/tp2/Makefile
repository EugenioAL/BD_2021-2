bd1_tp2: main.o tp2_parser.o tp2_hash.o tp2_bPlusTree.o
		g++ -o bd1_tp2 main.cpp tp2_parser.cpp tp2_bPlusTree.cpp tp2_hash.cpp

main.o: main.cpp tp2_parser.cpp tp2_hash.cpp tp2_bPlusTree.cpp
		g++ -c main.cpp

	
tp2_parser.o: tp2_parser.cpp tp2_header.h 
			g++ -c tp2_parser.cpp

tp2_hash.o: tp2_hash.cpp tp2_header.h 
			g++ -c tp2_hash.cpp 

tp2_bPlusTree.o: tp2_bPlusTree.cpp tp2_header.h 
				g++ -c tp2_bPlusTree.cpp 

run:
	./bd1_tp2 entrada.csv

clear:
		rm -rf *.bin
		rm -rf *.txt
		rm -rf *.o
		rm -rf *.out
		rm -rf *.exe
