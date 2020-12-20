#include <iostream>
#include <string>

using namespace std;

class Organ {
public:
  Organ () {};

  string name = "Organ";
};

class Dick : public Organ {
public:
  Dick () {
    this->name = "Dick";
  };
};

class Arm : public Organ {
public:
  Arm () {
    this->name = "Arm";
  }
};

void place(Organ o) {
  cout << "Your " << o.name << " place here." << endl;
}

int main() {
  Arm arm;
  Dick dick;

  place(arm);
  place(dick);
}