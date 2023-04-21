#include<stdio.h>
#include<stdlib.h>
using namespace std;

//actions.cpp, modifiable_obj.cpp, and constants.cpp are all included
//in characters.cpp
#include "characters.cpp"

int testFunc1(int apples) {
    cout << "\ntestFunc1 executed!" << apples;
}

int testFunc2(int bears) {
    cout << "\ntestFunc2 executed!" << bears;
}

int testFunc3(int cats) {
    cout << "\ntestFunc3 executed!" << cats;
}

int main() {
    typedef int(*ActionFunctionPtr)(int a);

    ActionFunctionPtr funcs[3] = {testFunc1,testFunc2,testFunc3};

    for(int i=0; i<3; i++) {
        funcs[i](i);
    }
}