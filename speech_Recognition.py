import speech_recognition as sr
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Please speak something...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    audio_data = recognizer.listen(source)
    print("Recognizing...")
    try:
        text = recognizer.recognize_google(audio_data)
        print("Speaked text file created whatsoevere You said")
        with open("recognized_text.txt", "a") as file:
            file.write(text + "\n")
        print("Text saved to recognized_text.txt")

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results; check your network connection.")
