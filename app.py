import streamlit as st
import requests
import base64
from gtts import gTTS
import io
import urllib.parse
import re
import time

# --- પેજ સેટિંગ ---
st.set_page_config(page_title="AI કૃષિ કવચ", page_icon="🛡️", layout="centered", initial_sidebar_state="collapsed")

# --- પ્રીમિયમ CSS (Android App જેવો લુક) ---
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

/* પ્રોજેક્ટ વિગતો માટેનું ખાસ કાર્ડ */
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
    padding: 25px;
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

/* ડિજિટલ પેજ જેવો રિપોર્ટ લુક */
.report-page {
    background: #ffffff;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    font-size: clamp(16px, 3.5vw, 18px);
    line-height: 1.8;
    color: #333333;
    margin-top: 15px;
    position: relative;
}
.report-page::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 8px;
    background: linear-gradient(90deg, #ff9800, #4caf50);
    border-radius: 12px 12px 0 0;
}
.report-greeting {
    font-size: clamp(20px, 4.5vw, 24px);
    color: #e65100;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    border-bottom: 2px solid #ffe0b2;
    padding-bottom: 10px;
}

.blinking-warning { 
    animation: alert-blink 1s infinite; 
    padding: 15px; border-radius: 10px; 
    font-size: clamp(16px, 3.5vw, 20px); font-weight: 900; text-align: center; 
    margin: 20px 0; box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3); border: 2px solid #ff0000; 
}
@keyframes alert-blink { 0% { background-color: #fff; color: #f00; } 50% { background-color: #ffeaea; color: #d00; } 100% { background-color: #fff; color: #f00; } }

.action-container { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 25px; }
.action-btn { padding: 12px 15px; border-radius: 12px; text-decoration: none !important; font-weight: bold; font-size: clamp(14px, 3vw, 16px); flex: 1 1 180px; text-align: center; color: white !important; box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
.btn-wa { background: linear-gradient(135deg, #25D366, #128C7E); }
.btn-yt { background: linear-gradient(135deg, #FF0000, #cc0000); }
.btn-pm { background: linear-gradient(135deg, #f39c12, #d35400); }

audio { width: 100%; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("""
<div class="app-header">
    <h1>🛡️ AI કૃષિ કવચ</h1>
    <p>પાક, પ્રકૃતિ અને પૈસાનો રક્ષક</p>
</div>
""", unsafe_allow_html=True)

# --- વિજ્ઞાન મેળાની વિગતો (નવું આકર્ષક કાર્ડ) ---
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

# --- સેટિંગ્સ ---
st.markdown("<div class='custom-card'><div class='section-title'>⚙️ ભાષા અને સેટિંગ્સ</div>", unsafe_allow_html=True)
languages = {"ગુજરાતી (Gujarati)": "gu", "हिंदी (Hindi)": "hi", "मराठी (Marathi)": "mr", "English": "en"}
selected_lang = st.selectbox("તમારી ભાષા પસંદ કરો:", list(languages.keys()), label_visibility="collapsed")
target_lang_code = languages[selected_lang]
target_lang_name = selected_lang.split(' ')[0]
voice_enabled = st.toggle("🔊 ઓડિયો રિપોર્ટ (બોલીને સંભળાવો)", value=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- ફોટો અપલોડ ---
st.markdown("<div class='custom-card'><div class='section-title'>📸 ૧. પાકનો ફોટો પાડો</div>", unsafe_allow_html=True)
st.info("💡 શ્રેષ્ઠ નિદાન માટે બે ફોટા પાડો: (૧) બીમાર પાંદડાની નજીકથી અને (૨) આખા છોડનો ફોટો.")
uploaded_files = st.file_uploader("અહીં ક્લિક કરી ફોટો પાડો", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# --- લોકેશન ---
st.markdown("<div class='custom-card'><div class='section-title'>📍 ૨. લોકેશન (હવામાનની સલાહ માટે)</div>", unsafe_allow_html=True)
location_method = st.radio("તમારું લોકેશન કેવી રીતે આપશો?", ["૧. ઑટોમેટિક મારું લાઈવ લોકેશન લો 📍", "૨. પિનકોડ દ્વારા 🔢", "૩. હવામાનની માહિતી નથી જોઈતી ❌"], label_visibility="collapsed")

search_query_for_weather = "SKIP"
display_location_name = "લોકેશન આપેલ નથી"

if location_method.startswith("૧"):
    try:
        ip_res = requests.get('http://ip-api.com/json/', timeout=5).json()
        if ip_res['status'] == 'success':
            search_query_for_weather = ip_res['city']
            display_location_name = f"Live Location ({ip_res['city']})"
            st.success(f"✅ લોકેશન સેટ: {ip_res['city']}")
    except:
        st.warning("લોકેશન મળ્યું નહિ, પિનકોડ નો ઉપયોગ કરો.")
elif location_method.startswith("૨"):
    pincode = st.text_input("પિનકોડ લખો:", placeholder="દા.ત. 387411", label_visibility="collapsed")
    if pincode and len(pincode) == 6:
        search_query_for_weather = pincode
        display_location_name = f"પિનકોડ {pincode}"
st.markdown("</div>", unsafe_allow_html=True)

# --- પ્રોસેસિંગ ---
if uploaded_files:
    st.markdown("<div class='custom-card'><div class='section-title'>🖼️ પસંદ કરેલા ફોટા</div>", unsafe_allow_html=True)
    cols = st.columns(len(uploaded_files))
    for idx, file in enumerate(uploaded_files):
        cols[idx].image(file, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚀 વિશ્લેષણ કરો (રોગ, માપ અને હવામાન)"):
        today_rain = tomorrow_rain = day_after_rain = 0
        weather_data_success = False
        
        if search_query_for_weather != "SKIP":
            try:
                geo_res = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={search_query_for_weather}&count=1", timeout=5).json()
                if "results" in geo_res:
                    lat, lon = geo_res["results"][0]["latitude"], geo_res["results"][0]["longitude"]
                    w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_probability_max&timezone=auto&forecast_days=3", timeout=5).json()
                    today_rain, tomorrow_rain, day_after_rain = w_res["daily"]["precipitation_probability_max"][:3]
                    weather_data_success = True
            except:
                pass

        status_placeholder = st.empty()
        status_placeholder.info("⏳ AI તમારા ફોટાનું ગહન વિશ્લેષણ કરી રહ્યું છે... કૃપા કરીને રાહ જુઓ.")
        
        if weather_data_success:
            max_rain = max(today_rain, tomorrow_rain, day_after_rain)
            smart_advice = "હાલ વાતાવરણ એકદમ અનુકૂળ છે, તમે દવા છાંટી શકો છો." if max_rain < 50 else "⚠️ ચેતવણી: વરસાદની શક્યતા વધુ હોવાથી આજે દવા છાંટતા નહિ, નહીંતર દવા ધોવાઈ જશે!"
            weather_instruction = f"**૩. 🌦️ હવામાન ({display_location_name}):** આજે {today_rain}%, કાલે {tomorrow_rain}%. **સલાહ:** {smart_advice}"
        else:
            weather_instruction = "**૩. 🌦️ હવામાન:** માહિતી ઉપલબ્ધ નથી."

        smart_prompt = f"""
        Analyze ALL provided crop images. Provide response STRICTLY in {target_lang_name} language. 
        Format beautifully with bullet points.
        ૧. 🌾 પાક/છોડ અને રોગનું નામ: 
        ૨. 📊 રોગની અસર (Severity %): 
        {weather_instruction}
        ૪. 🚨 તાત્કાલિક પગલાં: WRAP INSIDE HTML TAG: <div class='blinking-warning'> 🚨 તાત્કાલિક પગલાં: [Action time frame] </div>
        ૫. 💡 ઉપાય અને સચોટ માપ: 
           - 🌿 પ્રાકૃતિક ઉપાય (૧૫ લિટર પંપ દીઠ સચોટ ગણતરી):
           - 🧪 રાસાયણિક ઉપાય (૧૫ લિટર પંપ દીઠ સચોટ ગણતરી):
        ૬. 🧮 જમીન મુજબ પંપ ગણતરી: ૧ વીઘા (૨૪ ગુંઠા) માટે અંદાજે ૩ પંપ.
        [YT_SEARCH: Keyword1, Keyword2]
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
                
                yt_keywords = []
                yt_match = re.search(r'\[YT_SEARCH:\s*(.*?)\]', text_response)
                if yt_match:
                    yt_keywords = [kw.strip() for kw in yt_match.group(1).split(',')]
                    text_response = re.sub(r'\[YT_SEARCH:\s*.*?\]', '', text_response).strip()
                
                # --- HTML કોડ રિમૂવલ (WhatsApp અને Download માટે ચોખ્ખું લખાણ) ---
                clean_text_for_sharing = re.sub(r'<[^>]+>', '', text_response).strip()
                
                st.markdown("<div class='custom-card'><div class='section-title'>✅ તમારો સ્માર્ટ રિપોર્ટ</div>", unsafe_allow_html=True)
                
                if voice_enabled:
                    audio_clean_text = re.sub(r'[*#_🚨💡🌿🧪🌾]', ' ', clean_text_for_sharing)
                    audio_text = f"નમસ્કાર ખેડૂત મિત્ર. તમારો રિપોર્ટ આ મુજબ છે: {audio_clean_text}"
                    try:
                        tts = gTTS(text=audio_text, lang=target_lang_code)
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)
                        audio_b64 = base64.b64encode(fp.read()).decode()
                        st.markdown(f'''<div style="margin-bottom:15px;"><audio autoplay controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio></div>''', unsafe_allow_html=True)
                    except:
                        pass
                
                # --- સુંદર પેજ ફોર્મેટિંગ અને હેડિંગ ---
                st.markdown(f"""
                <div class='report-page'>
                    <div class='report-greeting'>🌾 ખેડૂત મિત્ર, આ રહ્યો તમારા પાકનો સ્માર્ટ રિપોર્ટ:</div>
                    {text_response}
                </div>
                """, unsafe_allow_html=True)
                
                # --- Action Buttons ---
                html_buttons = '<div class="action-container">'
                
                # WhatsApp Button (Clean Text)
                whatsapp_msg = f"🛡️ *AI કૃષિ કવચ - સ્માર્ટ રિપોર્ટ* 🛡️\n\n{clean_text_for_sharing}\n\nસૌજન્ય: ચિત્રાસર પ્રાથમિક શાળા પ્રોજેક્ટ"
                encoded_msg = urllib.parse.quote(whatsapp_msg)
                html_buttons += f'<a href="https://api.whatsapp.com/send?text={encoded_msg}" target="_blank" class="action-btn btn-wa">💬 WhatsApp શેર</a>'
                
                for kw in yt_keywords:
                    yt_query = urllib.parse.quote(f"How to make {kw} organic farming in {target_lang_name}")
                    html_buttons += f'<a href="https://www.youtube.com/results?search_query={yt_query}" target="_blank" class="action-btn btn-yt">📺 {kw} શીખો</a>'
                
                html_buttons += f'<a href="https://pmfby.gov.in/" target="_blank" class="action-btn btn-pm">🌾 પાક વીમા અરજી</a>'
                html_buttons += '</div>'
                
                st.markdown(html_buttons, unsafe_allow_html=True)
                
                # --- ડાઉનલોડ બટન (.txt ફાઈલ) ---
                st.write("") # Spacing
                st.download_button(
                    label="📄 આ રિપોર્ટ મોબાઈલમાં સેવ કરો (Download)",
                    data=whatsapp_msg,
                    file_name="Krushi_Kavach_Report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("ગૂગલ સર્વર વ્યસ્ત છે. કૃપા કરીને ફરી પ્રયાસ કરો.")
        except Exception as e:
            st.error(f"ઇન્ટરનેટ કનેક્શન એરર: {e}")
