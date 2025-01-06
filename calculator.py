import numpy as np
import sounddevice as sd
import wavio  # For saving the audio as a WAV file
import speech_recognition as sr
import pyttsx3  # For text-to-speech
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')

engine = pyttsx3.init()
r = sr.Recognizer()


def record_audio(duration=5, fs=44100, filename="output.wav"):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()
    print("Finished recording")
    wavio.write(filename, recording, fs, sampwidth=2)
    return filename


def extract_numbers_and_operation(text):
    tokens = word_tokenize(text.lower())
    print(f"Tokens: {tokens}")
    numbers = []
    operation = None
    temp_number = ""
    
    for token in tokens:
        if token in ['negative', '-'] and not temp_number:
            temp_number += '-'
        elif token.replace('.', '', 1).isdigit():
            temp_number += token
        elif temp_number:
            numbers.append(float(temp_number))
            temp_number = ""
            if token in ['+', '-', '*', '/']:
                operation = token
            elif token in ['multiply', 'times', 'x']:
                operation = '*'
            elif token in ['add']:
                operation = '+'
            elif token in ['subtract']:
                operation = '-'
            elif token in ['divide']:
                operation = '/'

    # Append last number if any
    if temp_number:
        numbers.append(float(temp_number))

    print(f"Extracted numbers: {numbers}, operation: {operation}")
    return numbers, operation



def calculate_result(numbers, operation):
    if not operation or len(numbers) < 2:
        return "Invalid input"
    if operation == '+':
        return sum(numbers)
    elif operation == '-':
        return numbers[0] - sum(numbers[1:])
    elif operation == '*':
        result = 1
        for number in numbers:
            result *= number
        return result
    elif operation == '/':
        try:
            result = numbers[0]
            for number in numbers[1:]:
                result /= number
            return result
        except ZeroDivisionError:
            return "Error: Division by zero"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def ai_calculator():
    audio_filename = record_audio()
    with sr.AudioFile(audio_filename) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            numbers, operation = extract_numbers_and_operation(text)
            result = calculate_result(numbers, operation)
            print("Result:", result)
            speak(f"The result is {result}")
        except sr.UnknownValueError:
            print("Sorry, I didn't understand what you said")
            speak("Sorry, I didn't understand what you said.")
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("An error occurred.")
