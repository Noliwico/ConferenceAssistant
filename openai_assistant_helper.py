import json
import openai
from threading import Thread

class OpenAIAssistantHelper:
    def __init__(self):
        # Load API key and assistant ID from secrets.json
        with open('secrets.json', 'r') as file:
            secrets = json.load(file)
        self.api_key = secrets["openai_api_key"]
        self.assistant_id = secrets["openai_assistant_id"]
        # Set up OpenAI API key
        openai.api_key = self.api_key

    def send_message(self, message):
        # This method runs in a new thread to send a message to the assistant
        thread = Thread(target=self._create_and_send_message, args=(message,))
        thread.start()
        return thread

    def _create_and_send_message(self, message):
        # This method interacts with OpenAI to send a message and receive the response
        try:
            response = openai.ChatCompletion.create(
                model=self.assistant_id,  # Assume this to be the correct model ID
                messages=[{"role": "user", "content": message}]
            )
            print("Assistant's response:", response['choices'][0]['message']['content'])
        except Exception as e:
            print("An error occurred:", e)

# Example usage:
if __name__ == '__main__':
    assistant_helper = OpenAIAssistantHelper()
    thread = assistant_helper.send_message("Hello, assistant!")
    thread.join()  # Wait for the thread to complete
