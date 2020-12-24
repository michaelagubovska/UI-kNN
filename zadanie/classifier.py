#!/usr/bin/env python
from math import sqrt
from random import randrange
import matplotlib.pyplot as plotter

points = []                                                                        # pole objektov typy Point
state_space = []                                                                   # x a y suradnice bodov v priestore
num_of_points = 0                                                                  # pocet bodov na pridanie


class Point:                                                                       # trieda pre body v priestore
    def __init__(self, x, y, value, classified1, classified3, classified7, classified15):
        self.x = x                                                                 # suradnice x, y
        self.y = y
        self.value = value                                                         # povodna farba po vygenerovani
        self.classified1 = classified1                                             # farba dana klasifikatorom s k = 1
        self.classified3 = classified3                                             # farba dana klasifikatorom s k = 3
        self.classified7 = classified7                                             # farba dana klasifikatorom s k = 7
        self.classified15 = classified15                                           # farba dana klasifikatorom s k = 15


def calculate_distance(x1, y1, x2, y2):                                            # Euklidova vzdialenost dvoch bodov
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


def initialize_dataset():                                                          # prvych fixnych 20 bodov v priestore
    global points, state_space
    points.append(Point(-4500, -4400, "R", "R", "R", "R", "R"))
    points.append(Point(-4100, -3000, "R", "R", "R", "R", "R"))
    points.append(Point(-1800, -2400, "R", "R", "R", "R", "R"))
    points.append(Point(-2500, -3400, "R", "R", "R", "R", "R"))
    points.append(Point(-2000, -1400, "R", "R", "R", "R", "R"))
    points.append(Point(4500, -4400, "G", "G", "G", "G", "G"))
    points.append(Point(4100, -3000, "G", "G", "G", "G", "G"))
    points.append(Point(1800, -2400, "G", "G", "G", "G", "G"))
    points.append(Point(2500, -3400, "G", "G", "G", "G", "G"))
    points.append(Point(2000, -1400, "G", "G", "G", "G", "G"))
    points.append(Point(-4500, 4400, "B", "B", "B", "B", "B"))
    points.append(Point(-4100, 3000, "B", "B", "B", "B", "B"))
    points.append(Point(-1800, 2400, "B", "B", "B", "B", "B"))
    points.append(Point(-2500, 3400, "B", "B", "B", "B", "B"))
    points.append(Point(-2000, 1400, "B", "B", "B", "B", "B"))
    points.append(Point(4500, 4400, "P", "P", "P", "P", "P"))
    points.append(Point(4100, 3000, "P", "P", "P", "P", "P"))
    points.append(Point(1800, 2400, "P", "P", "P", "P", "P"))
    points.append(Point(2500, 3400, "P", "P", "P", "P", "P"))
    points.append(Point(2000, 1400, "P", "P", "P", "P", "P"))

    for i in range(20):                                              # pridame ich suradnice do pola stavoveho priestoru
        state_space.append([points[i].x, points[i].y])


def generate_red_point():                                            # generuje cerveny bod s 99% pravdepodobnostou
    if randrange(0, 101) > 0:
        x = randrange(-5000, 500)
        y = randrange(-5000, 500)
        while [x, y] in state_space:
            x = randrange(-5000, 500)
            y = randrange(-5000, 500)
    else:
        x = randrange(500, 5001)
        y = randrange(500, 5001)
        while [x, y] in state_space:
            x = randrange(500, 5001)
            y = randrange(500, 5001)

    return Point(x, y, "R", None, None, None, None)


def generate_green_point():                                          # generuje zeleny bod s 99% pravdepodobnostou
    if randrange(0, 101) > 0:
        x = randrange(-499, 5001)
        y = randrange(-5000, 500)
        while [x, y] in state_space:
            x = randrange(-499, 5001)
            y = randrange(-5000, 500)
    else:
        x = randrange(-5000, -499)
        y = randrange(500, 5001)
        while [x, y] in state_space:
            x = randrange(-5000, -499)
            y = randrange(500, 5001)

    return Point(x, y, "G", None, None, None, None)


