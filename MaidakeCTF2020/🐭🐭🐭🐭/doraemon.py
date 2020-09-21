import matplotlib.pyplot as plt

s = open("flag.csv").readlines()
plot = 0

for i in s:
    if ",Pressed" in i:
        plot = 1
        i = i.replace(",Pressed","")
    if ",Released" in i:
        plot = 0
        i = i.replace(",Released","")
    i = i.replace("\n","")
    if plot == 1:
        x_y = i.split(",")
        plt.scatter(int(x_y[0]), -1*int(x_y[1]), color="#ff4500")
plt.show()