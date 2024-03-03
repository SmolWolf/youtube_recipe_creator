import openai
from youtube_text_converter import fetch_video_description_and_subtitles
from dotenv import load_dotenv
import time
import json
import streamlit as st 


load_dotenv()

client = openai.OpenAI()

model = "gpt-4-turbo-preview"
#id="https://www.youtube.com/watch?v=BuCoZdLptwA"


class AssistantManager:
    thread_id=None
    assistant_id=None
    
    def __init__(self, model: str = model):
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None

        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id = AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=AssistantManager.thread_id
            )
    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=self.model
            )
            AssistantManager.assistant_id=assistant_obj.id
            self.assistant = assistant_obj
            print(f'AssisID::::: {self.assistant.id}')
    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id 
            self.thread = thread_obj 
            print(f'ThreadID::::: {self.thread.id}')

    def add_message_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role=role,
                content=content
            )
    
    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id = self.thread.id,
                assistant_id = self.assistant.id,
                instructions=instructions
            )
    def process_message(self):
        #is there a working thread?
        if self.thread:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
            summary = []

            last_message = messages.data[0]
            role = last_message.role
            response = last_message.content[0].text.value
            summary.append(response)

            self.summary = "\n".join(summary)
            print(f"Recipe-----> {role.capitalize()}: ==> {response}")

    def call_required_functions(self, required_actions):
        if not self.run:
            return
        tool_outputs = []
        
        for action in required_actions['tool_calls']:
            func_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])
            if func_name == "fetch_video_description_and_subtitles":
                output = fetch_video_description_and_subtitles(id=arguments['id'])
                print(output)
                #print("hellohellohellohellohellohello")
                final_str =""
                for item in output:
                    final_str += "".join(item)
                
                tool_outputs.append({"tool_call_id": action['id'],
                                     "output": final_str})
            else:
                raise ValueError(f'Unknown function: {func_name}')
        
        print("Submitting outputs back to the Assistant.....")
        self.client.beta.threads.runs.submit_tool_outputs(
           thread_id = self.thread.id,
           run_id = self.run.id,
           tool_outputs = tool_outputs

        )

    #for streamlit
    def get_summary(self):
        return self.summary


    def wait_for_completed(self):
        if self.thread and self.run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id = self.thread.id,
                    run_id = self.run.id
                )
                print(f'Run Status: {run_status.model_dump_json(indent=4)}')
                if run_status.status =="completed":
                    self.process_message()
                    break
                elif run_status.status =="requires_action":
                    print('Function calling now....')
                    self.call_required_functions(
                        required_actions=run_status.required_action.submit_tool_outputs.model_dump()
                    )

    def run_steps(self):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=self.thread.id,
            run_id = self.run.id
        ) 
        print(f"Run-Steps: {run_steps}")  

def main():

    manager = AssistantManager()
    # Streamlit interface
    st.title("Youtube Recipe writer")

    with st.form(key="user_input_form"):
        instructions = st.text_area("Enter Youtube Url for recipe extraction:")
        submit_button = st.form_submit_button(label="Run Assistant") 
        if submit_button:
            manager.create_assistant(
                name="Recipe Creator",
                instructions='''You get a youtube transcript. Please write the recipe down like it would appear in a cookbook.
                It should include following sections:
                *** ingredients ***
                *** instructions ***
                *** tips and tricks ***

                ''',
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "fetch_video_description_and_subtitles",
                            "description": "get's subtitles of a youtube recipe video",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "type": "string",
                                        "description": "youtube recipe url",
                                    }
                                },
                                "required": ["id"],
                            },
                        },
                    }
                ],
            )
            manager.create_thread()

            # Add the message and run the assistant
            manager.add_message_to_thread(
                role="user", content=f"Write a recipe given this instructions: {instructions}?"
            )
            manager.run_assistant(instructions="Write an recipe")

            # Wait for completions and process messages
            manager.wait_for_completed()

            summary = manager.get_summary()

            st.write(summary)

            #st.text("Run Steps:")
            #st.code(manager.run_steps(), line_numbers=True)


if __name__ == "__main__":
    main()