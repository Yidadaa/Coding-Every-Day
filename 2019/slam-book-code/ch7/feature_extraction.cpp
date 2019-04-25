#include<iostream>
#include<opencv2/core/core.hpp>
#include<opencv2/features2d/features2d.hpp>
#include<opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

int main(int argc, char const *argv[])
{
    if (argc != 3) {
        cout << "Usage: feature_extraction img1 img2" << endl;
        return 1;
    }

    Mat img_1 = imread(argv[1], CV_LOAD_IMAGE_COLOR);
    Mat img_2 = imread(argv[2], CV_LOAD_IMAGE_COLOR);

    // 初始化
    vector<KeyPoint> keypoints_1, keypoints_2;
    Mat descriptiors_1, descriptiors_2;
    auto orb = ORB::create(500, 1.2f, 8, 31, 0, 2, ORB::HARRIS_SCORE, 31, 20);

    // step 1: 检测Oriented FAST角点
    orb->detect(img_1, keypoints_1);
    orb->detect(img_2, keypoints_2);

    // step 2: 根据角点计算BRIEF描述子
    orb->compute(img_1, keypoints_1, descriptiors_1);
    orb->compute(img_2, keypoints_2, descriptiors_2);

    Mat outimg_1;
    drawKeypoints(img_1, keypoints_1, outimg_1, Scalar::all(-1), DrawMatchesFlags::DEFAULT);
    imshow("ORB特征点", outimg_1);

    // step 3: 匹配两帧图片中的描述子，使用Hamming距离
    vector<DMatch> matches;
    BFMatcher matcher(NORM_HAMMING);
    matcher.match(descriptiors_1, descriptiors_2, matches);

    // step 4: 匹配点对筛选
    double min_dist = 10000, max_dist = 0;

    // 找出所有匹配之间的最小距离和最大距离，即最相似的点与最不同的点之间的距离
    for (int i = 0; i < descriptiors_1.rows; i++) {
        double dist = matches[i].distance;
        min_dist = dist < min_dist ? dist : min_dist;
        max_dist = dist > max_dist ? dist : max_dist;
    }

    cout << "Max dist and Min dist: " << max_dist << '\n' << min_dist << endl;

    // 当描述子之间的距离大于两倍的最小距离时，判定为匹配失效
    // 为了防止最小距离过小，设置min_dist最小阈值为15.0(经验值)
    min_dist = max(min_dist, 15.0);
    vector<DMatch> good_matches;
    for (int i = 0; i < descriptiors_1.rows; i++) {
        if (matches[i].distance <= min_dist * 2) {
            good_matches.push_back(matches[i]);
        }
    }

    // step 5: 绘制匹配结果
    Mat img_match, img_goodmatch;
    drawMatches(img_1, keypoints_1, img_2, keypoints_2, matches, img_match);
    drawMatches(img_1, keypoints_1, img_2, keypoints_2, good_matches, img_goodmatch);
    imshow("所有匹配点对", img_match);
    imshow("优化后的匹配点对", img_goodmatch);

    waitKey(0);

    return 0;
}
