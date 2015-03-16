#ifndef __CORNERS_INCLUDE__
#define __CORNERS_INCLUDE__

#include <iostream>

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

float* detect_card_corners(cv::Mat image, float* corners);

#endif // __CORNERS_INCLUDE__
