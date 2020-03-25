#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <cstring>

using namespace std;

class Map
{
public:
  char *data;
  int rows;
  int cols;

  // Map: a rows * cols map
  Map(char *data, int rows, int cols)
  {
    this->data = data;
    this->rows = rows;
    this->cols = cols;
  }

  // Accesses the map data at location (row, col)
  char get(int row, int col)
  {
    check(row, col);
    return data[row * cols + col];
  }

  // Sets the map data at location (row, col)
  void set(int row, int col, char c)
  {
    check(row, col);
    data[row * cols + col] = c;
  }

  // Checks if out of range
  void check(int row, int col)
  {
    if (row < 0 or row >= rows or col < 0 or col >= cols)
      throw range_error("Range error when get data of map.");
  }

  // Returns a copy of this Map
  Map clone()
  {
    char *new_data = new char[rows * cols];
    memcpy(new_data, this->data, rows * cols);
    return Map(new_data, rows, cols);
  }
};

Map read_data(int argc, char *argv[])
{
  // check arguments
  if (argc < 2)
  {
    throw invalid_argument("Please specify input file.");
  }

  string file_name(argv[1]);
  ifstream infile;
  // check whether the input file exists
  infile.open(file_name, ios::in);
  if (!infile)
    throw runtime_error("The input file does not exist: " + file_name);
  if (!infile.is_open())
    throw runtime_error("Open file failed: " + file_name);

  // read input
  string raw_data;
  vector<vector<char>> map_data;
  int line_size = -1;
  while (!infile.eof())
  {
    infile >> raw_data;
    if (line_size = -1)
      line_size = raw_data.size();
    else if (line_size != raw_data.size())
      throw runtime_error("Please check size of input matrix.");
    map_data.push_back(vector<char>(raw_data.begin(), raw_data.end()));
  }
  // convert data to return type
  int rows = map_data.size(), cols = map_data[0].size();
  char *map_buffer = new char[rows * cols];
  for (int i = 0; i < rows; i += 1)
    memcpy(map_buffer + i * cols, map_data[i].data(), sizeof(char) * cols);

  return Map(map_buffer, rows, cols);
}

void solve(Map input_map)
{
  // we try to enter labyrinth from outside
  int rows = input_map.rows, cols = input_map.cols;
  // Position: defines where to enter the labyrinth
  struct Position
  {
    int row;
    int col;
  };
  vector<Position> enter_points;
  for (int row = 0; row < rows; row += rows - 1)
    for (int col = 0; col < cols; col += 1)
      if (input_map.get(row, col) == '.')
        enter_points.push_back(Position({row, col}));

  // PosWithCount: defines a position with a map and the length of traversed path
  struct PosWithCount
  {
    int row;
    int col;
    int count;
    Map map;
  };

  PosWithCount final_pos({0, 0, 0, input_map.clone()});

  // For each enter point, we traverse the labyrinth by DFS
  for (Position enter_point : enter_points)
  {
    // we do DFS with iterative style, which needs a stack to store the state of each step
    vector<PosWithCount> next_points = {PosWithCount({enter_point.row, enter_point.col, 0, input_map.clone()})};
    while (!next_points.empty())
    {
      PosWithCount current_postion = next_points.back();
      int row = current_postion.row, col = current_postion.col, count = current_postion.count;
      Map &map = current_postion.map;

      next_points.pop_back();
      if (map.get(row, col) != '.')
        continue;
      // update max length of path
      map.set(row, col, (char)(count % 10 + 48));
      if (count > final_pos.count)
      {
        final_pos = PosWithCount({row, col, count, map});
      }
      // explore adjacent points
      int ADJ_COUNT = 4;
      // indicates the shift of row index and col index
      int adj_point[ADJ_COUNT][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
      for (int i = 0; i < ADJ_COUNT; i += 1)
      {
        int dr = adj_point[i][0], dc = adj_point[i][1];
        int next_row = row + dr, next_col = col + dc;
        if (next_row < 0 or next_row >= rows or next_col < 0 or next_col >= cols)
          continue;
        if (map.get(next_row, next_col) != '.')
          continue;
        next_points.push_back(PosWithCount({next_row, next_col, count + 1, map.clone()}));
      }
    }
  }

  // output result
  cout << final_pos.count << endl;
  for (int r = 0; r < final_pos.map.rows; r += 1)
  {
    for (int c = 0; c < final_pos.map.cols; c += 1)
      cout << final_pos.map.get(r, c);
    cout << endl;
  }
}

int main(int argc, char *argv[])
{
  Map map = read_data(argc, argv);
  // Finding the longest pathway in an undirected graph is NP-hard,
  // So we use DFS to solve it in exponential time.
  solve(map);
}