def generate_blue_point():                                          # generuje modry bod s 99% pravdepodobnostou
    if randrange(0, 101) > 0:
        x = randrange(-5000, 500)
        y = randrange(-499, 5001)
        while [x, y] in state_space:
            x = randrange(-5000, 500)
            y = randrange(-499, 5001)
    else:
        x = randrange(500, 5001)
        y = randrange(-5000, -499)
        while [x, y] in state_space:
            x = randrange(500, 5001)
            y = randrange(-5000, -499)

    return Point(x, y, "B", None, None, None, None)


def generate_purple_point():                                        # generuje fialovy bod s 99% pravdepodobnostou
    if randrange(0, 101) > 0:
        x = randrange(-499, 5001)
        y = randrange(-499, 5001)
        while [x, y] in state_space:
            x = randrange(-499, 5001)
            y = randrange(-499, 5001)
    else:
        x = randrange(-5000, -499)
        y = randrange(-5000, -499)
        while [x, y] in state_space:
            x = randrange(-5000, -499)
            y = randrange(-5000, -499)

    return Point(x, y, "P", None, None, None, None)


def most_common_neighbor(colors):                                 # najde najcastejsie vyskytujucu sa farbu v okoli
    color = ""                                                    # ak viac s rovnakym poctom, vrati prvu najpocetnejsiu
    num = 0
    for key, value in colors.items():                             # prechadza slovnikom farieb a ich pocetnosti
        if value > num:
            color = key
            num = value

    return color                                                  # najpocestnejsia farba


def classify(x, y, k):                                            # klasifikator
    distances = {}
    neighbor_num = k
    colors = {"R": 0, "G": 0, "B": 0, "P": 0}
    if k == 1:
        for point in points:                                       # vypocet vzdialenosti bodu od bodov v stavovom priestore
            distances[calculate_distance(x, y, point.x, point.y)] = point.classified1
    elif k == 3:
        for point in points:                                       # vypocet vzdialenosti bodu od bodov v stavovom priestore
            distances[calculate_distance(x, y, point.x, point.y)] = point.classified3
    elif k == 7:
        for point in points:                                       # vypocet vzdialenosti bodu od bodov v stavovom priestore
            distances[calculate_distance(x, y, point.x, point.y)] = point.classified7
    else:
        for point in points:                                       # vypocet vzdialenosti bodu od bodov v stavovom priestore
            distances[calculate_distance(x, y, point.x, point.y)] = point.classified15

    distances_sorted = sorted(distances.items(),  key=lambda v: v[0])     # usporiada od najmensieho vzdialenosti

    for key, value in distances_sorted:                   # najde pocetnost farieb prvych k najblizsich bodov
        if neighbor_num == 0:
            break
        if value == "R":
            colors["R"] += 1
        elif value == "G":
            colors["G"] += 1
        elif value == "B":
            colors["B"] += 1
        elif value == "P":
            colors["P"] += 1

        neighbor_num -= 1

    return most_common_neighbor(colors)                  # vrati farbu najcastejsie vyskytujcej sa farby medzi k susedmi


def statistics(generated_points, k1, k3, k7, k15):               # vypis percentualnej uspesnosti klasifikatora
    print("Classification success rate of k = 1: ", k1/generated_points*100, "%")
    print("Classification success rate of k = 3: ", k3/generated_points*100, "%")
    print("Classification success rate of k = 7: ", k7/generated_points*100, "%")
    print("Classification success rate of k = 15: ", k15/generated_points*100, "%")


def check_color(original, classified):                   # kontrola, ci sa klasifikovana farba rovna tej vygenerovanej
    if original == classified:
        return True
    return False


def color_name(color):                                  # vrati nazov farby, ktorej je bod
    if color == "R":
        return 'red'
    elif color == "G":
        return 'green'
    elif color == "B":
        return 'blue'
    else:
        return 'purple'


