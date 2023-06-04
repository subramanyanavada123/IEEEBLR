import streamlit as st
import openai

def plan_event(user_input):
    chat_history = []
    while True:
        user_input = user_input.strip()
        if user_input.lower() == 'quit':
            return "Event planning canceled."

        chat_history.append(f"User: {user_input}")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chat_history,
            temperature=0.7,
            max_tokens=150,
            n=1,
            stop=None,
        )
        message = response.choices[0].text.strip().replace("Assistant:", "")
        chat_history.append(f"Assistant: {message}")
        if 'Event plan:' in message:
            return message
        user_input = st.text_input("User Input", value=message)

def main():
    st.title("Event Planner")

    user_input = st.text_input("User Input")
    if st.button("Submit"):
        event_plan = plan_event(user_input)
        st.write(event_plan)

if __name__ == "__main__":
    main()
