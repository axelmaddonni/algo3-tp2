# algo3-tp2
algo3-tp2 1c 2016

Para compilar el codigo en C++ se debe compilar el archivo XYZ.cpp con el codigo del programa:

        g++ XYZ.cpp -O2 -o XYZ

Para compilar el codigo en Java se debe compilar con:

        javac XYZ.java

Luego para testear utilizando, por ejemplo, el caso de prueba número T se debe correr el siguiente comando:

        java -jar XYZTester.jar -exec XYZ -test T

Si se usa el código en C++ XYZ es el nombre del ejecutable que se genera al compilar, y si se usa el código en Java XYZ es "java XYZ" siendo XYZ el nombre del archivo .class que genera javac

El argumento de -test es el número de test que se correra, siendo todos los tests generados al azar.

A modo de ejemplo: Se tiene el archivo HolaMundo.cpp entonces se compila

g++ HolaMundo.cpp -O2 -o HolaMundo

Y se corre con

java -jar HolaMundoTester.jar -exec ./HolaMundo -test 1

El ./ es importante porque sino el tester busca HolaMundo en el path y es probable que el directorio donde están trabajando no esté en el path
