#include "hamming.hpp"

using namespace std;

// Returns the Hamming distance between strings a and b.
// http://en.wikipedia.org/wiki/Hamming_distance
int hamming_distance(string a, string b) {
  int dist = 0;
  for (int i = 0; i < a.size(); i++) {
    if (a.at(i) != b.at(i)) {
      dist += 1;
    }
  }
  return dist;
}
