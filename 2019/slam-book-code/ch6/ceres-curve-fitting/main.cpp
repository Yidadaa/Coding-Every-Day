#include<iostream>
#include<opencv2/core/core.hpp>
#include<ceres/ceres.h>
#include<chrono>

using namespace std;

struct CURVE_FITTING_COST {
    CURVE_FITTING_COST (double x, double y): _x(x), _y(y) {};
    template <typename T>
    bool operator() (const T* const abc, T* residual) const {
        // y - exp{ax^2 + bx + c}
        residual[0] = T(_y) - ceres::exp(abc[0] * T(_x) * T(_x) + abc[1] * T(_x) + abc[2]);
        return true;
    }

    const double _x, _y;
};

int main(int argc, char const *argv[])
{
    double a = 1.0, b = 2.0, c = 1.0; // 真实参数值
    int N = 100; // 数据点
    double w_sigma = 1.0; // 噪声的sigma值
    cv::RNG rng; // 使用opencv的随机数产生器
    double abc[3] = { 0, 0, 0 };

    vector<double> x_data, y_data;

    cout << "Generating data" << endl;

    for (int i = 0; i < N; i++) {
        double x = i / 100.0;
        x_data.push_back(x);
        y_data.push_back(
            exp(a * x * x + b * x + c) + rng.gaussian(w_sigma)
        );
    }

    // 构建最小二乘问题
    ceres::Problem problem;
    for (int i = 0; i < N; i++) {
        // 添加误差项，使用自动求导
        problem.AddResidualBlock(
            new ceres::AutoDiffCostFunction<CURVE_FITTING_COST, 1, 3>(new CURVE_FITTING_COST(x_data[i], y_data[i])),
            nullptr, abc
        );
    }

    // 配置求解器
    ceres::Solver::Options options;
    options.linear_solver_type = ceres::DENSE_QR; // 使用QR分解求解增量方程
    options.minimizer_progress_to_stdout = true; // 输出到标准输出
    

    ceres::Solver::Summary summary;
    auto t1 = chrono::steady_clock::now();
    ceres::Solve(options, &problem, &summary);
    auto t2 = chrono::steady_clock::now();

    auto time_used = chrono::duration_cast<chrono::duration<double>>(t2 - t1);
    cout << "Solve time: " << time_used.count() << " s." << endl;

    // 输出结果
    cout << summary.BriefReport() << endl;
    cout << "Estimated a, b, c = ";
    for (auto x:abc) cout << x << " ";
    cout << endl;

    return 0;
}
