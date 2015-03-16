#include "corners.hpp"

using namespace std;
using namespace cv;


float* detect_card_corners(cv::Mat image, float* corners) {
  Mat gray, blurred;
  cvtColor(image, gray, COLOR_BGR2GRAY);
  medianBlur(gray, blurred, 17);
//  find edges
  Mat edges;
  Canny(blurred, edges, 100, 100, 3);
  dilate(edges, edges, 0);
//  get edge lines
  vector<Vec4i> lines;
  HoughLinesP(edges, lines, 1, CV_PI/180, 200, 300, 100);

  imshow("test", edges);

  if (lines.empty()) {
    cout << "no card detected" << endl;
    return corners;
  } else {
    cout << "CARD DETECTED" << endl;
    for (size_t i = 0; i < lines.size(); i++) {
      line(image, Point(lines[i][0], lines[i][1]),
           Point(lines[i][2], lines[i][3]), Scalar(0, 0, 255), 3, 8);
    }
  }
  //  vertical = find_vertical_lines
  //  horizontal = find_horizontal_lines
  //  edges = [ top, left, bottom, right ]
  //  corners = intersections, [ top_left, top_right, bottom_right, bottom_left ]
  //  return corners

  // corners[0] = 0.0f;
  // corners[1] = 0.0f;
  // corners[2] = 0.0f;
  // corners[3] = 0.0f;
  return corners;
}
