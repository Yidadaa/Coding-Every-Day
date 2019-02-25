#include<iostream>
#include<g2o/core/base_vertex.h>
#include<g2o/core/base_unary_edge.h>
#include<g2o/core/block_solver.h>
#include<g2o/core/optimization_algorithm_levenberg.h>
#include<g2o/core/optimization_algorithm_gauss_newton.h>
#include<g2o/core/optimization_algorithm_dogleg.h>
#include<g2o/solvers/dense/linear_solver_dense.h>
#include<Eigen/Core>
#include<opencv2/core/core.hpp>
#include<cmath>
#include<chrono>

using namespace std;

// 曲线模型的顶点，模板参数：优化变量维度和数据模型
class CurveFittingVertex: public g2o::BaseVertex<3, Eigen::Vector3d> {
public:
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    virtual void setToOriginImpl() {
        _estimate << 0, 0, 0;
    }

    virtual void oplusImpl(const double* update) {
        _estimate += Eigen::Vector3d(update);
    }
    virtual bool read(istream& in) {}
    virtual bool write(ostream& out) const {}
};

// 误差模型，模板参数：观测值维度，类型，连接顶点类型
class CurveFittingEdge: public g2o::BaseUnaryEdge<1, double, CurveFittingVertex> {
public:
    double _x;
public:
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
    CurveFittingEdge(double x): BaseUnaryEdge(), _x(x) {}
    // 计算曲线模型误差
    void computeError() {
        const CurveFittingVertex* v = static_cast<const CurveFittingVertex*> (_vertices[0]);
        const Eigen::Vector3d abc = v->estimate();
        _error(0, 0) = _measurement - std::exp(abc(0, 0) * _x * _x + abc(1, 0) * _x + abc(2, 0));
    }
    virtual bool read(istream& in) {}
    virtual bool write(ostream& out) const {}
};

int main(int argc, char const *argv[])
{
    double a = 1.0, b = 2.0, c = 1.0;
    int N = 100;
    double w_sigma = 1.0;
    cv::RNG rng;
    double abc[3] = { 0, 0, 0 };

    vector<double> x_data, y_data;

    cout << "geneating data:" << endl;

    for (int i = 0; i < N; i++) {
        double x = i / 100.0;
        x_data.push_back(x);
        y_data.push_back(
            exp(a * x * x + b * x + c) + rng.gaussian(w_sigma)
        );
    }

    // 开始构建图优化
    // 矩阵块：每个误差项优化变量维度为3， 误差值维度为1
    typedef g2o::BlockSolver<g2o::BlockSolverTraits<3, 1>> Block;
    // 线性方程求解器：稠密的增量方程
    Block::LinearSolverType* linearSolver = new g2o::LinearSolverDense<Block::PoseMatrixType>();
    // g2o::LinearSolver<Eigen::Matrix<double, 3, 3, 0, 3, 3>>* linearSolver;
    Block* solver_ptr = new Block(linearSolver);
    // 梯度下降法，从GN，LM，DogLeg中选
    g2o::OptimizationAlgorithmLevenberg* solver = new g2o::OptimizationAlgorithmLevenberg(solver_ptr);
    // 可以使用其他可选的求解器
    // auto* solver = new g2o::OptimizationAlgorithmGaussNewton(unique_ptr<Block>(solver_ptr));
    // auto* solver = new g2o::OptimizationAlgorithmDogleg(unique_ptr<Block>(linearSolver));
    // 设置图模型
    g2o::SparseOptimizer optimizer;
    optimizer.setAlgorithm(solver);
    optimizer.setVerbose(true); // 打开调试输出

    // 向图中增加顶点
    auto* v = new CurveFittingVertex();
    v->setEstimate(Eigen::Vector3d(0, 0, 0));
    v->setId(0);
    optimizer.addVertex(v);

    // 向图中增加边
    for (int i = 0; i < N; i++) {
        auto* edge = new CurveFittingEdge(x_data[i]);
        edge->setId(i);
        edge->setVertex(0, v);
        edge->setMeasurement(y_data[i]);
        // 信息矩阵，协方差矩阵的逆
        edge->setInformation(Eigen::Matrix<double, 1, 1>::Identity() * 1 / (w_sigma * w_sigma));
        optimizer.addEdge(edge);
    }
    // 开始优化
    cout << "Start optimization" << endl;
    auto t1 = chrono::steady_clock::now();

    optimizer.initializeOptimization();
    optimizer.optimize(100);

    auto t2 = chrono::steady_clock::now();
    auto time_used = chrono::duration_cast<chrono::duration<double>>(t2 - t1);
    cout << "time cost: " << time_used.count() << "s." << endl;

    // 输出优化值
    Eigen::Vector3d abc_estimate = v->estimate();
    cout << "estimated model: " << abc_estimate.transpose() << endl;


    return 0;
}
