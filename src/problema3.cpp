#include <iostream>
#include <vector>
#include <tuple>
#include <list>
#include <algorithm> // min

using namespace std;

// La tupla corresponde a: (altura, distMinima, Mov: X o Z)
typedef tuple<int, int, char> Casilla;

// Definiciones
int solve(vector<vector<Casilla>>& t, int n, int m, int h);
int costo (vector<vector<Casilla>>& t, int h, int i, int j, int k, int l);

int main() {

  int n, m, h;
  cin >> n >> m >> h;

  vector<vector<Casilla>> Tablero(n, vector<Casilla>(m, Casilla()));

  for (int i = 0; i < n; i++){
  	for (int j = 0; j < m; j++){
  		int a;
      cin >> a;
  		get<0>(Tablero[i][j]) = a;
  	}
  }

  int distMinima = solve(Tablero, n, m, h);

  //Armo el camino mínimo
  list<char> camino;
  int i = n-1;
  int j = m-1;
  while (!(i == 0 && j == 0)){
  	char mov = get<2>(Tablero[i][j]);
  	camino.push_front(mov);
  	if (mov == 'Y'){
  		j--;
  	}else{
  		i--;
  	}
  }

  cout << distMinima << endl;

  for (list<char>::iterator it = camino.begin(); it != camino.end(); it++){
  	cout << *it << endl;
  }
  return 0;
}


int costo (vector<vector<Casilla>>& t, int h, int i, int j, int k, int l){
	if (abs(get<0>(t[i][j]) -  get<0>(t[k][l])) <= h ){
		return 0;
	}else{
		return (abs(get<0>(t[i][j]) -  get<0>(t[k][l])) - h);
	}
}


int solve(vector<vector<Casilla>>& t, int n, int m, int h){

	get<1>(t[0][0]) = 0;

	for (int j=1; j < m; j++){
		get<1>(t[0][j]) = get<1>(t[0][j-1]) + costo(t, h, 0, j-1, 0, j);
		get<2>(t[0][j]) = 'Y';
	}

	for (int i=1; i < n; i++){
		get<1>(t[i][0]) = get<1>(t[i-1][0]) + costo(t, h, i-1, 0, i, 0);
		get<2>(t[i][0]) = 'X';
	}

	for (int i=1 ; i < n; i++){
		for (int j=1; j < m; j++){
			get<1>(t[i][j]) = min(get<1>(t[i-1][j]) + costo(t,h, i-1,j,i,j), 
								  get<1>(t[i][j-1]) + costo(t,h, i,j-1,i,j) );

			if (get<1>(t[i][j]) == get<1>(t[i-1][j]) + costo(t,h, i-1,j,i,j)){
				get<2>(t[i][j]) = 'X';
			}else{
				get<2>(t[i][j]) = 'Y';
			}
		}
	}
	
	return get<1>(t[n-1][m-1]);
}