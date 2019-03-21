#include<iostream>
#include<Eigen/Core>
#include<Eigen/Geometry>
#include<chrono>
#include<opencv2/core/core.hpp>
#include<opencv2/features2d/features2d.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/calib3d/calib3d.hpp>
#include<g2o/core/base_vertex.h>
#include<g2o/core/base_unary_edge.h>
#include<g2o/core/block_solver.h>
#include<g2o/core/optimization_algorithm_levenberg.h>
#include<g2o/core/optimization_algorithm_gauss_newton.h>
#include<g2o/core/optimization_algorithm_dogleg.h>
#include<g2o/solvers/dense/linear_solver_dense.h>
#include<g2o/solvers/csparse/linear_solver_csparse.h>
#include<g2o/types/sba/types_six_dof_expmap.h>
#include<g2o/types/sba/types_sba.h>

using namespace std;
using namespace cv;

#define R_ R.at<double>

void bundleAdjustment(
    const vector<Point3f> points_3d,
    const vector<Point2f> points_2d,
    const Mat& K,
    Mat& R, Mat& t
);

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
};

void bundleAdjustment(
    const vector<Point3f> points_3d,
    const vector<Point2f> points_2d,
    const Mat& K,
    Mat& R, Mat& t
) {
    // 初始化g2o
    typedef g2o::BlockSolver<g2o::BlockSolverTraits<6, 3>>Block; // pose 维度为6，landmark维度为3
    Block::LinearSolverType* linearSolver = new g2o::LinearSolverCSparse<Block::PoseMatrixType>();
    Block* solver_ptr = new Block(linearSolver);
    g2o::OptimizationAlgorithmLevenberg* solver = new g2o::OptimizationAlgorithmLevenberg(solver_ptr);
    g2o::SparseOptimizer optimizer;
    optimizer.setAlgorithm(solver);

    // 设置顶点
    auto* pose = new g2o::VertexSE3Expmap();

    Eigen::Matrix3d R_mat;

    R_mat << 
        R_(0, 0), R_(0, 1), R_(0, 2),
        R_(1, 0), R_(1, 1), R_(1, 2),
        R_(2, 0), R_(2, 1), R_(2, 2);
    
    pose->setId(0);
    pose->setEstimate(g2o::SE3Quat(R_mat, Eigen::Vector3d(t.at<double>(0, 0), t.at<double>(1, 0), t.at<double>(2, 0))));
    optimizer.addVertex(pose);

    int index = 1;
    for (auto p:points_3d) {
        auto* point = new g2o::VertexSBAPointXYZ();
        point->setId(index++);
        point->setEstimate(Eigen::Vector3d(p.x, p.y, p.z));
        point->setMarginalized(true);
        optimizer.addVertex(point);
    }

    // 相机内参
    auto camera = new g2o::CameraParameters(
        K.at<double>(0, 0), Eigen::Vector2d(K.at<double>(0, 2), K.at<double>(1, 2)), 0
    );
    camera->setId(0);
    optimizer.addParameter(camera);

    // edges
    index = 1;
    for (auto p:points_2d) {
        auto* edge = new g2o::EdgeProjectXYZ2UV();
        edge->setId(index);
        edge->setVertex(0, dynamic_cast<g2o::VertexSBAPointXYZ*>(optimizer.vertex(index)));
        edge->setVertex(1, pose);
        edge->setMeasurement(Eigen::Vector2d(p.x, p.y));
        edge->setParameterId(0, 0);
        edge->setInformation(Eigen::Matrix2d::Identity());
        optimizer.addEdge(edge);
        index++;
    }

    auto t1 = chrono::steady_clock::now();
    optimizer.setVerbose(true);
    optimizer.initializeOptimization();
    optimizer.optimize(100);
    auto t2 = chrono::steady_clock::now();
    auto time_used = chrono::duration_cast<chrono::duration<double>>(t2 - t1);
    cout << "Optimization costs time: " << time_used.count() << " seconds." << endl;

    cout << "After optimization: " << endl;
    cout << "T = " << endl << Eigen::Isometry3d(pose->estimate()).matrix() << endl;
};

int main(int argc, char const *argv[])
{
    if (argc != 4) {
        cout << "Usage: feature_extraction img1 img2" << endl;
        return 1;
    }

    Mat img_1 = imread(argv[1], CV_LOAD_IMAGE_COLOR);
    Mat img_2 = imread(argv[2], CV_LOAD_IMAGE_COLOR);
    Mat dpth_1 = imread(argv[3], CV_LOAD_IMAGE_UNCHANGED);

    vector<KeyPoint> keypoints_1, keypoints_2;
    vector<DMatch> matches;
    
    matches = find_feature_matches(img_1, img_2, keypoints_1, keypoints_2);

    cout << "一共找到了: " << matches.size() << "组匹配点" << endl;

    vector<Point3f> pts_3d;
    vector<Point2f> pts_2d;

    for (auto m:matches) {
        ushort d = dpth_1.ptr<unsigned short>(int (keypoints_1[m.queryIdx].pt.y))[int(keypoints_1[m.queryIdx].pt.x)];
        if (d == 0) continue;
        float dd = d / 1000.0;
        Point2d p1 = pixel2cam(keypoints_1[m.queryIdx].pt, K);
        pts_3d.push_back(Point3f(p1.x * dd, p1.y * dd, dd));
        pts_2d.push_back(keypoints_2[m.trainIdx].pt);
    }

    cout << "3d-2d pairs: " << pts_3d.size() << endl;

    Mat r, t;
    solvePnP(pts_3d, pts_2d, K, Mat(), r, t, false, cv::SOLVEPNP_EPNP);
    Mat R;
    cv::Rodrigues(r, R);
    cout << "R = \n" << R << endl;
    cout << "r = \n" << r << endl;

    cout << "Calling ba:" << endl;
    bundleAdjustment(pts_3d, pts_2d, K, R, t);

    return 0;
}
