from datetime import datetime
import json
import time

from openai import OpenAI


class OpenAIAssistantHelper:

    def __init__(self):

        # Load API key and assistant ID from secrets.json
        with open('secrets.json', 'r') as file:
            secrets = json.load(file)
        self.api_key = secrets["openai_api_key"]
        self.assistant_id = secrets["openai_assistant_id"]
        # Set up OpenAI API key
        self.client = OpenAI(api_key=self.api_key)
        self.thread = self.client.beta.threads.create()
        self.client.api_key = self.api_key

    def create_message(self, message):
        client_message = self.client.beta.threads.messages.create(thread_id=self.thread.id,
                                                                  role="user",
                                                                  content=message
                                                                  )
        print("Client message: ", client_message)
        return client_message

    def run_message(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        print("Current Time =", current_time)
        try:
            actual_run = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread.id,
                assistant_id=self.assistant_id,
                instructions="The current time is " + current_time
            )
            return actual_run
        except Exception as e:
            print("An error occurred while running the message:", e)

    def run_stream_message(self):
        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant_id  # ,
                # instructions="Please address the user as Jane Doe. The user has a premium account.",
        ) as stream:
            for event in stream:
                # Print the text from text delta events
                if event.event == "thread.message.delta" and event.data.delta.content:
                    print(event.data.delta.content[0].text)

    def get_latest_answer_text(self):
        message_list = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        return message_list.data[0].content[0].text.value

    def send_and_get_message(self, message_to_send):
        self.create_message(message_to_send)
        self.run_message()
        answer_text = self.get_latest_answer_text()
        return answer_text


# Example usage:
if __name__ == '__main__':
    assistant_helper = OpenAIAssistantHelper()
    answer = assistant_helper.send_and_get_message("What time is it?")
    print(answer)
    answer = assistant_helper.send_and_get_message("What is the first session on the day 1?")
    print(answer)

    # assistant_helper.run_message()
    # messages = assistant_helper.client.beta.threads.messages.list(thread_id=assistant_helper.thread.id)
    # print(messages.data[0].content[0].text.value)
    # assistant_helper.run_stream_message()
    # assistant_helper.create_message("Can you recommend a session for day 2?")
    # run = assistant_helper.run_message()
    # print(run)
    # assistant_helper.run_stream_message()

    # run = assistant_helper.run_message(message)

    # messages = assistant_helper.client.beta.threads.messages.list(thread_id=assistant_helper.thread.id)
    # print("********** RUN RESULT MESSAGE 1: ", messages)
    # message = assistant_helper.create_message("What is the first event on day 1?")
    # run = assistant_helper.run_message(message)
    # while run.status != "completed":
    #     print("********** RUN STATUS *********** ",run.status)
    #     time.sleep(1)
    # messages = assistant_helper.client.beta.threads.messages.list(thread_id=assistant_helper.thread.id)
    # print("********** RUN RESULT MESSAGE 2: ", messages)

