import streamlit as st
import requests
import base64
from gtts import gTTS
import io
import urllib.parse
import re

# --- પેજ સેટિંગ ---
st.set_page_config(page_title="AI કૃષિ કવચ", page_icon="🛡️", layout="centered", initial_sidebar_state="collapsed")

# --- પ્રીમિયમ CSS ---
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp { background-color: #f4f7f6; }

/* ટોપ હેડર */
.app-header {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    padding: 20px;
    border-radius: 0 0 25px 25px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(27, 94, 32, 0.4);
    margin-top: -60px;
    margin-bottom: 20px;
}
.app-header h1 { font-size: clamp(26px, 6vw, 36px); font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); color: white;}
.app-header p { font-size: clamp(14px, 3vw, 16px); margin: 5px 0 0 0; opacity: 0.9; }

/* પ્રોજેક્ટ કાર્ડ */
.info-card {
    background: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    margin-bottom: 25px;
    border-top: 5px solid #ff9800;
    text-align: center;
}
.info-title { color: #1b5e20; font-size: clamp(20px, 4vw, 24px); font-weight: 900; margin-bottom: 5px; }
.info-text { font-size: clamp(14px, 3vw, 16px); color: #424242; margin-bottom: 5px; line-height: 1.5; }
.info-highlight { color: #e65100; font-weight: bold; font-size: clamp(15px, 3vw, 17px); margin: 10px 0; }

.custom-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.06);
    margin-bottom: 25px;
    border-top: 5px solid #4caf50;
}
.section-title {
    color: #1b5e20;
    font-size: clamp(18px, 4vw, 22px);
    font-weight: bold;
    margin-bottom: 15px;
    border-bottom: 2px dashed #c8e6c9;
    padding-bottom: 10px;
}

div.stButton > button:first-child {
    background: linear-gradient(90deg, #43a047, #2e7d32);
    color: white;
    border-radius: 50px;
    font-size: clamp(16px, 4vw, 20px);
    font-weight: bold;
    padding: 12px 20px;
    border: none;
    box-shadow: 0 6px 15px rgba(46, 125, 50, 0.4);
    transition: 0.3s;
    width: 100%;
}
div.stButton > button:first-child:hover { transform: scale(1.02); }

.report-greeting {
    font-size: clamp(20px, 4.5vw, 24px);
    color: #e65100;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
    border-bottom: 2px solid #ffe0b2;
    padding-bottom: 10px;
}

.action-container { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 25px; }
.action-btn { padding: 12px 15px; border-radius: 12px; text-decoration: none !important; font-weight: bold; font-size: clamp(14px, 3vw, 16px); flex: 1 1 180px; text-align: center; color: white !important; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
.btn-wa { background: linear-gradient(135deg, #25D366, #128C7E); }
.btn-yt { background: linear-gradient(135deg, #FF0000, #cc0000); }

audio { width: 100%; border-radius: 10px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("""
<div class="app-header">
    <h1>🛡️ AI કૃષિ કવચ</h1>
    <p>પાક, પ્રકૃતિ અને પૈસાનો રક્ષક</p>
</div>
""", unsafe_allow_html=True)

# --- વિજ્ઞાન મેળાની વિગતો ---
st.markdown("""
<div class="info-card">
    <div class="info-title">શ્રી ચિત્રાસર પ્રાથમિક શાળા</div>
    <div class="info-text">મુ. ચિત્રાસર, તા. ખેડા, જી. ખેડા</div>
    <div class="info-highlight">નવાગામ ક્લસ્ટર કક્ષાનું વિજ્ઞાન, ગણિત અને પર્યાવરણ પ્રદર્શન : ૨૦૨૬-૨૭</div>
    <hr style='border: 1px dashed #e0e0e0; margin: 15px 0;'>
    <div class="info-text"><b>મુખ્ય વિષય:</b> ટકાઉ અને વિકસિત ભારત માટે વિજ્ઞાન, ટેકનોલોજી અને ઈનોવેશન</div>
    <div class="info-text" style="margin-bottom: 15px;"><b>વિભાગ:</b> 1. (A) બહેતર જીવન માટે આર્ટિફિશિયલ ઇન્ટેલિજન્સ (AI)</div>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: left; background: #f9fbe7; padding: 15px; border-radius: 10px;">
        <div style="margin-bottom: 10px;"><b>👨‍🎓 વિદ્યાર્થીઓ:</b><br>૧. મેઘાબેન દશરથભાઈ સોઢાપરમાર<br>૨. અંજલી ગોવિંદભાઈ ભરવાડ</div>
        <div><b>👨‍🏫 માર્ગદર્શક શિક્ષક:</b><br>ચેયુષભાઈ એન પટેલ</div>
    </div>
</div>
""", unsafe_allow_html=True)

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("⚠️ API Key મળતી નથી! સિક્યોરિટી સેટિંગ તપાસો.")
    st.stop()

# --- ઓટોમેટિક લાઈવ લોકેશન (કોઈ બટન વગર) ---
if 'live_location' not in st.session_state:
    st.session_state.live_location = "અજ્ઞાત"
    try:
        ip_res = requests.get('http://ip-api.com/json/', timeout=3).json()
        if ip_res['status'] == 'success':
            st.session_state.live_location = ip_res.get('city', ip_res.get('regionName', 'અજ્ઞાત'))
    except:
        pass

# --- સેટિંગ્સ અને લોકેશન ડિસ્પ્લે ---
st.markdown("<div class='custom-card'><div class='section-title'>⚙️ સેટિંગ્સ અને માહિતી</div>", unsafe_allow_html=True)
st.success(f"📍 તમારું ઓટોમેટિક લાઈવ લોકેશન: **{st.session_state.live_location}**")
languages = {"ગુજરાતી (Gujarati)": "gu", "हिंदी (Hindi)": "hi", "मराठी (Marathi)": "mr", "English": "en"}
selected_lang = st.selectbox("તમારી ભાષા પસંદ કરો:", list(languages.keys()), label_visibility="collapsed")
target_lang_code = languages[selected_lang]
target_lang_name = selected_lang.split(' ')[0]
voice_enabled = st.toggle("🔊 ઓડિયો રિપોર્ટ (બોલીને સંભળાવો)", value=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- ફોટો અપલોડ ---
st.markdown("<div class='custom-card'><div class='section-title'>📸 પાકનો ફોટો પાડો</div>", unsafe_allow_html=True)
st.info("💡 શ્રેષ્ઠ નિદાન માટે બે ફોટા પાડો: (૧) બીમાર પાંદડાની નજીકથી અને (૨) આખા છોડનો ફોટો.")
uploaded_files = st.file_uploader("અહીં ક્લિક કરી ફોટો પાડો", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# --- પ્રોસેસિંગ ---
if uploaded_files:
    st.markdown("<div class='custom-card'><div class='section-title'>🖼️ પસંદ કરેલા ફોટા</div>", unsafe_allow_html=True)
    cols = st.columns(len(uploaded_files))
    for idx, file in enumerate(uploaded_files):
        cols[idx].image(file, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚀 વિશ્લેષણ કરો (રોગ, માપ અને હવામાન)"):
        weather_details = "લોકેશનની ચોક્કસ માહિતી ન હોવાથી હવામાન ડેટા ઉપલબ્ધ નથી."
        
        # હવામાન ડેટા ખેંચવો
        if st.session_state.live_location != "અજ્ઞાત":
            try:
                geo_res = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={st.session_state.live_location}&count=1", timeout=5).json()
                if "results" in geo_res and len(geo_res["results"]) > 0:
                    lat, lon = geo_res["results"][0]["latitude"], geo_res["results"][0]["longitude"]
                    w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_probability_max&timezone=auto&forecast_days=3", timeout=5).json()
                    
                    today = w_res["daily"]["precipitation_probability_max"][0]
                    tomorrow = w_res["daily"]["precipitation_probability_max"][1]
                    day_after = w_res["daily"]["precipitation_probability_max"][2]
                    
                    max_rain = max(today, tomorrow, day_after)
                    if max_rain < 40:
                        advice = "હાલ વાતાવરણ એકદમ અનુકૂળ છે, તમે આજે જ દવાનો છંટકાવ કરી શકો છો."
                    else:
                        advice = "⚠️ ચેતવણી: આગામી દિવસોમાં વરસાદની શક્યતા વધુ છે. આજે દવા છાંટતા નહિ, નહીંતર દવા ધોવાઈ જશે અને તમારો ખર્ચ માથે પડશે!"
                        
                    weather_details = f"આજે વરસાદની શક્યતા {today}%, આવતીકાલે {tomorrow}%, અને પરમદિવસે {day_after}% છે.\n\n**AI સલાહ:** {advice}"
            except:
                pass

        status_placeholder = st.empty()
        status_placeholder.info("⏳ AI તમારા ફોટાનું અને હવામાનનું ગહન વિશ્લેષણ કરી રહ્યું છે... કૃપા કરીને રાહ જુઓ.")
        
        # --- સુધારેલ કડક પ્રોમ્પ્ટ (Clear Formatting & Strict Weather) ---
        smart_prompt = f"""
        Analyze ALL provided crop images. Provide response STRICTLY in {target_lang_name} language. 
        IMPORTANT FORMATTING RULES: 
        1. Use proper Markdown Headings (###) for each section.
        2. Leave a DOUBLE NEWLINE (\\n\\n) after every single section so they do not mix together.
        3. Explain in clear, simple bullet points.
        
        ### ૧. 🌾 પાક અને રોગનું નામ: 
        (Provide accurate crop and disease name)
        
        ### ૨. 📊 રોગની અસર (Severity %): 
        (Provide percentage and brief detail)
        
        ### ૩. 🌦️ હવામાન રિપોર્ટ અને દવાની સલાહ ({st.session_state.live_location}):
        (YOU MUST EXACTLY COPY THIS TEXT: {weather_details})
        
        ### ૪. 🌿 પ્રાકૃતિક / ઓર્ગેનિક ઉપાય (પ્રથમ પસંદગી):
        (GIVE HIGHEST PRIORITY. Suggest 2-3 organic methods like જીવામૃત, નીમાસ્ત્ર, ખાટી છાશ etc. CLEARLY specify exact mixing ratio for a 15-liter pump).
        
        ### ૫. 🧪 રાસાયણિક ઉપાય (વૈકલ્પિક):
        (Provide chemical alternative ONLY as a backup. Specify exact 15-liter pump dosage. Add a warning about soil damage).
        
        ### ૬. 🧮 પંપ અને દવાની ગણતરી: 
        (૧ વીઘા = ૨૪ ગુંઠા માટે અંદાજે ૩ પંપ (15 Liters each) વાપરવા. ખેડૂતને ગણતરી સમજાવો).
        
        [YT_SEARCH: Keyword1, Keyword2] (Provide 1 or 2 organic method names you just suggested, comma separated)
        """

        contents_parts = [{"text": smart_prompt}]
        for file in uploaded_files:
            base64_image = base64.b64encode(file.getvalue()).decode('utf-8')
            mime_type = "image/jpeg" if file.name.endswith(('jpg', 'jpeg')) else "image/png"
            contents_parts.append({"inlineData": {"mimeType": mime_type, "data": base64_image}})

        data = {"contents": [{"parts": contents_parts}]}
        headers = {'Content-Type': 'application/json'}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={API_KEY}"
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                text_response = response.json()['candidates'][0]['content']['parts'][0]['text']
                status_placeholder.empty()
                
                # Extract YouTube Keywords
                yt_keywords = []
                yt_match = re.search(r'\[YT_SEARCH:\s*(.*?)\]', text_response)
                if yt_match:
                    yt_keywords = [kw.strip() for kw in yt_match.group(1).split(',') if kw.strip()]
                    text_response = re.sub(r'\[YT_SEARCH:\s*.*?\]', '', text_response).strip()
                
                # --- WhatsApp માટે ચોખ્ખું લખાણ અને ઓટોમેટિક લિંક્સ બનાવવી ---
                clean_text_for_sharing = re.sub(r'<[^>]+>', '', text_response).strip()
                
                whatsapp_msg = f"🛡️ *AI કૃષિ કવચ - સ્માર્ટ રિપોર્ટ ({st.session_state.live_location})* 🛡️\n\n{clean_text_for_sharing}\n\n"
                
                if yt_keywords:
                    whatsapp_msg += "📺 *પ્રાકૃતિક દવા ઘરે બનાવવાના વિડીયો:*\n"
                    for kw in yt_keywords:
                        yt_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(kw + ' banavvani rit')}"
                        whatsapp_msg += f"👉 {kw}: {yt_url}\n"
                
                whatsapp_msg += "\nસૌજન્ય: ચિત્રાસર પ્રાથમિક શાળા પ્રોજેક્ટ"
                
                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                
                if voice_enabled:
                    audio_clean_text = re.sub(r'[*#_🚨💡🌿🧪🌾📊🌦️🧮]', ' ', clean_text_for_sharing)
                    audio_text = f"નમસ્કાર ખેડૂત મિત્ર. તમારો રિપોર્ટ આ મુજબ છે: {audio_clean_text}"
                    try:
                        tts = gTTS(text=audio_text, lang=target_lang_code)
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)
                        audio_b64 = base64.b64encode(fp.read()).decode()
                        st.markdown(f'''<audio autoplay controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>''', unsafe_allow_html=True)
                    except:
                        pass
                
                st.markdown("<div class='report-greeting'>🌾 ખેડૂત મિત્ર, આ રહ્યો તમારો સ્માર્ટ રિપોર્ટ:</div>", unsafe_allow_html=True)
                
                # રિપોર્ટ પ્રિન્ટ
                st.markdown(text_response)
                
                # Action Buttons
                html_buttons = '<div class="action-container">'
                encoded_msg = urllib.parse.quote(whatsapp_msg)
                html_buttons += f'<a href="https://api.whatsapp.com/send?text={encoded_msg}" target="_blank" class="action-btn btn-wa">💬 WhatsApp પર રિપોર્ટ અને વિડીયો લિંક શેર કરો</a>'
                html_buttons += '</div>'
                
                st.markdown(html_buttons, unsafe_allow_html=True)
                
                st.write("") 
                st.download_button(
                    label="📄 આ રિપોર્ટ મોબાઈલમાં સેવ કરો (Download TXT)",
                    data=whatsapp_msg,
                    file_name="Krushi_Kavach_Report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("ગૂગલ સર્વર વ્યસ્ત છે. કૃપા કરીને થોડીવાર પછી ફરી પ્રયાસ કરો.")
        except Exception as e:
            st.error(f"ઇન્ટરનેટ કનેક્શન એરર: {e}")
