#include <string>
#include <vector>
using std::string;
using std::vector;

struct Point {
    string Id;
    float x;
    float y;
    float z;
    float bulge;
};

struct WallLine {
    string Id;
    Point startPoint;
    Point endPoint;
    float distance;
    float angle;
};

struct Region {
    vector<WallLine> walls;
    float area;
    float perimeter;
    Point center;
};
struct House {
    string Id;
    vector<WallLine> walls;
    vector<Region> regions;
};