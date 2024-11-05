import openai
import json


class OpenAIHandler:
    def __init__(self, config_file="secrets.json"):
        # Load API key from JSON configuration file
        with open(config_file, 'r') as file:
            secrets = json.load(file)
            self.api_key = secrets.get("openai_api_key")

        # Set the API key for OpenAI
        openai.api_key = self.api_key
        self.messages = []  # List to store message history

    def start_conversation(self, system_instruction):
        """
        Starts a new conversation by setting the initial system message.

        Parameters:
        - system_instruction: The role message to instruct the assistant's behavior.
        """
        self.messages = [{"role": "system", "content": system_instruction}]

    def get_response(self, prompt, model="asst_ge1GpJP6nP0xqASiqvsaK6tX"):  # Replace with your Assistant model ID
        """
        Sends a prompt to the OpenAI API with conversation history and returns the response.

        Parameters:
        - prompt: The input text to send to OpenAI.
        - model: The model to use for generating responses.

        Returns:
        - response_text: The generated response from the Assistant.
        """
        try:
            # Add the user message to conversation history
            self.messages.append({"role": "user", "content": prompt})

            # Make a request to the OpenAI API with the conversation history
            response = openai.ChatCompletion.create(
                model=model,
                messages=self.messages
            )

            # Extract the assistant's response
            response_text = response['choices'][0]['message']['content']

            # Add the assistant response to the message history
            self.messages.append({"role": "assistant", "content": response_text})

            return response_text
        except Exception as e:
            print(f"Error in OpenAIHandler.get_response: {e}")
            return "I'm sorry, but I encountered an error."


# Example usage
if __name__ == "__main__":
    openai_handler = OpenAIHandler()
    openai_handler.start_conversation("You are a helpful conference assistant.")
    user_prompt = "What’s on the agenda for today?"
    response = openai_handler.get_response(user_prompt)
    print("Assistant:", response)
