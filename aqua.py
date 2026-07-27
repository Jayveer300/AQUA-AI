import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text
import streamlit as st
from google import genai

from config import GEMINI_API_KEY
from prompt import SYSTEM_PROMPT
from voice import text_to_audio
def microphone_html():
    components.html("""
    <button id="micButton" style="
        background:#0077cc;
        color:white;
        border:none;
        border-radius:50%;
        width:60px;
        height:60px;
        font-size:28px;
        cursor:pointer;">
        🎤
    </button>

    <p id="status">Click the microphone</p>

    <script>
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if(SpeechRecognition){
        const recognition = new SpeechRecognition();

        recognition.lang = "en-IN";
        recognition.interimResults = false;

        document.getElementById("micButton").onclick = function(){

            document.getElementById("status").innerHTML = "🎙 Listening...";

            recognition.start();

        };

        recognition.onresult = function(event){

            const text = event.results[0][0].transcript;

            parent.postMessage({
                isStreamlitMessage:true,
                type:"streamlit:setComponentValue",
                value:text
            },"*");

        };

        recognition.onend = function(){

            document.getElementById("status").innerHTML="Finished";

        };
    }
    </script>
    """, height=130)

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="AQUA AI",
    page_icon="🌊",
    layout="wide"
)

# -----------------------------
# GEMINI CLIENT
# -----------------------------
client = genai.Client(api_key=AQ.Ab8RN6Kvr5I2FOQ0bXCZbM25OupCZMMRsnrEDLhYSo93dBJk6Q)

# -----------------------------
# PROJECT INTRODUCTION
# -----------------------------
PROJECT_INTRODUCTION = """
AQUA is an AI-powered Smart Water Management and Wind Energy System.

English:
Our project demonstrates an integrated water management system. Water is stored in an overhead tank and then flows through a turbine, generating clean electricity to power street lights. After electricity generation, the water passes through a filtration system and is supplied to houses. A separate well collects groundwater into a collection tank, and a submersible pump pumps the water back to the overhead tank, creating a continuous water cycle. This system promotes renewable energy, water conservation, and sustainable water management.

Hindi:
हमारा प्रोजेक्ट एक स्मार्ट जल प्रबंधन प्रणाली को दर्शाता है। पानी सबसे पहले एक ऊपरी टैंक में संग्रहित किया जाता है। वहाँ से पानी टरबाइन से होकर गुजरता है, जिससे बिजली उत्पन्न होती है और स्ट्रीट लाइट जलती है। इसके बाद पानी फ़िल्ट्रेशन प्रणाली से होकर घरों तक पहुँचता है। एक अलग कुएँ से पानी कलेक्शन टैंक में आता है और सबमर्सिबल पंप द्वारा फिर से ऊपरी टैंक में भेजा जाता है। यह प्रणाली जल संरक्षण, स्वच्छ ऊर्जा और सतत जल प्रबंधन को बढ़ावा देती है।

Gujarati:
અમારો પ્રોજેક્ટ સ્માર્ટ વોટર મેનેજમેન્ટ સિસ્ટમ દર્શાવે છે. પાણી ઓવરહેડ ટાંકીમાં સંગ્રહિત થાય છે અને પછી ટર્બાઇનમાંથી પસાર થાય છે, જેના કારણે વીજળી ઉત્પન્ન થાય છે અને સ્ટ્રીટ લાઇટ ચાલુ થાય છે. ત્યારબાદ પાણી ફિલ્ટરેશન પ્રક્રિયામાંથી પસાર થઈ ઘર સુધી પહોંચે છે. અલગ કૂવામાંથી પાણી કલેક્શન ટાંકીમાં આવે છે અને સબમર્સિબલ પંપની મદદથી ફરી ઓવરહેડ ટાંકીમાં મોકલવામાં આવે છે. આ સિસ્ટમ પાણી બચત, સ્વચ્છ ઊર્જા અને ટકાઉ જળ વ્યવસ્થાપનને પ્રોત્સાહન આપે છે.

Always answer briefly and directly. If the user asks for the project introduction, reply in the same language as the user's question.
"""

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main{
    background:#eef7ff;
}
.title{
    text-align:center;
    color:#0077cc;
    font-size:42px;
    font-weight:bold;
}
.subtitle{
    text-align:center;
    color:gray;
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    "<h1 class='title'>🌊 AQUA AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Smart Water Management & Wind Energy Assistant</p>",
    unsafe_allow_html=True
)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("🌊 AQUA")
    st.write("### Languages")
    st.write("✅ English")
    st.write("✅ हिन्दी")
    st.write("✅ ગુજરાતી")
    st.divider()
    st.write("Science Exhibition AI Assistant")

# -----------------------------
# CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
st.markdown("### 🎤 Speak to AQUA")

voice_question = microphone_html

if isinstance(voice_question, dict):
    question = voice_question.get("text", "")
else:
    question = voice_question

# Text Input
typed_question = st.chat_input("Ask AQUA anything...")

if typed_question:
    question = typed_question

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            full_prompt = f"""
{SYSTEM_PROMPT}

Project Introduction:
{PROJECT_INTRODUCTION}

User Question:
{question}
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt
                )

                answer = response.text

            except Exception as e:
                answer = f"Error: {e}"

            st.markdown(answer)
            import base64

            try:
                audio_file = text_to_audio(answer)

                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()

                audio_base64 = base64.b64encode(audio_bytes).decode()

                st.markdown(
                    f"""
                    <audio autoplay>
                          <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.warning(f"Voice Error: {e}")                

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )