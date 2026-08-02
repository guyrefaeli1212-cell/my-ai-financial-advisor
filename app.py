import streamlit as st
from google import genai
import os

st.set_page_config(page_title="AI Financial Advisor", page_icon="💰", layout="centered")

st.title("💰 יועץ פיננסי אישי - AI")
st.write("שלום! אני הבוט הפיננסי האישי שלך. שאל אותי כל שאלה על תקציב, חיסכון או תכנון פיננסי.")

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ מפתח ה-API חסר. יש להגדיר את GEMINI_API_KEY בהגדרות ה-Streamlit Secrets.")
else:
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "היי! איך אני יכול לעזור לך להתנהל נכון יותר עם הכסף שלך היום?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("שאל אותי משהו..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("חושב על תשובה..."):
                prompt = f"אתה יועץ פיננסי מקצועי, אדיב ואחראי. ענה בצורה נגישה ומועילה בעברית.\n\nשאלה: {user_input}"
                
                try:
                    # שימוש ב-gemini-1.5-flash לווידוא מכסה זמינה
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt,
                    )
                    bot_reply = response.text
                except Exception as e:
                    bot_reply = f"ארעה שגיאה בחיבור לשרת: {e}"
                
                st.write(bot_reply)

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
