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

# Download NLTK data (if not already downloaded)
nltk.download('punkt', quiet=True)

# Initialize text-to-speech engine and speech recognizer
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=3, fs=44100, filename="output.wav"):
    """Record audio and save it to a file."""
    try:
        print("Recording...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
        sd.wait()
        print("Finished recording")
        wavio.write(filename, recording, fs, sampwidth=2)
        return filename
    except Exception as e:
        print(f"Error recording audio: {e}")
        speak("There was an error recording the audio. Please try again.")
        return None

def listen_for_input(prompt):
    """Listen for user input and return the recognized number or prompt for keyboard input."""
    print(prompt)
    speak(prompt)

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        try:
            # Record audio and handle potential errors
            audio_filename = record_audio()
            if audio_filename is None:
                continue

            # Recognize speech from the recorded audio file
            with sr.AudioFile(audio_filename) as source:
                audio = recognizer.record(source)

                # Get the recognized text from speech
                text = recognizer.recognize_google(audio).lower()
                print(f"Recognized Text: {text}")  # Debugging log

                # Tokenize the recognized text to get individual words
                tokens = word_tokenize(text)
                print(f"Tokens: {tokens}")  # Debugging log

                # Iterate through the tokens and try converting them to numbers
                for token in tokens:
                    try:
                        # Check if the token is a valid number using word2num
                        number = w2n.word_to_num(token)
                        print(f"Converted '{token}' to number: {number}")  # Debugging log
                        return number
                    except ValueError:
                        if token.isdigit():  # Direct check for digit strings like '1', '2', etc.
                            print(f"Token '{token}' is a valid digit.")
                            return int(token)
                        elif token.startswith('-') and token[1:].isdigit():  # Handle negative numbers
                            print(f"Token '{token}' is a negative number.")
                            return int(token)

                # If no valid number is found, notify the user
                print("No valid number found in spoken input.")
                speak("That doesn't seem like a valid number. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I didn't understand the audio. Please try again.")
            speak("Sorry, I couldn't understand. Please try again.")
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            speak("There was an error with the speech recognition service. Please try again later.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("An unexpected error occurred. Please try again.")

        attempts += 1

    # Fallback to keyboard input if all attempts fail
    fallback = input("Could not understand. Please type the coefficient: ")
    try:
        return int(fallback)
    except ValueError:
        print("Invalid input. Defaulting to 0.")
        return 0




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

    if a == 0:
        print("This is not a quadratic equation. It's a linear equation.")
        speak("This is not a quadratic equation. Solving as a linear equation.")
        if b != 0:
            sol = -c / b
            print(f"The solution is: {sol}")
            speak(f"The solution is: {sol}")
        else:
            print("No valid equation to solve.")
            speak("No valid equation to solve.")
        return

    D = b ** 2 - 4 * a * c
    sqrt_D = cmath.sqrt(D) if D < 0 else D ** 0.5
    sol1 = (-b + sqrt_D) / (2 * a)
    sol2 = (-b - sqrt_D) / (2 * a)

    result = f"The solutions are {sol1} and {sol2}"
    speak(result)
    print(result)

    nature = "complex" if D < 0 else "real and distinct" if D > 0 else "real and equal"
    speak(f"The equation has {nature} solutions.")

    plot_quadratic(a, b, c)

# Main execution
if __name__ == "__main__":
    polynomial_solver()
