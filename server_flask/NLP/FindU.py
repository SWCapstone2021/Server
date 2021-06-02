from basefunction.FindUMethod import *


def findyou():
    if __name__ == "__main__":
        i = input("기능번호: 1(extract subtitle), 2(ctrl+F), 3(Frequency)")

        if i == '1':
            URL = input("URL:")
            MakeVttFile(URL)
        if i == '2':
            SearchingValue = input("키워드입력:")
            URL = input("URL:")
            Ctrl_F(SearchingValue, URL)
        if i == '3':
            SearchingValue = input("키워드입력:")
            URL = input("URL:")
            Frequency(SearchingValue, URL)
