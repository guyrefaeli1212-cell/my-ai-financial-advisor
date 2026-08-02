import streamlit as st
from openai import OpenAI
import os

# הגדרת עיצוב הדף
st.set_page_config(page_title="AI Financial Advisor", page_icon="💰", layout="centered")

st.title("💰 יועץ פיננסי אישי - AI")
st.write("שלום! אני הבוט הפיננסי האישי שלך (מבוסס ChatGPT). שאל אותי כל שאלה על תקציב, חיסכון או תכנון פיננסי.")

# חיבור למפתח ה-API של OpenAI
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ מפתח ה-API חסר. יש להגדיר את OPENAI_API_KEY בהגדרות ה-Streamlit Secrets.")
else:
    client = OpenAI(api_key=api_key)

    # אתחול היסטוריית הצ'אט
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "אתה יועץ פיננסי מקצועי, אדיב ואחראי. ענה למשתמש בצורה נגישה, ברורה ומועילה בעברית."},
            {"role": "assistant", "content": "היי! איך אני יכול לעזור לך להתנהל נכון יותר עם הכסף שלך היום?"}
        ]

    # הצגת הודעות קודמות בצ'אט (ללא הודעת המערכת)
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # תיבת קלט מהמשתמש
    if user_input := st.chat_input("שאל אותי משהו (למשל: איך לחסוך 1,000 ש\"ח בחודש?)..."):
        # הוספת הודעת המשתמש
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # פנייה ל-OpenAI
        with st.chat_message("assistant"):
            with st.spinner("חושב על תשובה..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.messages
                    )
                    bot_reply = response.choices[0].message.content
                except Exception as e:
                    bot_reply = f"ארעה שגיאה: {e}"
                
                st.write(bot_reply)

        # שמירת תשובת הבוט בהיסטוריה
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
