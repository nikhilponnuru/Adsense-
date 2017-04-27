
import csv
f = open("ads.csv", "r")
def iteratecsv(keyword, url):
    # print(keyword)
    # print("11111111111111111111111111111")



    reader1 = csv.reader(f)
    for row in reader1:
        print("1", row)

        if (row[0] == keyword):
            if (row[2] == "ad"):
                print("ad nany ad", row[0])

                return "ok", row[0], row[1]

            else:
                print("non ad")




print(iteratecsv("monitor","ads.csv"))