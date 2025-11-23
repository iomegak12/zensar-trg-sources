import os
import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

def main():
    try:
        load_dotenv(override=True)
        
        st.set_page_config(
            page_icon=":sparkles:",
            page_title="Interact with CSV Data"
        )

        st.title("HR - Attrition Analysis")
        st.subheader(
            "This is a simple AI assistant to help you to find HR Attrition Insights")

        st.markdown("""
                    This is a simple chatbot which helps to analyze HR Attrition related information and unleash the insights.
                    """)

        user_question = st.text_input(
            "Ask your questions about HR Employees Attritioning ...")

        csv_path = "../lc-training-data/hr-employees-attritions-internet.csv"
        df = pd.read_csv(csv_path)

        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
        azure_api_version = os.getenv("AZURE_API_VERSION")
        temperature = 0.8
        max_tokens = 1000

        llm = AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=azure_api_key,
            azure_deployment=azure_deployment,
            api_version=azure_api_version,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        agent = create_pandas_dataframe_agent(
            llm,
            [df],
            verbose=True,
            allow_dangerous_code=True,
        )

        agent.handle_parsing_errors = True
        answer = agent.invoke(user_question)
        
        st.write(answer["output"])
    except Exception as e:
        st.error(f"Error loading environment variables: {e}")
        
        return
    
if __name__ == "__main__":
    main()