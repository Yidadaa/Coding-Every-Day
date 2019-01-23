#include<iostream>
#include<cmath>
using namespace std;

#include <Eigen/Core>
#include <Eigen/Geometry>

#include "sophus/so3.hpp"
#include "sophus/se3.hpp"

int main(int argc, char const *argv[])
{
    // SO(3) operations
    // rotate according Z axis
    Eigen::Matrix3d R = Eigen::AngleAxisd(M_PI / 2, Eigen::Vector3d(0, 0, 1)).toRotationMatrix();

    Sophus::SO3<double> SO3_R(R);
    Eigen::Quaterniond q(R);
    Sophus::SO3<double> SO3_q(q);

    cout << "SO3 from matrix: " << SO3_R.log().transpose() << endl;
    cout << "SO3 from quaterninon: " << SO3_q.log().transpose() << endl;

    Eigen::Vector3d so3 = SO3_R.log();

    cout << "SO3 hat: \n" << Sophus::SO3<double>::hat(so3).transpose() << endl;

    cout << "SO3 hat vee: " << Sophus::SO3<double>::vee(Sophus::SO3<double>::hat(so3)).transpose() << endl;

    Eigen::Vector3d delta_so3(1e-4, 0, 0);
    Sophus::SO3<double> SO3_updated = Sophus::SO3<double>::exp(delta_so3) * SO3_R;
    cout << "SO3 updated: " << SO3_updated.log().transpose() << endl;

    // SE(3) operations
    // translate according to X axis
    Eigen::Vector3d t(1, 0, 0);
    Sophus::SE3<double> SE3_Rt(R, t);
    Sophus::SE3<double> SE3_Qt(q, t);
    cout << "SE3 from R, t: \n" << SE3_Rt.log().transpose() << endl;
    cout << "SE3 from q, t: \n" << SE3_Qt.log().transpose() << endl;

    typedef Eigen::Matrix<double, 6, 1> Vector6d;

    Vector6d se3 = SE3_Rt.log();
    cout << "SE3: \n" << se3.transpose() << endl;

    Sophus::Matrix<double, 4, 4> SE3_hat = Sophus::SE3<double>::hat(se3);

    cout << "SE3 hat: \n" << SE3_hat << endl;
    cout << "SE3 hat vee: \n" << Sophus::SE3<double>::vee(SE3_hat).transpose() << endl;

    Vector6d delta_se3;
    delta_se3.setZero();
    delta_se3(0, 0) = 1e-4;
    Sophus::SE3<double> SE3_updated = Sophus::SE3<double>::exp(delta_se3) * SE3_Rt;
    cout << "SE3 updated: \n" << SE3_updated.matrix() << endl;

    return 0;
}
