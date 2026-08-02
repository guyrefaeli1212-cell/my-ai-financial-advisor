import streamlit as st
import google.generativeai as genai
import os

# הגדרת עיצוב הדף
st.set_page_config(page_title="AI Financial Advisor", page_icon="💰", layout="centered")

st.title("💰 יועץ פיננסי אישי - AI")
st.write("שלום! אני הבוט הפיננסי האישי שלך. שאל אותי כל שאלה על תקציב, חיסכון או תכנון פיננסי.")

# חיבור למפתח ה-API של גוגל
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ מפתח ה-API חסר. יש להגדיר את GEMINI_API_KEY בהגדרות ה-Streamlit.")
else:
    genai.configure(api_key=api_key)
    
    # חיבור לדגם הנתמך והעדכני ביותר
    model = genai.GenerativeModel('gemini-2.0-flash')

    # אתחול היסטוריית הצ'אט
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "היי! איך אני יכול לעזור לך להתנהל נכון יותר עם הכסף שלך היום?"}
        ]

    # הצגת הודעות קודמות בצ'אט
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # תיבת קלט מהמשתמש
    if user_input := st.chat_input("שאל אותי משהו (למשל: איך לחסוך 1,000 ש\"ח בחודש?)..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("חושב על תשובה..."):
                prompt = f"""
                אתה יועץ פיננסי מקצועי, אדיב ואחראי. 
                ענה למשתמש בצורה נגישה, ברורה ומועילה בעברית.
                
                שאלה/הודעה: {user_input}
                """
                try:
                    response = model.generate_content(prompt)
                    bot_reply = response.text
                except Exception as e:
                    # מנגנון גיבוי (Fallback) למקרה של בעיה בדגם הספציפי
                    try:
                        fallback_model = genai.GenerativeModel('gemini-1.5-flash-latest')
                        response = fallback_model.generate_content(prompt)
                        bot_reply = response.text
                    except Exception as err:
                        bot_reply = f"ארעה שגיאה: {err}"
                
                st.write(bot_reply)

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
