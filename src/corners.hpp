#ifndef __CORNERS_INCLUDE__
#define __CORNERS_INCLUDE__

#include <opencv2/imgproc/imgproc.hpp>
#include <vector>

// Find the corners in an image.
std::vector<cv::Point> scry_corners(cv::Mat img);

// Plot the corners on the image.
void draw_corners(cv::Mat img, std::vector<cv::Point> corners);

#endif // __CORNERS_INCLUDE__
