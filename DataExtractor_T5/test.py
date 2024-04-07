import urllib.parse
import os
import streamlit as st
from langchain.llms.openai import OpenAI
from langchain_openai import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import psycopg2


os.environ['OPENAI_API_KEY'] = "..........."
# Load environment variables
load_dotenv()


# Function to create SQL agent
def create_sql_agent_with_streamlit(db):
    # Initialize ChatOpenAI model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    # Create SQLDatabaseToolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Create SQL agent executor
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

    return agent_executor


def main():
    # Add an icon image
    icon = "C:/Users/smart/PycharmProjects/pythonProject/cognizant.png"
    #st.image(icon, width=50)
    st.image(icon, width=80, caption="Cognizant")
    #st.caption("Aetna")

    # UI
    #st.title("COGNIZANT")
    st.title("Data Extractor")



    # Database connection details
    #st.sidebar.header("Database Connection")
    #username = st.sidebar.text_input("Username", value="postgres")
    #password = st.sidebar.text_input("Password", type="password", value="Test1234")
    #hostname = st.sidebar.text_input("Hostname", value="localhost")
    #dbname = st.sidebar.text_input("Database Name", value="TestDB_Trail1")

    username = 'postgres'
    password = 'Test1234'
    hostname = 'localhost'
    dbname = 'TestDB_Trail1'
    # Connection URI
    encoded_password = urllib.parse.quote_plus(password)
    uri = f"postgresql://{username}:{encoded_password}@{hostname}:5432/{dbname}"
    db = SQLDatabase.from_uri(uri)

    # Create SQL agent
    agent_executor = create_sql_agent_with_streamlit(db)

    # User input
    user_input = st.text_input("Enter the description of data you are looking for: ")

    if st.button("Submit"):
        # Execute user query
        result = agent_executor.run(user_input)
        st.write("Relevant Data you have requested:", result)


if __name__ == "__main__":
    main()

