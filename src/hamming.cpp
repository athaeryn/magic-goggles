#include <assert.h>

#include "hamming.hpp"

// Returns the Hamming distance between strings a and b.
// http://en.wikipedia.org/wiki/Hamming_distance
int hamming_distance(std::string a, std::string b) {
  assert(a.size() == b.size());
  int dist = 0;
  for (int i = 0; i < a.size(); i++) {
    if (a.at(i) != b.at(i)) {
      dist += 1;
    }
  }
  return dist;
}
