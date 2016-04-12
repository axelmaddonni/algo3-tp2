CC = g++
CFLAGS = -O2 -Wall -Wextra --std=c++11
PYTHON = python2
TEST_CORRECTITUD = ./test/test-correctitud.sh
N_TESTS = 100

problema1: problema1.cpp
	$(CC) $(CFLAGS) problema1.cpp -o problema1

problema2: problema2.cpp
	$(CC) $(CFLAGS) problema2.cpp -o problema2

problema3: problema3.cpp
	$(CC) $(CFLAGS) problema3.cpp -o problema3


test2: problema2 
	$(TEST_CORRECTITUD) test/ElImperioContraatacaTester.jar ./problema2 $(N_TESTS)

clean:
	rm -rf problema1 problema2 problema3

