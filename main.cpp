#include <iostream>

#include <opencv2/highgui/highgui.hpp>
#include "src/corners.hpp"

using namespace std;
using namespace cv;

const string TEST_IMG = "/Users/mike/magic/goggles/sample_imgs/Forest.jpg";

int main() {
  namedWindow("goggles");

  Mat image = imread(TEST_IMG);

  vector<Point> corners = scry_corners(image);

  if (corners.empty()) {
    cout << "No corners found!" << endl;
  } else {
    cout << corners << endl;
    draw_corners(image, corners);
  }

  // TODO: detect card (get corners)
  // TODO: draw edges/corners
  // TODO: extract/warpPerspective card
  // TODO: retrieve phash of card
  // TODO: have the guesser guess

  imshow("goggles", image);
  waitKey(0);

  destroyWindow("goggles");
  return 0;
}


