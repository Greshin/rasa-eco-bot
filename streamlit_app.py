import streamlit as st
import requests
 
# Sidebar
st.sidebar.title("Navigation")
st.sidebar.markdown("Use this panel to configure the bot")
page = st.sidebar.selectbox("Go to", ["Home", "Chat", "About"])
 
# Main areac
st.title("Course Companion Bot")
st.divider()
 
if page == "Home":
    st.header("Welcome")
    st.write("Select a page from the sidebar to get started.")
 
elif page == "Chat":
    st.header("Chat")
 
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
 
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
 
    user_input = st.chat_input("Type your message here...")
 
    if user_input:
        # Store and display user message
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
 
        # Call Rasa REST API
        try:
            response = requests.post(
                "http://localhost:5005/webhooks/rest/webhook",
                json={"sender": "user1", "message": user_input}
            )
            rasa_replies = response.json()
            reply = rasa_replies[0]["text"] if rasa_replies else "I did not understand that."
        except:
            reply = "Could not reach the bot. Is Rasa running?"
 
        # Store and display bot reply
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
 
elif page == "About":
    st.header("About")
    st.write("Built with Rasa 3.6.21 and Streamlit.")
