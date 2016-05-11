#include <chrono>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;
typedef int vertice;
typedef vector<vertice> VerticesAdyacentes;
typedef vector<VerticesAdyacentes> ListaAdyacencia;

vector<vertice> bfs(ListaAdyacencia vs, vertice root, vertice target, int n) {
  queue<vertice> c;
  vector<int> distancia(n, -1); 
  vector<int> acm(n, -1);
  vertice actual;
  distancia[root] = 0;
  acm[root] = root;
  c.push(root);
  while (!c.empty()) {
    actual = c.front();   
    c.pop();
    VerticesAdyacentes vecinos = vs[actual];
    for (const vertice& v : vecinos) {
      if (distancia[v] == -1) {
        distancia[v] = distancia[actual]+1;
        acm[v] = actual;
        if(v == target) break;
        c.push(v);
      }
    }
  }
  //Tengo que reconstruir el camino de atrás 
  //para adelante
  int long_sol = distancia[target]-1;
  vector<vertice> solucion(long_sol, 0);
  //Arranco en el padre del nodo n-1
  vertice v = acm[target];

  for (int i = long_sol - 1; i >= 0; i--) {
    solucion[i] = v;
    v = acm[v];
  }

  return solucion;
}


int main() {
  int n, m;
  cin >> n >> m;
  vector<vector<int>> input;
  for (int i = 0; i < m; i++) {
    int ai, bi, ei;
    cin >> ai >> bi >> ei;
    input.push_back(vector<int>({ai, bi, ei}));
  }

  std::chrono::time_point<std::chrono::system_clock> start, end;
  start = std::chrono::system_clock::now(); /* Empezamos medicion de tiempo */
  ListaAdyacencia adj_list(3*n, VerticesAdyacentes());
  for (const vector<int>& arista : input) {
    int ai = arista[0], bi = arista[1];
    bool ei = arista[2];
    if (ei) {
      adj_list[ai].push_back(bi + n);
      adj_list[ai + n].push_back(bi + 2*n);
      adj_list[bi].push_back(ai + n);
      adj_list[bi + n].push_back(ai + 2*n);
    } else {
      adj_list[ai].push_back(bi);
      adj_list[bi].push_back(ai);
      adj_list[ai + n].push_back(bi + n);
      adj_list[bi + n].push_back(ai + n);
    }

    adj_list[ai + 2*n].push_back(bi + 2*n);
    adj_list[bi + 2*n].push_back(ai + 2*n);
  }

  vector<vertice> solucion = bfs(adj_list, 0, 3*n-1, 3*n);
  end = std::chrono::system_clock::now(); /* Terminamos medicion de tiempo */
  #ifdef TOMAR_TIEMPO
  std::cerr << std::chrono::duration<double>(end - start).count();
  #endif
  
  cout << solucion.size() + 1 << endl;
  for (const int s : solucion) {
    cout << s % n << " ";
  }
  cout << endl;
}
