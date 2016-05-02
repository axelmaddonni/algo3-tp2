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

test1: problema1
	$(TEST_CORRECTITUD) test/UnaNuevaEsperanzaTester.jar ./problema1 $(N_TESTS)

test2: problema2 
	$(TEST_CORRECTITUD) test/ElImperioContraatacaTester.jar ./problema2 $(N_TESTS)

test3: problema3
	$(TEST_CORRECTITUD) test/ElRetornoDelJediTester.jar ./problema3 $(N_TESTS)

test: N_TESTS = 10
test: test1 test2 test3

tiempos1: CFLAGS += -DTOMAR_TIEMPO
tiempos1: problema1
	$(PYTHON) exp/tiempos.py 1 20 100 5

tiempos2: CFLAGS += -DTOMAR_TIEMPO
tiempos2: problema2
	$(PYTHON) exp/tiempos.py 2 400 5000 20

tiempos3: CFLAGS += -DTOMAR_TIEMPO
tiempos3: problema3
	$(PYTHON) exp/tiempos.py 3 1 300 1


clean:
	rm -rf problema1 problema2 problema3

