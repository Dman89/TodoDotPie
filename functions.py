import os
from sys import platform

def clear():
    if "win" in platform.lower():
        os.system("cls")
    else:
        os.system("clear")

def p(msg):
    print(msg)
