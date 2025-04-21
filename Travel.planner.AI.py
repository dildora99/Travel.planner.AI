
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# ========== Load API Key from .env ==========
load_dotenv()
api_key = os.getenv("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")
client = OpenAI(api_key=api_key)

# ========== Streamlit Page Settings ==========
st.set_page_config(page_title="Travel Planner AI", page_icon="🌍", layout="wide")
st.title("🌍 Travel Planner AI ✈️")
st.caption("Plan your dream trip with the help of AI – from itineraries to inspiration.")

# ========== Sidebar Navigation ==========
st.sidebar.header("🧭 Travel Assistant Menu")
mode = st.sidebar.radio("Choose what to do:", ("🗺️ Plan a Trip", "💬 Travel Chat", "📷 Generate Destination Image"))

# Option to reset trip memory
if st.sidebar.button("🧹 Reset Trip Planner"):
    st.session_state.trip_chat = []

# ========== Session Memory ==========
if "trip_chat" not in st.session_state:
    st.session_state.trip_chat = [
        {"role": "system", "content": "You are a friendly travel planner AI. You help users build personalized travel itineraries, suggest destinations, and give tips based on their preferences like budget, season, and travel style."}
    ]

def add_message(role, content):
    st.session_state.trip_chat.append({"role": role, "content": content})
    if len(st.session_state.trip_chat) > 30:
        st.session_state.trip_chat = st.session_state.trip_chat[-30:]

# ========== Mode 1: Trip Planning Chat ==========
if mode == "🗺️ Plan a Trip":
    st.header("🗺️ Plan Your Dream Trip")
    prompt = st.text_input("Tell me what kind of trip you want to plan (e.g. '10 days in Italy, budget-friendly, foodie focus'):")

    if st.button("📍 Plan My Trip") and prompt.strip():
        add_message("user", prompt.strip())
        try:
            with st.spinner("Crafting your itinerary..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=st.session_state.trip_chat
                )
            result = response.choices[0].message.content
            add_message("assistant", result)
            st.success("🧳 Trip Plan Ready!")
            st.markdown(result)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    with st.expander("📖 See Conversation History"):
        for msg in st.session_state.trip_chat[1:]:
            st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")

# ========== Mode 2: General Travel Chat ==========
elif mode == "💬 Travel Chat":
    st.header("💬 Chat with Your Travel Assistant")
    user_q = st.text_input("Ask me anything about travel (visas, safety, best months to go, etc.):")

    if st.button("💬 Ask") and user_q.strip():
        add_message("user", user_q.strip())
        try:
            with st.spinner("Answering your travel question..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=st.session_state.trip_chat
                )
            reply = response.choices[0].message.content
            add_message("assistant", reply)
            st.success("✅ Got it!")
            st.markdown(reply)
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    with st.expander("📖 Chat History"):
        for msg in st.session_state.trip_chat[1:]:
            st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")

# ========== Mode 3: Image Generator ==========
elif mode == "📷 Generate Destination Image":
    st.header("📷 Imagine Your Destination")
    description = st.text_input("Describe a destination or travel scene you'd like to visualize:")

    if st.button("🎨 Generate Image") and description.strip():
        try:
            with st.spinner("Generating your dream view..."):
                response = client.images.generate(
                    prompt=description,
                    n=1,
                    size="512x512"
                )
            image_url = response.data[0].url
            st.image(image_url, caption="Your AI-generated travel scene 🌅", use_column_width=True)
            st.success("✨ Here's your image!")
        except Exception as e:
            st.error(f"Error: {e}")
