import openai
from dotenv import find_dotenv, load_dotenv
import os
import requests
import json
import time
import streamlit as st
from hospitals.models import UserReview, Institution

load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"
'''
#This is the getnews example from the api 
s_api_key = os.environ.get("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=5"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            news_json = response.json()
            data = news_json

            # Looping through the json and accessing all the fields
            status = data["status"]
            total_results = data["totalResults"]
            articles = data["articles"]
            final_news = []

            # Loop through the articles
            for article in articles:
                source_name = article["source"]["name"]
                author = article["author"]
                title = article["title"]
                description = article["description"]
                url = article["url"]
                content = article["content"]

                title_description = f"""
                    Title : {title}
                    Author : {author}
                    Description : {description}  
                    Source : {source_name}   
                    Url: {url}
                """
                final_news.append(title_description)

            return final_news

        else:
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API REQUEST: {e}")
        return []
'''
def get_reviews(institution_name):
    institution = Institution.objects.filter(institution_name__icontains=institution_name).first()
    if institution:
        reviews = UserReview.objects.filter(institution=institution)
        return [review.review for review in reviews]
    else:
        return []

# Main class definition
class AssistantManager:
    assistant_id= None
    thread_id=None 
    def __init__(self, model=model):
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None

        # Retrieve existing assistants if IDs are already present and avoid duplication
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=AssistantManager.thread_id
            )
    def create_assistant(self, name, instructions, tools):
     if not self.assistant:
        try:
            assistant_obj = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=self.model
            )
            AssistantManager.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            print(f"Assistant ID: {self.assistant_id}")
        except Exception as e:
            print(f"Error creating assistant: {e}")
        else:
          print(f"Assistant already created. Assistant ID: {self.assistant_id}")

    def create_thread (self):
        if not self.thread:
            thread_obj= self.client.beta.threads.create()
            AssistantManager.thread_id=thread_obj.id
            self.thread=thread_obj
            print(f"thread:::{self.thread.id}")
    def add_message_to_thread(self,role,content):
        if self.thread:
            self.client.beta.threads.messages.create (
                thread_id=self.thread.id,
                role=role,
                content=content
            )
    def run_assistant(self, instructions):
          if self.thread and self.assistant:
              try:
                self.run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
                instructions=instructions
            )
                print(f"Run ID: {self.run.id}")
              except Exception as e:
                print(f"Error running assistant: {e}")

    # Inside the AssistantManager class

    def run_steps(self):
      if self.thread and self.run:
        if self.run.id:
            run_steps = self.client.beta.threads.runs.steps.list(
                thread_id=self.thread.id,
                run_id=self.run.id
            )
            print(f"RUN-STEPS :::{run_steps}")
        else:
            print("The 'run' object does not have an 'id' attribute.")
      else:
        print("Assistant or run not initialized. Unable to fetch run steps.")
    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread),
            summary =[]

            last_message= messages.data[0]
            role= last_message.role
            response= last_message.content[0].text.value
            summary.append(response)
            self.summary= "\n".join(summary)
            print(f"SUMMARY--->{role.capitalize()}:.....response: {response}")

            #for msg in messages:
            #    role=msg.role
            #    content=msg.content[0].text.value
             #   print(f"SUMMARY--->{role.capitalize()}:.....response: {response}")
    def call_required_functions(self,required_actions):
        if not self.run:
            return
        tool_outputs= []
        for action in required_actions["tool_calls"]:
            func_name = action["function"] ["name"] 
            arguments = json.loads(action["function"]["arguments"])
            '''
              if func_name== "get_news":
                output= get_news(topic=arguments["topic"])
                print(f"STUFFF.....{output}")
                final_str = ""
                for item in output:
                  final_str +="".join(item)
                  tool_outputs.append({"tool_call_id": action["id"],
                                      "output": final_str })
             '''
            if func_name == "get_reviews":
              output= get_reviews(institution_name=arguments["institution_name"])
        print(f"STUFFF.....{output}")
        final_str = ""
        for item in output:
                  final_str +="".join(item)
                  tool_outputs.append({"tool_call_id": action["id"],
                                      "output": final_str })

                  print("SUBMITTING OUTPUT TO THE ASSISTANT")
        else:
                raise ValueError (f"Unkown function: {func_name}")
            

                
                print("Submitting outputs back yo the assistant....")
                self.client.beta.threads.runs.submit_outputs(
                    thread_id=self.thread.id,
                    run_id=self.run.id,
                    tool_outputs=tool_outputs
                )
    def get_summary(self):
                return self.summary            
    def wait_for_completion(self):
        if self.thread and self.run:
            while True:
                time.sleep(5)
                run_status=self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id, run_id=self.run.id
                )
                print(f"RUN STATUS:::{run_status.model_dump_json(indent=4)}")

                if run_status.status== "completed":
                  self.process_message()
                  break
                elif run_status.status=="requires_action":
                    print("function calling now")
                    self.call_required_functions(
                        required_actions=run_status.required_action.submit_tool_outputs.model_dump()
                    )


  #run steps
    def run_steps(self):
      if self.thread and self.run and self.run.id:  # Check if self.run is not None
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=self.thread.id,
            run_id=self.run.id
        )
        print(f"RUN-STEPS :::{run_steps}")
      else:
        print("Assistant, run, or run ID not initialized. Unable to fetch run steps.")

def main():
   # news = get_news("Bitcoin")
    #print(news[0])


    # Create an instance of the AssistantManager class
    assistant_manager = AssistantManager()

    #Streamlit interface
    st.title("Reviews baboy")

    with st.form (key= "user_input_form"):
        institution_name = st.text_input("Enter institution name")
        submit_button = st.form_submit_button(label="Run Assistant")

        if submit_button:
          assistant_manager.create_assistant(
            name="Ixnay",
            instructions="You are a personal review summarizer assistant who knows how to summarize reviews for institutions",
            tools=[
                {
                "type": "function",
                "function": {
                    "name": "get_reviews",
                    "description":"Get the list of reviews from the function",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string"},
                            "description": {"type": "string"}
                        }
                        },
                        "required" : ["institution_name"],
                },
                    },
                

            ]
        )
       
        assistant_manager.create_thread()
         #add the message and run assistant
        assistant_manager.add_message_to_thread(
            role="user",
             content=f"Summarize reviews for {institution_name}"
        )
        assistant_manager.run_assistant("summarize the news")
#wait for completion and process the messages
        assistant_manager.wait_for_completion()

        summary= assistant_manager.get_summary()

        st.write(summary)
        st.text("run steps: ")
        assistant_manager.run_steps()






if __name__ == "__main__":
    main()

