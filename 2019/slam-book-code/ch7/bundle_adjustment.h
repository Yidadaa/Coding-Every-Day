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

#if !defined(BUNDLE_ADJUSTMENT_H_)
#define BUNDLE_ADJUSTMENT_H_

void bundleAdjustment(
    const vector<Point3f> points_3d,
    const vector<Point2f> points_2d,
    const Mat& K,
    Mat& R, Mat& t
);

#endif // BUNDLE_ADJUSTMENT_H_

