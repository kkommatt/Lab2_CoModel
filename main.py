import numpy as np
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

transmitters = np.array([[5, 7], [-2, 5], [-1, -9], [5, -4], [8, -1]])
angles = np.array([41, 163, 48, 148, 110])

angles = np.radians(angles)
ship_position = np.array([0, 0])


def find_location(transmitters=transmitters, bearings=angles):
    x = 0
    y = 0

    for i in range(len(transmitters)):
        x += transmitters[i][0] * math.cos(bearings[i])
        y += transmitters[i][1] * math.sin(bearings[i])

    return (x / len(transmitters), y / len(transmitters))


def dev(transmitters, ship_position):
    sum = 0
    for i in range(len(transmitters)):
        sum = sum + np.square(transmitters[i][0] / len(transmitters) - ship_position[0])
    return np.sqrt(sum)


def calculate_ship_coordinates():
    global transmitters, angles, ship_position
    x_values = x_values_entry.get().split()
    y_values = y_values_entry.get().split()
    angle_values = angle_values_entry.get().split()

    transmitters = np.array([[float(x), float(y)] for x, y in zip(x_values, y_values)])
    angles = np.array([np.radians(float(angle)) for angle in angle_values])

    ship_position = find_location(transmitters, angles)
    deviation = dev(transmitters, ship_position)

    result_label.config(
        text=f"Ship Coordinates: X={ship_position[0]:.3f}, Y={ship_position[1]:.3f}, Deviation: {deviation:.3f}")

    ax.cla()
    ax.scatter(ship_position[0], ship_position[1], color="red", label="Ship")
    ax.scatter(transmitters[:, 0], transmitters[:, 1], color='blue', label='Transmitters')
    length = 100
    for (x, y), angle in zip(transmitters, angles):
        x_line = [x - length * np.cos(angle), x + length * np.cos(angle)]
        y_line = [y - length * np.sin(angle), y + length * np.sin(angle)]
        ax.plot(x_line, y_line, color='green')
    ax.axis([-20, 20, -20, 20])
    ax.grid(True)
    ax.legend()
    canvas.draw()


def calculate_distance():
    x_exact_value = float(x_exact.get())
    y_exact_value = float(y_exact.get())

    distance = np.sqrt(np.square(x_exact_value - ship_position[0]) + np.square(y_exact_value - ship_position[1]))

    result_distance_label.config(
        text=f"Distance between exact and approximate coordinates: {distance:.3f}")
    ax.cla()
    ax.scatter(x_exact_value, y_exact_value, color="black", label="Ship exact")
    ax.scatter(ship_position[0], ship_position[1], color="red", label="Ship")
    ax.scatter(transmitters[:, 0], transmitters[:, 1], color='blue', label='Transmitters')
    length = 100
    for (x, y), angle in zip(transmitters, angles):
        x_line = [x - length * np.cos(angle), x + length * np.cos(angle)]
        y_line = [y - length * np.sin(angle), y + length * np.sin(angle)]
        ax.plot(x_line, y_line, color='green')
    ax.plot([x_exact_value, ship_position[0]], [y_exact_value, ship_position[1]], color='yellow')
    ax.axis([-20, 20, -20, 20])
    ax.grid(True)
    ax.legend()
    canvas.draw()
    canvas.draw()


def calculate_angles():
    global transmitters, angles, ship_position
    x_values = x_entry.get().split()
    y_values = y_entry.get().split()
    x_ship_exact = float(x_super_exact.get())
    y_ship_exact = float(y_super_exact.get())
    ship_position = x_ship_exact, y_ship_exact
    # Convert input values to numpy arrays
    transmitters = np.array([[float(x), float(y)] for x, y in zip(x_values, y_values)])
    angles = []
    for transmitter in transmitters:
        diff = transmitter - ship_position
        angle = math.atan(diff[1] / diff[0])
        angles.append(angle)
    text = "Criterion: np.sqrt(np.sum((transmitters[:, 0]*np.cos(angles) - ship_position[0]) ** 2\n + (transmitters[:, 1]*np.sin(angles) - ship_position[1]) ** 2)/len(angles))\n Angles in degrees:\n"
    angles = np.degrees(angles)
    text = text + str(np.round(angles, 3))
    criterion = np.sqrt(np.sum((transmitters[:, 0] * np.cos(angles) - ship_position[0]) ** 2 + (
                transmitters[:, 1] * np.sin(angles) - ship_position[1]) ** 2) / len(angles))
    text = text + f"\nCriterion value: {criterion:.3f}"
    criterion1 = np.sqrt(((transmitters[:, 0] * np.cos(angles) - ship_position[0]) ** 2 + (
            transmitters[:, 1] * np.sin(angles) - ship_position[1]) ** 2) / len(angles))
    text = text + "\n" + str(criterion1)
    angles_label.config(text=text)
    ax.cla()
    ax.scatter(ship_position[0], ship_position[1], color="red", label="Ship")
    ax.scatter(transmitters[:, 0], transmitters[:, 1], color='blue', label='Transmitters')
    length = 100
    angles = np.radians(angles)
    for (x, y), angle in zip(transmitters, angles):
        x_line = [x - length * np.cos(angle), x + length * np.cos(angle)]
        y_line = [y - length * np.sin(angle), y + length * np.sin(angle)]
        ax.plot(x_line, y_line, color='green')
    ax.axis([-20, 20, -20, 20])
    ax.grid(True)
    ax.legend()
    canvas.draw()


