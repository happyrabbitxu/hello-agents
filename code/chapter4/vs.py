import tkinter as tk
import random

def judge(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "平局"
    elif (player_choice == "石头" and computer_choice == "剪刀") or \
         (player_choice == "剪刀" and computer_choice == "布") or \
         (player_choice == "布" and computer_choice == "石头"):
        return "你赢了！"
    else:
        return "你输了！"

root = tk.Tk()
root.title("人机对战石头剪刀布")
root.geometry("300x200")

def get_computer_choice():
    return random.choice(['石头', '剪刀', '布'])

def play(player_choice):
    computer_choice = get_computer_choice()
    result = judge(player_choice, computer_choice)
    result_label.config(text=f"你出了{player_choice}，电脑出了{computer_choice}。{result}")

btn_stone = tk.Button(root, text="石头", command=lambda: play("石头"))
btn_scissors = tk.Button(root, text="剪刀", command=lambda: play("剪刀"))
btn_paper = tk.Button(root, text="布", command=lambda: play("布"))

result_label = tk.Label(root, text="请选择", font=("Arial", 12))

result_label.pack(pady=10)
btn_stone.pack(side=tk.LEFT, padx=5)
btn_scissors.pack(side=tk.LEFT, padx=5)
btn_paper.pack(side=tk.LEFT, padx=5)

root.mainloop()