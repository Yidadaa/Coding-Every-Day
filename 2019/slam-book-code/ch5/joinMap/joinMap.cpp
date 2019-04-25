#include<iostream>
#include<fstream>

#include<opencv2/core/core.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<Eigen/Geometry>
#include<boost/format.hpp> // format string
#include<pcl/point_types.h>
#include<pcl/io/pcd_io.h>
#include<pcl/visualization/pcl_visualizer.h>
#include<pcl/visualization/cloud_viewer.h>

using namespace std;

int main(int argc, char const *argv[])
{
    vector<cv::Mat> colorImgs, depthImgs;
    vector<Eigen::Isometry3d, Eigen::aligned_allocator<Eigen::Isometry3d>> poses;

    ifstream fin("./pose.txt");
    if (!fin) {
        cerr << "Can not find pose.txt!" << endl;
        return 1;
    }

    // 处理位姿数据
    for (int i = 0; i < 5; i++) {
        boost::format fmt("./%s/%d.%s"); // format of image files
        colorImgs.push_back(cv::imread((fmt % "color" % (i + 1) % "png").str()));
        depthImgs.push_back(cv::imread((fmt % "depth" % (i + 1) % "pgm").str(), -1));

        // 开一个数组，用来放位姿数据
        double data[7] = { 0 };
        for (auto& d:data) {
            fin >> d;
        }
        Eigen::Quaterniond q(data[6], data[3], data[4], data[5]); // 四元数
        Eigen::Isometry3d T(q);
        T.pretranslate(Eigen::Vector3d(data[0], data[1], data[2]));
        poses.push_back(T);
    }

    // 计算点云数据并开始拼接
    // 处理相机内参
    double cx = 325.5, cy = 253.5, fx = 518.0, fy = 519.0;
    double depthScale = 1000.0;

    cout << "正在将图像转换为点云数据..." << endl;

    typedef pcl::PointXYZRGB PointT; // 点云数据类型
    typedef pcl::PointCloud<PointT> PointCloud;

    PointCloud::Ptr pointCloud(new PointCloud);

    for (int i = 0; i < 5; i++) {
        cout << i << " of 5\n";
        cv::Mat color = colorImgs[i];
        cv::Mat depth = depthImgs[i];
        Eigen::Isometry3d T = poses[i];

        const int step = color.step;
        const int channels = color.channels();

        // 逐像素处理点云数据
        for (int v = 0; v < color.rows; v++) {
            for (int u = 0; u < color.cols; u++) {
                unsigned int d = depth.ptr<unsigned short>(v)[u]; // 深度数据
                if (d == 0) continue;
                Eigen::Vector3d point;
                point[2] = double(d) / depthScale;
                point[0] = (u - cx) * point[2] / fx;
                point[1] = (v - cy) * point[2] / fy;

                Eigen::Vector3d pointWorld = T * point;

                PointT p;
                p.x = pointWorld[0];
                p.y = pointWorld[1];
                p.z = pointWorld[2];
                p.b = color.data[v * step + u * channels];
                p.g = color.data[v * step + u * channels + 1];
                p.r = color.data[v * step + u * channels + 2];
                pointCloud->points.push_back(p);
            }
        }
    }

    pointCloud->is_dense = false;
    cout << "点云共有" << pointCloud->size() << "个点" << endl;
    pcl::io::savePCDFileBinary("map.pcd", *pointCloud);

    return 0;
}
