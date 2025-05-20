from SinhVien import SinhVien

class QuanLySinhVien:
    listSinhVien = []

    def generateID(self):
        maxID = 1
        if (self.soLuongSinhVien() > 0):
            maxID = self.listSinhVien[0].id
            for sv in self.listSinhVien:
                if (maxID < sv.id):
                    maxID = sv.id
            maxID = maxID + 1
        return maxID

    def soLuongSinhVien(self):
        return self.listSinhVien.__len__()

    def nhapSinhVien(self):
        svID = self.generateID()
        name = input("Nhap ten sinh vien: ")
        sex = input("Nhap gioi tinh sinh vien: ")
        major = input("Nhap chuyen nganh cua sinh vien: ")
        diemTB = float(input("Nhap diem cua sinh vien: "))
        sv = SinhVien(svID, name, sex, major, diemTB)
        self.xepLoaiHocLuc(sv)
        self.listSinhVien.append(sv)

    def updateSinhVien(self, ID):
        sv = self.findByID(ID)
        if (sv != None):
            name = input("Nhap ten sinh vien: ")
            sex = input("Nhap gioi tinh sinh vien: ")
            major = input("Nhap chuyen nganh cua sinh vien: ")
            diemTB = float(input("Nhap diem cua sinh vien: "))
            sv.name = name
            sv.sex = sex
            sv.major = major
            sv.diemTB = diemTB
            self.xepLoaiHocLuc(sv)
        else:
            print("Sinh vien co ID = {} khong ton tai.".format(ID))

    def sortByID(self):
        self.listSinhVien.sort(key=lambda x: x.id, reverse=False)

    def sortByName(self):
        self.listSinhVien.sort(key=lambda x: x.name, reverse=False)

    def sortByDiemTB(self):
        self.listSinhVien.sort(key=lambda x: x.diemTB, reverse=False)

    def findByID(self, ID):
        searchResult = None
        if (self.soLuongSinhVien() > 0):
            for sv in self.listSinhVien:
                if (sv.id == ID):
                    searchResult = sv
        return searchResult

    def findByName(self, keyword):
        listSV = []
        if (self.soLuongSinhVien() > 0):
            for sv in self.listSinhVien:
                if (keyword.upper() in sv.name.upper()):
                    listSV.append(sv)
        return listSV

    def deleteByID(self, ID):
        isDeleted = False
        sv = self.findByID(ID)
        if (sv != None):
            self.listSinhVien.remove(sv)
            isDeleted = True
        return isDeleted

    def xepLoaiHocLuc(self, sv):
        if (sv.diemTB >= 8):
            sv.hocLuc = "Gioi"
        elif (sv.diemTB >= 6.5):
            sv.hocLuc = "Kha"
        elif (sv.diemTB >= 5):
            sv.hocLuc = "Trung binh"
        else:
            sv.hocLuc = "Yeu"

    def showSinhVien(self, listSV):
        print("{:<8} {:<18} {:<8} {:<8} {:<8} {:<8}".format("ID", "Name", "Sex", "Major", "Diem TB", "Hoc Luc"))
        if (listSV.__len__() > 0):
            for sv in listSV:
                print("{:<8} {:<18} {:<8} {:<8} {:<8} {:<8}".format(sv.id, sv.name, sv.sex, sv.major, sv.diemTB, sv.hocLuc))
        print("\n")

    def getListSinhVien(self):
        return self.listSinhVien