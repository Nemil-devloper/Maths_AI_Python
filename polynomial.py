import cmath
import numpy as np
import speech_recognition as sr
import matplotlib.pyplot as plt
import pyttsx3  # For text-to-speech
import sounddevice as sd
import wavio
import nltk
from word2number import w2n
from nltk.tokenize import word_tokenize

nltk.download('punkt')
engine = pyttsx3.init()
recognizer = sr.Recognizer()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def record_audio(duration=5, fs=44100, filename="output.wav"):
    """Record audio and save it to a file."""
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()
    print("Finished recording")
    wavio.write(filename, recording, fs, sampwidth=2)
    return filename


from word2number import w2n

def listen_for_input(prompt):
    """Listen for user input and return the recognized number or prompt for keyboard input."""
    print(prompt)
    speak(prompt)

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        try:
            audio_filename = record_audio()
            with sr.AudioFile(audio_filename) as source:
                audio = recognizer.record(source)

                text = recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")  # Log the recognized text

                try:
                    # Attempt to convert spoken text (words or numbers) to a number
                    number = w2n.word_to_num(text)  # Convert word-form numbers
                    return number
                except ValueError:
                    if text.isdigit():  # Direct numeric input check
                        return int(text)
                    else:
                        print("Invalid input. Please try again.")
                        speak("That doesn't seem like a valid number. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I didn't understand the audio. Please try again.")
            speak("Sorry, I couldn't understand. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("There was an error with the speech recognition service. Please try again later.")
            return None

        attempts += 1

    # Fallback to keyboard input
    fallback = input("Please type the coefficient: ")
    try:
        return int(fallback)
    except ValueError:
        print("Invalid input. Defaulting to 0.")
        return 0  # Default to 0 if input is invalid
def plot_quadratic(a, b, c):
    """Plot the quadratic equation based on coefficients."""
    x = np.linspace(-100, 100, 400)
    y = a * x ** 2 + b * x + c
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=f'{a}x² + {b}x + {c}', color='b')
    plt.title('Quadratic Equation Graph')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.grid()
    plt.legend()
    plt.ylim(-100, 100)
    plt.xlim(-100, 100)
    plt.show()


def polynomial_solver():
    """Solve a quadratic equation based on user input."""
    a = listen_for_input("Please say the coefficient of X squared.")
    b = listen_for_input("Please say the coefficient of X.")
    c = listen_for_input("Please say the constant term.")

    if a is None or b is None or c is None:
        print("Invalid input detected. Exiting.")
        return

    D = b ** 2 - 4 * a * c
    sqrt_D = cmath.sqrt(D) if D < 0 else D ** 0.5
    sol1 = (-b + sqrt_D) / (2 * a)
    sol2 = (-b - sqrt_D) / (2 * a)

    result = f"The solutions are {sol1} and {sol2}"
    speak(result)
    print(result)

    nature = "complex" if D < 0 else "real" if D > 0 else "real and equal"
    speak(f"The equation has {nature} solutions.")

    plot_quadratic(a, b, c)
