#include <iostream>

void tang_theo_gia_tri(int x) { x++; }
void tang_theo_con_tro(int* x) { (*x)++; }
void tang_theo_tham_chieu(int& x) { x++; }
int main(){
    int* q = nullptr;
    if (q != nullptr) { 
        std::cout << *q; 
    } else {
        std::cout << "q chua tro vao dau"<< std::endl;
    }
    int a = 5;
    int n = 5;
    int* p = &a;
    std::cout <<"a = "<< a << std::endl;
    std::cout <<"&a = "<< &a << std::endl;
    std::cout <<"p = "<< p << std::endl;
    std::cout <<"*p = "<< *p << std::endl;
    *p = 10;
    std::cout <<"a sau khi *p = 10 : "<< a << std::endl;
    tang_theo_gia_tri(n);
    std::cout << "n sau khi tang theo gia tri: " << n << std::endl;

    tang_theo_con_tro(&n);
    std::cout << "n sau khi tang theo con tro: " << n << std::endl;

    tang_theo_tham_chieu(n);
    std::cout << "n sau khi tang theo tham chieu: " << n << std::endl;
    return 0;
}

