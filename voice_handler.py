import openai
import json
import tempfile
import pyaudio
import wave


class VoiceHandler:
    def __init__(self, config_file="secrets.json"):
        # Load API key from JSON configuration file
        with open(config_file, 'r') as file:
            secrets = json.load(file)
            self.api_key = secrets.get("openai_api_key")

        # Set the API key for OpenAI
        openai.api_key = self.api_key

        # Audio recording parameters
        self.chunk = 1024  # Buffer size
        self.format = pyaudio.paInt16  # Audio format
        self.channels = 1  # Mono
        self.rate = 44100  # Sample rate

    def record_audio(self, duration=5):
        """
        Records audio from the microphone and returns the filename of the saved audio file.

        Parameters:
        - duration: Duration of the recording in seconds.

        Returns:
        - filename: The file path of the recorded audio.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=self.channels,
                        rate=self.rate, input=True,
                        frames_per_buffer=self.chunk)

        print("Recording...")
        frames = []

        for _ in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("Recording finished.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save audio to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(temp_file.name, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))

        return temp_file.name

    def transcribe_audio(self, audio_file):
        """
        Sends the recorded audio file to OpenAI Whisper API for transcription.

        Parameters:
        - audio_file: The file path of the recorded audio.

        Returns:
        - transcribed_text: The transcribed text from the audio input.
        """
        try:
            with open(audio_file, "rb") as file:
                response = openai.Audio.transcribe("whisper-1", file)
                transcribed_text = response['text']
                print(f"Transcribed text: {transcribed_text}")
                return transcribed_text
        except Exception as e:
            print(f"Error in VoiceHandler.transcribe_audio: {e}")
            return None

    def playback_response(self, text):
        """
        Placeholder for text-to-speech playback of the assistant's response.

        Parameters:
        - text: The response text to convert to speech.
        """
        print(f"Playing back: {text}")
        # Placeholder for future TTS integration


# Example usage
if __name__ == "__main__":
    voice_handler = VoiceHandler()
    audio_file = voice_handler.record_audio()
    transcribed_text = voice_handler.transcribe_audio(audio_file)
    if transcribed_text:
        voice_handler.playback_response("This is a response placeholder.")
