import cmath
import speech_recognition as sr  # Make sure this line is present
import pyttsx3
import sounddevice as sd
import numpy as np
import wavio  # For saving the audio as a WAV file
import nltk
import sys
from nltk.tokenize import word_tokenize
from word2number import w2n
import matplotlib.pyplot as plt

from calculator import *  # Import AI calculator function
from polynomial import *  # Import polynomial solver function
nltk.download('punkt')


def main_menu():
    print("===================================")
    print("        Welcome to the Main Menu")
    print("===================================")
    print("1: AI Calculator")
    print("2: Polynomial Solver")
    print("0: Exit")
    print("===================================")

    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            ai_calculator()  # Call the AI calculator function
        elif choice == 2:
            polynomial_solver()  # Call the polynomial solver function
        elif choice == 0:
            confirm = input("Are you sure you want to exit? (y/n): ").lower()
            if confirm == 'y':
                print("Exiting. Goodbye!")
                sys.exit()
            else:
                main_menu()
        else:
            print("Invalid choice. Please try again.")
            main_menu()
    except ValueError:
        print("Invalid input. Please enter a number.")
        main_menu()



if __name__ == "__main__":
    main_menu()  # Start the menu
