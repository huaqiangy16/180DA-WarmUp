#Work Cited: RealPython: The Ultimate Guide To Speech Recognition With Python, https://realpython.com/python-speech-recognition/#putting-it-all-together-a-guess-the-word-game
import random
import time

import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.energy_threshold = 3000
        #recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["Hello", "Guess", "fireball", "ice", "Water"]
    input = " "
    reuslt = ""
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    Words_To_Speak = [] #empty list for words to speak

    while(True):
        target = " "
        for i in range(2): #randomly choose two words from the word list
            Words_To_Speak.append(random.choice(WORDS))

        print("please speak out the following words in order: ", end="")
        print(Words_To_Speak)

        while(True):
            input = recognize_speech_from_mic(recognizer, microphone)
            if input["transcription"]:
                break
            if not input["success"]:
                continue
            print("I didn't catch that. Please try again.\n")  
            pass

        for j in Words_To_Speak:
            target = target + " " + j

        result = " " + input["transcription"]
        print(result.lower())
        print(target.lower())
        if(result.lower() == target.lower()):
            print("Great Job!")
        else:
            print("Please try again")

        Words_To_Speak.clear()
        if(result.lower() == " stop"):
            break

