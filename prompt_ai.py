#from transformers import pipeline
import streamlit as st

st.title("Welcome to world of AI")
# # Load chatbot model
# chatbot = pipeline("text-generation", model="gpt2")
#
# while True:
#     #prompt = input("You: ")
#     prompt = st.text_input("Enter your message...")
#     if prompt.lower() == "exit":
#         break
#     if st.button("Enter") and prompt:
#         response = chatbot(prompt, max_length=100, do_sample=True)
#         print("AI:", response[0]['generated_text'])
#         st.write("AI:", response[0]['generated_text'])