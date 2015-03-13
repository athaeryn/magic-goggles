#include <iostream>
#include <string>
#include <assert.h>

using namespace std;


int hamming_distance(string a, string b);


int main() {
  string a = "foo";
  string b = "bar";
  int distance = hamming_distance(a, b);
  cout << "Distance: " << distance << endl;
}


// Returns the Hamming distance between strings a and b.
// http://en.wikipedia.org/wiki/Hamming_distance
int hamming_distance(string a, string b) {
  assert(a.length() == b.length());
  int dist = 0;
  for (int i = 0; i < a.length(); i++) {
    if (a.at(i) != b.at(i)) {
      dist += 1;
    }
  }
  return dist;
}