def visualize(num):                                     # vizualizuje body v priestore podla zadaneho k
    x = []
    y = []
    colors = []

    for point in points:
        x.append(point.x)
        y.append(point.y)
        if num == 1:
            colors.append(color_name(point.classified1))
        elif num == 3:
            colors.append(color_name(point.classified3))
        elif num == 7:
            colors.append(color_name(point.classified7))
        else:
            colors.append(color_name(point.classified15))

    plotter.title("CLASSIFIED BY K=" + str(num) + " on " + str(len(x)) + " points")
    plotter.scatter(x, y, c=colors)
    plotter.show()


def main():
    global points, state_space, num_of_points
    k1, k3, k7, k15 = 0, 0, 0, 0
    initialize_dataset()
    print("Enter number of points you wish to generate")
    num_of_points = int(input())
    print("---------- k-N-N classifier starting on", num_of_points, "points ----------")

    generated_points = 0
    while generated_points < num_of_points:
        red = generate_red_point()                                   # vygeneruje cerveny bod
        state_space.append([red.x, red.y])                           # prida jeho suradnice do stavoveho priestoru
        color1 = classify(red.x, red.y, 1)                           # klasifikator bodu s k = 1
        if check_color("R", color1):                                 # zaznamena spravnu klasifikaciu
            k1 += 1
        color3 = classify(red.x, red.y, 3)                           # klasifikator bodu s k = 3
        if check_color("R", color3):
            k3 += 1
        color7 = classify(red.x, red.y, 7)                           # klasifikator bodu s k = 7
        if check_color("R", color7):
            k7 += 1
        color15 = classify(red.x, red.y, 15)                         # klasifikator bodu s k = 15
        if check_color("R", color15):
            k15 += 1
        points.append(Point(red.x, red.y, "R", color1, color3, color7, color15))
        # prida bod do zoznamu vsetkych bodov, aj s farbami

        green = generate_green_point()                               # to iste pre ostatne farby
        state_space.append([green.x, green.y])
        color1 = classify(green.x, green.y, 1)
        if check_color("G", color1):
            k1 += 1
        color3 = classify(green.x, green.y, 3)
        if check_color("G", color3):
            k3 += 1
        color7 = classify(green.x, green.y, 7)
        if check_color("G", color7):
            k7 += 1
        color15 = classify(green.x, green.y, 15)
        if check_color("G", color15):
            k15 += 1
        points.append(Point(green.x, green.y, "G", color1, color3, color7, color15))

        blue = generate_blue_point()
        state_space.append([blue.x, blue.y])
        color1 = classify(blue.x, blue.y, 1)
        if check_color("B", color1):
            k1 += 1
        color3 = classify(blue.x, blue.y, 3)
        if check_color("B", color3):
            k3 += 1
        color7 = classify(blue.x, blue.y, 7)
        if check_color("B", color7):
            k7 += 1
        color15 = classify(blue.x, blue.y, 15)
        if check_color("B", color15):
            k15 += 1
        points.append(Point(blue.x, blue.y, "B", color1, color3, color7, color15))

        purple = generate_purple_point()
        state_space.append([purple.x, purple.y])
        color1 = classify(purple.x, purple.y, 1)
        if check_color("P", color1):
            k1 += 1
        color3 = classify(purple.x, purple.y, 3)
        if check_color("P", color3):
            k3 += 1
        color7 = classify(purple.x, purple.y, 7)
        if check_color("P", color7):
            k7 += 1
        color15 = classify(purple.x, purple.y, 15)
        if check_color("P", color15):
            k15 += 1
        points.append(Point(purple.x, purple.y, "P", color1, color3, color7, color15))

        generated_points += 4
        # print(generated_points)

    statistics(generated_points, k1, k3, k7, k15)                      # vypise statistiku uspesnosti klasifikatora
    visualize(1)                                                       # vizualizacia 1-n-n
    visualize(3)                                                       # vizualizacia 3-n-n
    visualize(7)                                                       # vizualizacia 7-n-n
    visualize(15)                                                      # vizualizacia 15-n-n


main()
