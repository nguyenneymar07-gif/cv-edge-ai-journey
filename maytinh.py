# MÁY TÍNH PY
def maytinh():
    while True:
        a = input("Nhap so dau tien hoac 'q' de thoat: ")
        if a.lower() == "q":
            print("Da thoat khoi may tinh.")
            break
        try:
            float(a)
        except ValueError:
            print("Loi: Vui long nhap mot so hop le!")
            continue
        op = input("Nhap phep toan (+,-,*,/): ")
        if op not in ["+", "-", "*", "/"]:
            print("Loi: Phep toan khong hop le!")
            continue
        b = input("Nhap so thu hai: ")
        try:
            float(b)
        except ValueError:
            print("Loi: Vui long nhap mot so hop le!")
            continue
        if op == "+":
            print("ket qua: ",float(a)+float(b))
        elif op == "-":
            print("ket qua: ",float(a)-float(b))
        elif op == "*":
            print("ket qua: ",float(a)*float(b))
        elif op == "/":
            if float(b) == 0:
                print("Loi: Khong the chia cho 0!")
            else:
                print("ket qua: ",float(a)/float(b))
if __name__ == "__main__":
    maytinh()