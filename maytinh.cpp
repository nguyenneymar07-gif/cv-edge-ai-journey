#include <iostream>
#include <string>

    int main(){
    while (true) {
    float a,b;
    std::string op;
    std::cout << "enter one operator (+,-,*,/) or 'q' to quit: ";
    std::cin >> op;
    if ( op == "q") {
        break;
    }
    if (op != "+" && op != "-" && op != "*" && op != "/") {
        std::cout << "Error: Invalid operator!" << std::endl;
        continue;
    }
    std::cout << "Please enter first number: ";
    std::cin >> a;
    std::cout << "Please enter second number: ";
    std::cin >> b;
    if ( op == "+") {
        std::cout << a+b << std::endl;
    } else if ( op == "-") {
        std::cout << a-b << std::endl;
    } else if ( op == "*") {
        std::cout << a*b << std::endl;
    } else if ( op == "/") {
        if (b == 0) {
            std::cout << "Error: Division by zero is not allowed!" << std::endl;
            continue;
        } else {
            std::cout << a/b << std::endl;
        }
    }
    continue;
} }