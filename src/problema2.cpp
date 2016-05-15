#include "problema2.h"

#include <chrono>
#include <cstddef>
#include <limits>

// Función para debugear.
void printVertexVector(std::vector<Vertex>& vs) {
  std::cerr << "{";
  for(const Vertex& v : vs) {
    std::cerr << "(" << v.key<< ", " << v.value << "), ";
  }
  std::cerr << "}" << std::endl;
}

MinHeap::MinHeap(const std::vector<Vertex>& v)
  : a(v), pos(v.size(), 0) {
  for (int i = a.size() / 2; i >= 0; i--) {
    MinHeapify(i);
  }
  for (int i = 0; inbound(a, i); i++) {
    pos[a[i].key] = i;
  }
}

Vertex MinHeap::Top() const {
  return a[0];
}

Vertex MinHeap::Pop() {
  Vertex minimum = a[0];
  // El primero deja de existir.
  pos[a[0].key] = -1;
  // El ultimo pasa a estar arriba de todo.
  pos[a[a.size() - 1].key] = 0;

  // El ultimo pasa estar arriba de todo.
  a[0] = a[a.size() - 1];
  // Achico el vector.
  a.resize(a.size() - 1);
  
  // Bajo la raiz hasta dejarlo todo bien.
  MinHeapify(0);
  return minimum;
}

void MinHeap::DecValue(int v, int new_value) {
    // Consigo el indice de v.
    int i = pos[v];
    // Le pongo el nuevo valor.
    a[i].value = new_value;
 
    // Voy para arriba "heapificando" el array.
    while (i > 0 && a[i].value < a[parent(i)].value) {
        // Lo cambio con su padre.
        pos[a[i].key] = parent(i);
        pos[a[parent(i)].key] = i;
        swap(a, i, parent(i));
        i = parent(i);
    }
}

inline size_t MinHeap::Size() const {
  return a.size();
}

void MinHeap::MinHeapify(int i) {
    int smallest = i;
    int l = left(i);
    int r = right(i);

    if (inbound(a, l) && a[l].value < a[smallest].value)
      smallest = l;
    if (inbound(a, r) && a[r].value < a[smallest].value)
      smallest = r;
 
    if (smallest != i) { 
        // Los vertices que tengo que cambiar.
        Vertex smallest_vertex = a[smallest];
        Vertex index_vertex = a[i];
        // Cambio las posiciones.
        pos[smallest_vertex.key] = i;
        pos[index_vertex.key] = smallest;
        // Cambio los vertices.
        swap(a, smallest, i);
        // Aplico MinHeapify para abajo.
        MinHeapify(smallest);
    }
}

std::vector<std::pair<int, int>> prim(
    MinHeap& heap, std::vector<VerticesAdyacentes> adj_list) {
  std::vector<std::pair<int, int>> parent(heap.Size(), std::make_pair(0, 0));

  while (heap.Size() > 0) {
    Vertex min_vertex = heap.Pop();
    int u = min_vertex.key;

    for (const auto& vertex_and_weight :  adj_list[u]) {
      int v = vertex_and_weight.first;
      int weight = vertex_and_weight.second;
      if (heap.At(v) && weight < heap.Value(v)) {
        parent[v].first = u;
        parent[v].second = weight;
        heap.DecValue(v, weight);
      }
    }
  }
  return std::move(parent);
}


int main() {
  int n, m;
  std::cin >> n >> m;
  std::vector<VerticesAdyacentes> adj_list(n, VerticesAdyacentes());

  for (int i = 0; i < m; i++) {
    int ai, bi, li;
    std::cin >> ai >> bi >> li;
    adj_list[ai].push_back(std::make_pair(bi, li));
    adj_list[bi].push_back(std::make_pair(ai, li));
  }

  std::chrono::time_point<std::chrono::system_clock> start, end;
  start = std::chrono::system_clock::now(); /* Empezamos medicion de tiempo */

  std::vector<Vertex> v_inicial;
  v_inicial.push_back({.key = 0, .value = 0});
  for (int i = 1; i < n; i++) {
    v_inicial.push_back({.key = i, .value = std::numeric_limits<int>::max()});
  }
  MinHeap h(v_inicial);  
  std::vector<std::pair<int, int>> resultado = prim(h, adj_list);

  end = std::chrono::system_clock::now(); /* Terminamos medicion de tiempo */
  #ifdef TOMAR_TIEMPO
  std::cerr << std::chrono::duration<double>(end - start).count();
  #endif

  int litros = 0;
  for (const auto& x : resultado) {
    litros += x.second;
  }

  std::cout << litros << std::endl;
  for (size_t i = 1; i < resultado.size(); i++) {
    std::cout << resultado[i].first << std::endl;
  }
}
