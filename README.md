# Maths_AI_Python
An AI which calucluate basic maths question by taking input as a voice and TYPE both.

main.py
This script serves as the entry point for the application, providing a main menu for users to choose between different functionalities:

AI Calculator: Utilizes an AI-powered calculator to perform various mathematical operations.
Polynomial Solver: Solves quadratic polynomial equations based on user-provided coefficients.
The main menu interacts with other modules to handle specific tasks and includes:

Menu Navigation: Guides users through options.
Function Calls: Executes the AI calculator or polynomial solver based on user input.
Error Handling: Prompts the user for correct input if an invalid choice is made.
This file should be run to initiate the program and access the menu options.

polynomial.py
This module focuses on solving quadratic polynomial equations and includes several auxiliary functions for user interaction and result visualization:

Speech-to-Text Input: Uses voice recognition to gather coefficients (a, b, and c) for the quadratic equation.
Equation Solution: Calculates roots of the quadratic equation and determines the nature of the solutions (real or complex).
Graph Plotting: Visualizes the quadratic function based on the provided coefficients.
Key functions:

speak(): Provides text-to-speech functionality to improve user experience.
record_audio(): Records audio input from the user.
listen_for_input(): Transforms speech into numeric input for coefficients.
plot_quadratic(): Plots the quadratic function for a visual representation of the equation.

calculator.py
This module provides basic arithmetic operations, allowing for addition, subtraction, multiplication, and division. Designed for use within the main program, it enables simple, straightforward calculations.

Key functions:

Addition: Adds two or more numbers.
Subtraction: Subtracts one number from another.
Multiplication: Multiplies two or more numbers.
Division: Divides one number by another, with error handling for division by zero.
This module is used by main.py as part of the AI Calculator functionality, enabling fundamental operations to be performed through a text or voice-driven interface.
