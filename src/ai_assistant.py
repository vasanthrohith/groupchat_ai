from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate


load_dotenv(override=True)
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

# # Initialize Groq LLM
# llm = ChatGroq(
#     model_name="llama3-70b-8192",
#     temperature=0.7
# )



class AI_Assistant:
    def __init__(self,):
        # Initialize Groq LLM
        self.llm = ChatGroq(
            model_name="llama3-70b-8192",
            temperature=0.7
        )

   
    def monitor_user_discussion(self,message_history: list, user_recent_message: str)-> str:
        try:
            if "heyai" in user_recent_message.replace(" ","").lower():
                response = self.call_assistant(message_history, user_recent_message)
                return response
            
            return "skip"
        except Exception as error:
            print("Error : ",error)
            return "skip"


    def call_assistant(self, message_history, user_recent_message):
        system_prompt = f"""You are an helpful assistant bot helping in group discussion. 
                        with the below chat message try to assist user's question.
                        \n\n discussion hustory:\n\n {message_history}
                        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}")
        ])

        # Create the chain that guarantees JSON output
        assistant_chain = prompt | self.llm 
        response  = assistant_chain.invoke({"input": user_recent_message})

        return response.content