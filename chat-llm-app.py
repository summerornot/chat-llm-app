import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load the OpenAI API key from the .env file
load_dotenv('.env', override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

# Ensure the API key is set
if not openai_api_key:
    raise ValueError("OpenAI API key is missing. Please set it in the .env file.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

# Load the document into memory
document_path = "your_document.txt"
if not os.path.exists(document_path):
    raise FileNotFoundError(f"Document file '{document_path}' not found!")

with open(document_path, "r") as file:
    document_content = file.read()

# Streamlit app
st.title("Ask me anything")
st.write("I'll help you think from a different perspective.")

# Horizontal Divider
st.markdown("---")

# Instructions Section
st.markdown("""
### How to Use the App
1. Type your question in the input box.
2. Click **Help me think about this** to receive meaningful insights.
3. Reflect on the response and explore your thoughts!
""")

# Input for user question
user_question = st.text_input("Ask a question:")

if st.button("Help me think about this"):
    if user_question.strip():
        try:
            # Send the question and document to the LLM
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers the user based on the given document. Do not mention the document in your response. Your response should be a full answer, not a conversation. Remember to end the response wiht a helpful short activity that user can try. You can also add a quote from the internet if its fits the user's query. Your tone is like a friendly therapist. anThe user is not looking for answers or advice. Your job is to help the user think about their problems in a different way, like a psychologist or life coach."},
                    {"role": "system", "content": f"Document content: {document_content}"},
                    {"role": "user", "content": user_question},
                ]
            )
            # Extract the AI's response
            answer = response.choices[0].message.content

            # Display the response
            st.success("Answer:")
            st.write(answer)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a question.")
