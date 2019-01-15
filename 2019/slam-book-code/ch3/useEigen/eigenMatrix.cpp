#include <iostream>
#include <ctime>
using namespace std;

// import eigen
#include <Eigen/Core>
#include <Eigen/Dense>

#define MATRIX_SIZE 50

int main(int argc, char const *argv[])
{
    Eigen::Matrix<float, 2, 3> matrix_23;
    Eigen::Vector3d v_3d;
    Eigen::Matrix3d matrix_33 = Eigen::Matrix3d::Zero();

    Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic> matrix_dynamic;
    Eigen::MatrixXd matrix_x;

    matrix_23 << 1,2,3,4,5,6;

    cout << matrix_23 << endl;

    for (int i = 0; i < 1; i++) {
        for (int j = 0; j < 2; j++) {
            cout << matrix_23(i, j) << endl;
        }
    }

    v_3d << 3, 2, 1;

    Eigen::Matrix<double, 2, 1> result = matrix_23.cast<double>() * v_3d;
    cout << result << endl;

    matrix_33 = Eigen::Matrix3d::Random();

    cout << matrix_33 << endl;
    cout << matrix_33.transpose() << endl;
    cout << matrix_33.sum() << endl;

    Eigen::SelfAdjointEigenSolver<Eigen::Matrix3d> eigen_solver (matrix_33.transpose() * matrix_33);

    cout << "Eigen values:\n" << eigen_solver.eigenvalues() << endl;
    cout << "Eigen vectors:\n" << eigen_solver.eigenvectors() << endl;

    // Solve Function: A * x = b
    Eigen::Matrix<double, MATRIX_SIZE, MATRIX_SIZE> A;
    A = Eigen::MatrixXd::Random(MATRIX_SIZE, MATRIX_SIZE);
    Eigen::Matrix<double, MATRIX_SIZE, 1> b;
    b = Eigen::MatrixXd::Random(MATRIX_SIZE, 1);

    clock_t start_t = clock();

    Eigen::Matrix<double, MATRIX_SIZE, 1> x = A.inverse() * b;
    cout << "Time use in normal inverse: " << 1000 * (clock() - start_t) / (double) CLOCKS_PER_SEC << "ms" << endl;
    // cout << "x = " << x << endl;

    start_t = clock();
    x = A.colPivHouseholderQr().solve(b);
    cout << "Time use in Qr composition is: " << 1000 * (clock() - start_t) / (double) CLOCKS_PER_SEC << "ms" << endl;
    // cout << "x = " << x << endl;

    return 0;
}
