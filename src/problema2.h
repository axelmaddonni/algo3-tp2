#include <iostream>
#include <utility>
#include <vector>

struct Vertex {
  int key;
  int value;
};

// Para facilitar la lectura. El primer elemento es el otro vertice, y el
// segundo elemento es el costo de esa ruta.
typedef std::vector<std::pair<int, int>> VerticesAdyacentes;

// MinHeap de Vertices. Es la implementacion standard, solo que con algunos 
// detalles cambiados. Hubo que agregar el arreglo "pos" que nos permite hacer
// DecValue de manera rapida (logn). No implementamos funciones de insercion
// porque no hacen falta.
class MinHeap {
 public:
  MinHeap(const std::vector<Vertex>& v);

  inline Vertex Top() const;

  Vertex Pop();

  void DecValue(int i, int new_value);

  inline size_t Size() const;

  inline int At(int i) const {
    return pos[i] >= 0;
  }

  inline int Value(int i) const {
    return a[pos[i]].value;
  }

 private:
  inline int parent(int i) { return (i - 1) / 2; }
  inline int left(int i) { return 2 * i + 1; }
  inline int right(int i) { return 2 * i + 2; }

  template <typename X>
  inline void swap(std::vector<X>& a, int i, int j) {
    X temp = a[i]; a[i] = a[j]; a[j] = temp;
  }

  template <typename X>
  inline bool inbound(std::vector<X>& a, int i) {
    return i < (int) a.size();
  }
  
  void MinHeapify(int i);

  // Array interno.
  std::vector<Vertex> a;
  // Posiciones de los elementos. Invariante: a[pos[i]].key = i.
  std::vector<int> pos;
};


