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

    while True: 

        bomb_pct = input(
            "Enter the percentage of the board that will be bombs [Typical value is 0.15] :"
            )
        try:
            bomb_pct = float(bomb_pct)
            if 0 < bomb_pct < 1:
                break
            else:
                print("Please enter a value between 0 and 1")

        except ValueError:
            print("Please enter a valid value between 0 - 1")

    root = tk.Tk()
    app = GUI.MinesweeperGUI(root, user_width, user_height, bomb_pct, cell_size=40)
    root.mainloop()
main()