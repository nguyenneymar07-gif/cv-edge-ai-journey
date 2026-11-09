#include <iostream>
#include <fstream>
#include <vector>

int main() {
    std::ifstream f("so.txt");
    if (!f.is_open()){
        std::cout << "loi: kh mo duoc file so.txt" << std::endl;
        return 1;
    }
    std::vector<float> so;
    float x;
    while (f >> x) {
        so.push_back(x);
    }if (so.empty()) {
        std::cout << "file khong co so nao" << std::endl;
        return 1;
    }
    float tong = 0;
    int n = so.size();
    float min = so[0];
    float max = so[0];
    for (int i=0; i < so.size(); i++) {
        tong += so[i];
        if (min > so[i]) min = so[i];
        if (max < so[i]) max = so[i];
    }
    float tb = tong / n ;
    std::cout << "TONG = " << tong <<std::endl;
    std::cout << "TRUNG BINH = " << tb << std ::endl;
    std::cout << "GIA TRI MIN = " << min << std::endl;
    std::cout << "GIA TRI MAX = " << max << std::endl;
    f.close();
    return 0;
}