import pyttsx4


class TextToSpeech:
    def __init__(self, rate=200, volume=1.0):
        # Initialize the TTS engine
        self.engine = pyttsx4.init()
        # Set initial properties
        self.set_rate(rate)
        self.set_volume(volume)

    def speak(self, text):
        """
        Convert text to speech and play it.

        Parameters:
        text (str): The text to be spoken.
        """
        # Queue the text for speech
        self.engine.say(text)
        # Process the queued speech (blocking)
        self.engine.runAndWait()

    def set_rate(self, rate):
        """
        Set the rate (speed) of speech.

        Parameters:
        rate (int): Words per minute.
        """
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """
        Set the volume level.

        Parameters:
        volume (float): Volume level (0.0 to 1.0).
        """
        self.engine.setProperty('volume', volume)

    def change_voice(self, voice_id):
        """
        Set a specific voice by ID.

        Parameters:
        voice_id (str): The ID of the voice to use.
        """
        self.engine.setProperty('voice', voice_id)

    def list_voices(self):
        """
        List available voices.

        Returns:
        list: Available voices with ID and name.
        """
        voices = self.engine.getProperty('voices')
        return [(voice.id, voice.name) for voice in voices]


# Example usage:
if __name__ == "__main__":
    tts = TextToSpeech(rate=150, volume=0.9)

    # List available voices and set one
    for voice_id, voice_name in tts.list_voices():
        print(f"Voice ID: {voice_id}, Name: {voice_name}")

    # Use a specific voice if available (replace with desired voice ID)
    # tts.change_voice(voice_id="com.apple.speech.synthesis.voice.Alex")  # Example for MacOS

    # Test speaking
    tts.speak("Hello, welcome to the text-to-speech system.")
