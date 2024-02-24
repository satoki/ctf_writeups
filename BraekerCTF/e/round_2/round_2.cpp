#include <iomanip>
#include <iostream>

int main() {
    float total = 0;

    for (int i = 0; i < 9; i++)
        total += 0.1;

    float requiredToAdd = 1.0 - total;

    std::cout << std::fixed << std::setprecision(30) << requiredToAdd << std::endl;

    return 0;
}