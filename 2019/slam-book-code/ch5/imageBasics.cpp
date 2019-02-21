#include<iostream>
#include<chrono>

using namespace std;

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

int main(int argc, char const *argv[])
{
    cv::Mat image;
    image = cv::imread(argv[1]);

    if (image.data == nullptr) {
        cout << "文件" << argv[1] << "不存在";
    }

    cout << "Width: " << image.cols << endl;
    cout << "Height: " << image.rows << endl;
    cout << "Channels: " << image.channels() << endl;
    cout << "Type: " << image.type() << endl;

    cv::imshow("image", image);
    cv::waitKey(0);

    chrono::steady_clock::time_point t1 = chrono::steady_clock::now(); // Timing
    for (size_t y = 0; y < image.rows; y++) {
        for (size_t x = 0; x < image.cols; x++) {
            unsigned char* row_ptr = image.ptr<unsigned char>(y); // Row y
            unsigned char* data_ptr = &row_ptr[x * image.channels()]; // Col x
            for (int c = 0; c < image.channels(); c++) {
                unsigned char data = data_ptr[c]; // Get data
            }
        }
    }

    chrono::steady_clock::time_point t2 = chrono::steady_clock::now();
    auto time_used = chrono::duration_cast<chrono::duration<double>>(t2 - t1);

    cout << "遍历图片耗时：" << time_used.count() << "s" << endl;

    cv::Mat image_2 = image;
    image_2(cv::Rect(0, 0, 40, 40)).setTo(0);

    cv::imshow("image", image);
    cv::waitKey(0);

    cv::Mat image_clone = image.clone();
    image_clone(cv::Rect(0, 0, 100, 100)).setTo(255);
    cv::imshow("image", image);
    cv::imshow("image clone", image_clone);
    cv::waitKey(0);

    cv::destroyAllWindows();
    return 0;
}
