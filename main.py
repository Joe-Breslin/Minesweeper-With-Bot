# main.py

import GUI
import tkinter as tk

def main():
    while True:

        user_width = input("Enter the width of the board: ")

        try:
            user_width = int(user_width)
            break
        except ValueError:
            print("Please entera valid whole number")
        
    while True:

        user_height = input("Enter the height of the board: ")

        try:    
            user_height = int(user_height)
            break
        except ValueError:
            print("Please enter a valid whole number")

    root = tk.Tk()
    app = GUI.MinesweeperGUI(root, user_width, user_height, cell_size=40)
    root.mainloop()
main()