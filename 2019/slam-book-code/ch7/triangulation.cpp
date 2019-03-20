#include<iostream>
#include<opencv2/core/core.hpp>
#include<opencv2/features2d/features2d.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/calib3d/calib3d.hpp>

using namespace std;
using namespace cv;

#define R_MAT R.at<double>

// 对极约束
void pose_estimation_2d2d(
    vector<KeyPoint> keypoints_1,
    vector<KeyPoint> keypoints_2,
    vector<DMatch> matches,
    Mat& R, Mat& t);
// 寻找特征点
vector<DMatch> find_feature_matches(
    Mat img_1, Mat img_2,
    vector<KeyPoint>& keypoints_1,
    vector<KeyPoint>& keypoints_2);

// 三角测量
void triangulation(
    const vector<KeyPoint>& keypoint_1,
    const vector<KeyPoint>& keypoint_2,
    const vector<DMatch>& matches,
    const Mat& R, const Mat& t,
    vector<Point3d>& points
);

// 获得相机的归一化坐标
Point2d pixel2cam (const Point2d& p, const Mat& K);

// 相机内参
const Mat K = (Mat_<double>(3, 3) << 520.9, 0, 325.1, 0, 521.0, 249.7, 0, 0, 1);

void pose_estimation_2d2d(
    vector<KeyPoint> keypoints_1,
    vector<KeyPoint> keypoints_2,
    vector<DMatch> matches,
    Mat& R, Mat& t) {
    
    // 把匹配点转化为vector<Point2f>的形式
    vector<Point2f> points1, points2;
    for (int i = 0; i < matches.size(); i++) {
        points1.push_back(keypoints_1[matches[i].queryIdx].pt);
        points2.push_back(keypoints_2[matches[i].queryIdx].pt);
    }

    // 计算基础矩阵F
    Mat F;
    F = findFundamentalMat(points1, points2, CV_FM_8POINT);
    cout << "Fundamental Matrix is: " << endl << F << endl;

    // 计算本质矩阵
    Point2d principal_point(325.1, 249.7); // 光心，TUM dataset标定值
    int focal_length = 521; // 焦距
    Mat E;
    E = findEssentialMat(points1, points2, focal_length, principal_point, RANSAC);
    cout << "Essential Matrix is: " << endl << E << endl;

    // 计算单应矩阵
    Mat H;
    H = findHomography(points1, points2, RANSAC, 3, noArray(), 2000, 0.99);
    cout << "Homography Matrix is: " << endl << H << endl;

    // 从本质矩阵中恢复旋转和平移
    recoverPose(E, points1, points2, R, t, focal_length, principal_point);
    cout << "R is: " << R << endl;
    cout << "t is: " << t << endl;
};

vector<DMatch> find_feature_matches(
    Mat img_1, Mat img_2,
    vector<KeyPoint>& keypoints_1,
    vector<KeyPoint>& keypoints_2) {
    // Most code of this function is from './feature_extractino.cpp'

    Mat descriptiors_1, descriptiors_2;
    auto orb = ORB::create(500, 1.2f, 8, 31, 0, 2, ORB::HARRIS_SCORE, 31, 20);

    // step 1: 检测Oriented FAST角点
    orb->detect(img_1, keypoints_1);
    orb->detect(img_2, keypoints_2);

    // step 2: 根据角点计算BRIEF描述子
    orb->compute(img_1, keypoints_1, descriptiors_1);
    orb->compute(img_2, keypoints_2, descriptiors_2);

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

    // 当描述子之间的距离大于两倍的最小距离时，判定为匹配失效
    // 为了防止最小距离过小，设置min_dist最小阈值为15.0(经验值)
    min_dist = max(min_dist, 15.0);
    cout << "Max dist = " << max_dist << endl;
    cout << "Min dist = " << min_dist << endl;
    vector<DMatch> good_matches;
    for (int i = 0; i < descriptiors_1.rows; i++) {
        if (matches[i].distance <= min_dist * 2) {
            good_matches.push_back(matches[i]);
        }
    }

    return good_matches;
};

Point2d pixel2cam(const Point2d& p, const Mat& K) {
    return Point2d(
        ( p.x - K.at<double> ( 0,2 ) ) / K.at<double> ( 0,0 ),
        ( p.y - K.at<double> ( 1,2 ) ) / K.at<double> ( 1,1 )
    );
}

void triangulation(
    const vector<KeyPoint>& keypoint_1,
    const vector<KeyPoint>& keypoint_2,
    const vector<DMatch>& matches,
    const Mat& R, const Mat& t,
    vector<Point3d>& points
) {
    Mat T1 = (Mat_<double>(3, 4) << 
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0);
    Mat T2 = (Mat_<double>(3, 4) << 
        R_MAT(0, 0), R_MAT(0, 1), R_MAT(0, 2), R_MAT(0, 0),
        R_MAT(1, 0), R_MAT(1, 1), R_MAT(1, 2), R_MAT(1, 0),
        R_MAT(2, 0), R_MAT(2, 1), R_MAT(2, 2), R_MAT(2, 0)
    );
    vector<Point2d> pts_1, pts_2;
    for (auto m:matches) {
        pts_1.push_back(pixel2cam(keypoint_1[m.queryIdx].pt, K));
        pts_2.push_back(pixel2cam(keypoint_2[m.queryIdx].pt, K));
    }

    Mat pts_4d;
    cv::triangulatePoints(T1, T2, pts_1, pts_2, pts_4d);

    // 转换成齐次坐标
    for (int i = 0; i < pts_4d.cols; i++) {
        Mat x = pts_4d.col(i);
        x /= x.at<float>(3, 0); // 归一化
        points.push_back(Point3d(x.at<float>(0, 0), x.at<float>(1, 0), x.at<float>(2, 0)));
    }
};

int main(int argc, char const *argv[])
{
    if (argc != 3) {
        cout << "Usage: feature_extraction img1 img2" << endl;
        return 1;
    }

    Mat img_1 = imread(argv[1], CV_LOAD_IMAGE_COLOR);
    Mat img_2 = imread(argv[2], CV_LOAD_IMAGE_COLOR);

    vector<KeyPoint> keypoints_1, keypoints_2;
    vector<DMatch> matches;
    
    matches = find_feature_matches(img_1, img_2, keypoints_1, keypoints_2);

    cout << "一共找到了: " << matches.size() << "组匹配点" << endl;

    // 估计两张图之间的运动
    Mat R, t;
    pose_estimation_2d2d(keypoints_1, keypoints_2, matches, R, t);

    // 验证三角化点与特征点的重投影关系
    vector<Point3d> points;
    triangulation(keypoints_1, keypoints_2, matches, R, t, points);

    for (int i = 0; i < matches.size(); i++) {
        Point2d pt1_cam = pixel2cam(keypoints_1[matches[i].queryIdx].pt, K);
        Point2d pt1_cam_3d (
            points[i].x / points[i].z,
            points[i].y / points[i].z
        );
        cout << "Point in the first camear frame: " << pt1_cam << ", d = " << points[i].z << endl;
        cout << "Point projected from 3d: " << pt1_cam_3d << endl;

        // 第二幅图
        Point2f pt2_cam = pixel2cam(keypoints_2[matches[i].trainIdx].pt, K);
        Mat pt2_trans = R * (Mat_<double>(3, 1) << points[i].x, points[i].y, points[i].z) + t;

        pt2_trans /= pt2_trans.at<double>(2, 0);
        cout << "Point in the second camera frame: " << pt2_cam << endl;
        cout << "Point projected from second frame: " << pt2_trans.t() << endl;
    }

    return 0;
}
