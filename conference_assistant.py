from voice_handler import VoiceHandler
from openai_handler import OpenAIHandler
from animation_controller import AnimationController


class ConferenceAssistant:
    def __init__(self):
        # Initialize the handlers
        self.voice_handler = VoiceHandler()
        self.openai_handler = OpenAIHandler()
        self.animation_controller = AnimationController()

    def interact(self):
        """
        Manages a full interaction sequence: records audio, sends it to OpenAI,
        triggers animations, and provides a spoken response.
        """
        # Trigger idle animation initially
        self.animation_controller.idle_animation()

        # Record user input
        print("Awaiting user input...")
        audio_file = self.voice_handler.record_audio()

        # Transcribe audio
        transcribed_text = self.voice_handler.transcribe_audio(audio_file)

        if transcribed_text:
            # Acknowledge the user's input
            self.animation_controller.acknowledge_animation()

            # Generate response from OpenAI
            self.animation_controller.start_speaking_animation()
            response_text = self.openai_handler.get_response(transcribed_text)
            self.animation_controller.stop_speaking_animation()

            # Playback response (currently just a placeholder)
            self.voice_handler.playback_response(response_text)

            # Back to idle animation after response
            self.animation_controller.idle_animation()
        else:
            print("No valid input received. Please try again.")


# Example usage
if __name__ == "__main__":
    assistant = ConferenceAssistant()
    assistant.interact()