# Create a Tkinter window
root = tk.Tk()
root.title("Ship Coordinates Calculator")

# Create a frame for the input and result
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

# Create labels and entry fields
ttk.Label(frame, text="ОЧІКУЄТЬСЯ КОРЕКТНИЙ ВВІД!\n\n Task1").grid(row=0, column=0, columnspan=2)

ttk.Label(frame, text="X Values").grid(row=1, column=0)
x_values_entry = ttk.Entry(frame)
x_values_entry.grid(row=1, column=1)
x_values_entry.insert(0, "5 -2 -1 5 8")

ttk.Label(frame, text="Y Values").grid(row=2, column=0)
y_values_entry = ttk.Entry(frame)
y_values_entry.grid(row=2, column=1)
y_values_entry.insert(0, "7 5 -9 -4 -1")

ttk.Label(frame, text="Angle Values (in degrees)").grid(row=3, column=0)
angle_values_entry = ttk.Entry(frame)
angle_values_entry.grid(row=3, column=1)
angle_values_entry.insert(0, "41 163 48 148 110")

result_label = ttk.Label(frame, text="")
result_label.grid(row=4, column=0, columnspan=2)

# Create a button to calculate ship coordinates
calculate_button = ttk.Button(frame, text="Calculate Ship Coordinates", command=calculate_ship_coordinates)
calculate_button.grid(row=5, column=0, columnspan=2)

ttk.Label(frame, text="\nTask2\n").grid(row=6, column=0)

ttk.Label(frame, text="Exact X of ship").grid(row=7, column=0)
x_exact = ttk.Entry(frame)
x_exact.grid(row=7, column=1)

ttk.Label(frame, text="Exact Y of ship").grid(row=8, column=0)
y_exact = ttk.Entry(frame)
y_exact.grid(row=8, column=1)

result_distance_label = ttk.Label(frame, text="")
result_distance_label.grid(row=9, column=0, columnspan=2)

distance_button = ttk.Button(frame, text="Calculate distance between exact and approximate coordinates",
                             command=calculate_distance)
distance_button.grid(row=10, column=0, columnspan=2)

ttk.Label(frame, text="\nTask3\n").grid(row=11, column=0)

ttk.Label(frame, text="X Values").grid(row=12, column=0)
x_entry = ttk.Entry(frame)
x_entry.grid(row=12, column=1)

ttk.Label(frame, text="Y Values").grid(row=13, column=0)
y_entry = ttk.Entry(frame)
y_entry.grid(row=13, column=1)

ttk.Label(frame, text="Exact X of ship").grid(row=14, column=0)
x_super_exact = ttk.Entry(frame)
x_super_exact.grid(row=14, column=1)

ttk.Label(frame, text="Exact Y of ship").grid(row=15, column=0)
y_super_exact = ttk.Entry(frame)
y_super_exact.grid(row=15, column=1)

angles_button = ttk.Button(frame, text="Calculate angles", command=calculate_angles)
angles_button.grid(row=17, column=0, columnspan=2)

angles_label = ttk.Label(frame, text="")
angles_label.grid(row=16, column=0, columnspan=2)

# Create a frame for the plot
plot_frame = ttk.Frame(root)
plot_frame.grid(row=0, column=1, padx=10, pady=10)

# Create a matplotlib figure and a canvas to display the plot
fig = Figure(figsize=(6, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack()

# Initialize the plot
calculate_ship_coordinates()

root.mainloop()
