#include "corners.hpp"

using namespace cv;
using namespace std;

std::vector<Point> scry_corners(Mat img) {
  std::vector<Point> corners;
  corners.push_back(Point(10, 10));
  corners.push_back(Point(100, 10));
  corners.push_back(Point(100, 100));
  corners.push_back(Point(10, 100));
  return corners;
}

void draw_corners(Mat img, std::vector<Point> corners) {
  Point lastPoint = corners[0];
  Scalar green = Scalar(0, 255, 0);
  for (std::vector<Point>::size_type i = 1; i <= corners.size(); i++) {
    line(img, lastPoint, corners[i % corners.size()], green, 2);
    lastPoint = corners[i % corners.size()];
  }
}