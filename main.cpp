#include <iostream>
#include <string>
#include <assert.h>

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace cv;


// Corner stuff.
vector<Point> scry_corners(cv::Mat img);
void draw_corners(cv::Mat img, vector<Point> corners);


int main() {
  namedWindow("goggles");
  namedWindow("test");

  Mat image = imread("sample_imgs/Forest.jpg");

  vector<Point> corners = scry_corners(image);

  if (corners.empty()) {
    cout << "No corners found!" << endl;
  } else {
    cout << corners << endl;
    draw_corners(image, corners);
  }

  imshow("goggles", image);
  waitKey(0);

  /*
  VideoCapture stream(0);

  if (!stream.isOpened()) {
    cout << "Couldn't open camera!" << endl;
    return 1;
  }

  while (true) {
    Mat frame;
    stream.read(frame);

    // Reduce the size.
    pyrDown(frame, frame);

    // TODO: detect card (get corners)
    // TODO: draw edges/corners
    // TODO: extract/warpPerspective card
    // TODO: retrieve phash of card
    // TODO: have the guesser guess

    imshow("goggles", frame);

    if (waitKey(30) >= 0) break;
  }
  */

  destroyWindow("goggles");
  destroyWindow("test");
  return 0;
}



vector<Point> scry_corners(cv::Mat img) {
  vector<Point> corners;
  corners.push_back(Point(10, 10));
  corners.push_back(Point(100, 10));
  corners.push_back(Point(100, 100));
  corners.push_back(Point(10, 100));
  return corners;
}


void draw_corners(cv::Mat img, vector<Point> corners) {
  Point lastPoint = corners[0];
  Scalar green = Scalar(0, 255, 0);
  for (vector<Point>::size_type i = 1; i <= corners.size(); i++) {
    line(img, lastPoint, corners[i % corners.size()], green, 2);
    lastPoint = corners[i % corners.size()];
  }
}
