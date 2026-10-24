#include <iostream>
int main() {
    float a,b;
    char op;
    std::cout << "Please enter first number: ";
    std::cin >> a;
    std::cout << "enter one operator (+,-,*,/): ";
    std::cin >> op;
    if (op != '+' && op != '-' && op != '*' && op != '/') {
        std::cout << "Error: Invalid operator!" << std::endl;
        return 1;
    }
    std::cout << "Please enter second number: ";
    std::cin >> b;
    if ( op == '+') {
        std::cout << a+b << std::endl;
    } else if ( op == '-') {
        std::cout << a-b << std::endl;
    } else if ( op == '*') {
        std::cout << a*b << std::endl;
    } else if ( op == '/') {
        if (b == 0) {
            std::cout << "Error: Division by zero is not allowed!" << std::endl;
        } else {
            std::cout << a/b << std::endl;
        }
    }
    return 0;
} 