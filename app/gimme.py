f = open("codes.txt", "r")

line = f.readline()
while line:
    line = f.readline().replace('\n', '')
    l = f"https://www.moex.com/ru/issue.aspx?code={line}"
    print(l)
