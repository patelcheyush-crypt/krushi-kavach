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

# --- પ્રીમિયમ CSS ---
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp { background-color: #f4f7f6; }

.app-header { background: linear-gradient(135deg, #1b5e20, #2e7d32); padding: 20px; border-radius: 0 0 25px 25px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(27, 94, 32, 0.4); margin-top: -60px; margin-bottom: 20px; }
.app-header h1 { font-size: clamp(26px, 6vw, 36px); font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); color: white;}
.app-header p { font-size: clamp(14px, 3vw, 16px); margin: 5px 0 0 0; opacity: 0.9; }

.info-card { background: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); margin-bottom: 25px; border-top: 5px solid #ff9800; text-align: center; }
.info-title { color: #1b5e20; font-size: clamp(20px, 4vw, 24px); font-weight: 900; margin-bottom: 5px; }
.info-text { font-size: clamp(14px, 3vw, 16px); color: #424242; margin-bottom: 5px; line-height: 1.5; }
.info-highlight { color: #e65100; font-weight: bold; font-size: clamp(15px, 3vw, 17px); margin: 10px 0; }
.info-date-venue { color: #d32f2f; font-weight: 900; font-size: clamp(15px, 3vw, 17px); margin-bottom: 10px; background-color: #ffebee; padding: 5px; border-radius: 8px; display: inline-block; }

.custom-card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.06); margin-bottom: 25px; border-top: 5px solid #4caf50; }
.section-title { color: #1b5e20; font-size: clamp(18px, 4vw, 22px); font-weight: bold; margin-bottom: 15px; border-bottom: 2px dashed #c8e6c9; padding-bottom: 10px; }

div.stButton > button:first-child { background: linear-gradient(90deg, #43a047, #2e7d32); color: white; border-radius: 50px; font-size: clamp(16px, 4vw, 20px); font-weight: bold; padding: 12px 20px; border: none; box-shadow: 0 6px 15px rgba(46, 125, 50, 0.4); transition: 0.3s; width: 100%; }
div.stButton > button:first-child:hover { transform: scale(1.02); }

.report-greeting { font-size: clamp(20px, 4.5vw, 24px); color: #e65100; font-weight: bold; text-align: center; margin-bottom: 15px; border-bottom: 2px solid #ffe0b2; padding-bottom: 10px; }

.action-container { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 25px; }
.action-btn { padding: 12px 15px; border-radius: 12px; text-decoration: none !important; font-weight: bold; font-size: clamp(14px, 3vw, 16px); flex: 1 1 180px; text-align: center; color: white !important; box-shadow: 0 4px 10px rgba(0,0,0,0.15); transition: 0.3s; }
.action-btn:hover { transform: translateY(-3px); }
.btn-wa { background: linear-gradient(135deg, #25D366, #128C7E); }
.btn-yt { background: linear-gradient(135deg, #FF0000, #cc0000); }
.btn-map { background: linear-gradient(135deg, #4285F4, #0d47a1); }
.btn-call { background: linear-gradient(135deg, #9C27B0, #6A1B9A); }
.btn-pm { background: linear-gradient(135deg, #f39c12, #d35400); }

audio { width: 100%; border-radius: 10px; margin-bottom: 15px; }

.scanner-container { position: relative; display: inline-block; overflow: hidden; width: 100%; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 3px solid #4caf50; }
.scanner-img { width: 100%; display: block; border-radius: 15px; }
.scanner-line { position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: #39ff14; box-shadow: 0 0 10px #39ff14, 0 0 20px #39ff14, 0 0 30px #39ff14; animation: scan 1.5s infinite linear; }
@keyframes scan { 0% { top: 0%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 100%; opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("""
<div class="app-header">
    <h1>🛡️ AI કૃષિ કવચ</h1>
    <p>પાક, પ્રકૃતિ અને પૈસાનો રક્ષક</p>
</div>
""", unsafe_allow_html=True)

# --- વિજ્ઞાન મેળાની વિગતો (તમારો નવો સુધારો: સ્થળ, તારીખ અને નામ) ---
st.markdown("""
<div class="info-card">
    <div class="info-title">શ્રી ચિત્રાસર પ્રાથમિક શાળા</div>
    <div class="info-text">મુ. ચિત્રાસર, તા. ખેડા, જી. ખેડા</div>
    <div class="info-highlight">નવાગામ ક્લસ્ટર કક્ષાનું વિજ્ઞાન, ગણિત અને પર્યાવરણ પ્રદર્શન : ૨૦૨૬-૨૭</div>
    <div class="info-date-venue">📍 સ્થળ: ચલીન્દ્રા પ્રાથમિક શાળા &nbsp;|&nbsp; 📅 તારીખ: ૦૯/૧૦/૨૦૨૬</div>
    <hr style='border: 1px dashed #e0e0e0; margin: 15px 0;'>
    <div class="info-text"><b>મુખ્ય વિષય:</b> ટકાઉ અને વિકસિત ભારત માટે વિજ્ઞાન, ટેકનોલોજી અને ઈનોવેશન</div>
    <div class="info-text" style="margin-bottom: 15px;"><b>વિભાગ:</b> 1. (A) બહેતર જીવન માટે આર્ટિફિશિયલ ઇન્ટેલિજન્સ (AI)</div>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: left; background: #f9fbe7; padding: 15px; border-radius: 10px;">
        <div style="margin-bottom: 10px;"><b>👨‍🎓 બાળ વૈજ્ઞાનિકો:</b><br>૧. મેઘાબેન દશરથભાઈ સોઢાપરમાર<br>૨. ડિમ્પલબેન કાનજીભાઈ ઠાકોર</div>
        <div><b>👨‍🏫 માર્ગદર્શક શિક્ષક:</b><br>ચેયુષભાઈ એન પટેલ</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- મલ્ટીપલ API Key સેટઅપ (સ્માર્ટ રોટેશન સિસ્ટમ) ---
try:
    if "GEMINI_API_KEYS" in st.secrets:
        api_keys_list = [k.strip() for k in st.secrets["GEMINI_API_KEYS"].split(",") if k.strip()]
    elif "GEMINI_API_KEY" in st.secrets:
        api_keys_list = [st.secrets["GEMINI_API_KEY"]]
    else:
        api_keys_list = []
        
    if not api_keys_list:
        st.error("⚠️ API Key મળતી નથી! કૃપા કરીને સિક્યોરિટી સેટિંગમાં 'GEMINI_API_KEYS' ઉમેરો.")
        st.stop()
except Exception as e:
    st.error("⚠️ સિક્યોરિટી સેટિંગમાં ભૂલ છે! મહેરબાની કરીને API Key ચેક કરો.")
    st.stop()

# --- ઓટોમેટિક લાઈવ લોકેશન ---
if 'live_location' not in st.session_state:
    st.session_state.live_location = "અજ્ઞાત"
    try:
        ip_res = requests.get('http://ip-api.com/json/', timeout=3).json()
        if ip_res['status'] == 'success':
            st.session_state.live_location = ip_res.get('city', ip_res.get('regionName', 'અજ્ઞાત'))
    except:
        pass

# --- સેટિંગ્સ ---
st.markdown("<div class='custom-card'><div class='section-title'>⚙️ સેટિંગ્સ અને માહિતી</div>", unsafe_allow_html=True)
st.success(f"📍 તમારું ઓટોમેટિક લાઈવ લોકેશન: **{st.session_state.live_location}**")
languages = {"ગુજરાતી (Gujarati)": "gu", "हिंदी (Hindi)": "hi", "मराठी (Marathi)": "mr", "English": "en"}
selected_lang = st.selectbox("તમારી ભાષા પસંદ કરો:", list(languages.keys()), label_visibility="collapsed")
target_lang_code = languages[selected_lang]
target_lang_name = selected_lang.split(' ')[0]
voice_enabled = st.toggle("🔊 ઓડિયો રિપોર્ટ (બોલીને સંભળાવો)", value=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- ફોટો અપલોડ (મલ્ટીપલ ફોટો સિસ્ટમ) ---
st.markdown("<div class='custom-card'><div class='section-title'>📸 પાકનો ફોટો પાડો (1 થી વધુ ફોટા આપી શકો છો)</div>", unsafe_allow_html=True)
st.info("💡 શ્રેષ્ઠ નિદાન માટે: (૧) બીમાર પાંદડાનો નજીકથી અને (૨) આખા છોડનો ફોટો એમ ૨-૩ ફોટા એકસાથે પાડો અથવા ગેલેરીમાંથી પસંદ કરો.")
uploaded_files = st.file_uploader("અહીં ક્લિક કરી ફોટો પાડો", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# --- પ્રોસેસિંગ ---
if uploaded_files:
    image_preview = st.empty()
    with image_preview.container():
        st.markdown(f"<div class='custom-card'><div class='section-title'>🖼 પસંદ કરેલા ફોટા ({len(uploaded_files)})</div>", unsafe_allow_html=True)
        cols = st.columns(len(uploaded_files))
        for idx, file in enumerate(uploaded_files):
            cols[idx].image(file, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚀 વિશ્લેષણ કરો (રોગ, માપ અને હવામાન)"):
        image_preview.empty()
        scanner_placeholder = st.empty()
        
        first_file = uploaded_files[0]
        base64_img = base64.b64encode(first_file.getvalue()).decode('utf-8')
        mime_type = "image/jpeg" if first_file.name.endswith(('jpg', 'jpeg')) else "image/png"
        
        scanner_html = f"""
        <div class='custom-card' style='text-align:center;'>
            <div class='section-title'>🔍 AI સ્કેન કરી રહ્યું છે...</div>
            <div class="scanner-container" style="max-width: 400px; margin: 0 auto;">
                <img src="data:{mime_type};base64,{base64_img}" class="scanner-img" />
                <div class="scanner-line"></div>
            </div>
            <p style='color:#1b5e20; margin-top:10px;'><b>{len(uploaded_files)} ફોટાઓનું</b> વિશ્લેષણ થઈ રહ્યું છે...</p>
        </div>
        """
        scanner_placeholder.markdown(scanner_html, unsafe_allow_html=True)

        weather_details = "લોકેશનની ચોક્કસ માહિતી ન હોવાથી હવામાન ડેટા ઉપલબ્ધ નથી."
        
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

        smart_prompt = f"""
        Analyze ALL provided crop images together. Provide response STRICTLY in {target_lang_name} language. 
        IMPORTANT FORMATTING RULES: 
        1. Use proper Markdown Headings (###) for each section.
        2. Leave a DOUBLE NEWLINE (\\n\\n) after every single section.
        
        ### ૧. 🌾 પાક અને રોગનું નામ: 
        (Provide accurate crop and disease name by analyzing all provided photos)
        
        ### ૨. 📊 રોગની અસર (Severity %): 
        (Provide percentage. If damage is >= 80%, strongly advise the farmer to apply for 'Pradhan Mantri Fasal Bima Yojana' for compensation).
        
        ### ૩. 🌦️ હવામાન રિપોર્ટ અને દવાની સલાહ ({st.session_state.live_location}):
        (YOU MUST EXACTLY COPY THIS TEXT: {weather_details})
        
        ### ૪. 🌿 પ્રાકૃતિક / ઓર્ગેનિક ઉપાય (પ્રથમ પસંદગી):
        (GIVE HIGHEST PRIORITY. Suggest 2-3 organic methods. CLEARLY specify exact mixing ratio for a 15-liter pump).
        
        ### ૫. 🧪 રાસાયણિક ઉપાય (વૈકલ્પિક):
        (Provide chemical alternative ONLY as a backup. Specify exact 15-liter pump dosage. Add a warning about soil damage).
        
        ### ૬. 🧮 પંપ અને દવાની ગણતરી: 
        (૧ વીઘા = ૨૪ ગુંઠા માટે અંદાજે ૩ પંપ (15 Liters each) વાપરવા. ખેડૂતને ગણતરી સમજાવો).
        
        ### ૭. 📞 નિષ્ણાતની સલાહ:
        જો વધુ માહિતી જોઈતી હોય તો ખેડૂત હેલ્પલાઇન (કિસાન કોલ સેન્ટર) નંબર 1551 પર કૉલ કરી શકો છો.
        
        [YT_SEARCH: Keyword1, Keyword2] (Provide 1 or 2 organic method names you just suggested, comma separated)
        """

        contents_parts = [{"text": smart_prompt}]
        
        # લૂપ દ્વારા બધા જ (૧, ૨ કે ૩) ફોટા AI ને મોકલવામાં આવશે
        for file in uploaded_files:
            base64_image = base64.b64encode(file.getvalue()).decode('utf-8')
            mime_type = "image/jpeg" if file.name.endswith(('jpg', 'jpeg')) else "image/png"
            contents_parts.append({"inlineData": {"mimeType": mime_type, "data": base64_image}})

        data = {"contents": [{"parts": contents_parts}]}
        headers = {'Content-Type': 'application/json'}
        
        success = False
        error_msg = ""
        
        # 🟢 મલ્ટીપલ API Key લૂપ (જે મોડેલ વ્યવસ્થિત ચાલે છે: gemini-3.8-flash)
        for current_key in api_keys_list:
            if success:
                break
                
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={current_key}"
            
            for attempt in range(2):
                try:
                    response = requests.post(url, headers=headers, json=data)
                    if response.status_code == 200:
                        success = True
                        break
                    elif response.status_code == 429:
                        error_msg = "પહેલી API Key ની લિમિટ પૂરી, બીજી કી પર સ્વિચ કરી રહ્યું છે..."
                        break
                    else:
                        error_msg = response.json().get('error', {}).get('message', 'Unknown Error')
                        time.sleep(1.5)
                except Exception as e:
                    error_msg = str(e)
                    time.sleep(1.5)
        
        if success:
            text_response = response.json()['candidates'][0]['content']['parts'][0]['text']
            scanner_placeholder.empty()
            
            yt_keywords = []
            yt_match = re.search(r'\[YT_SEARCH:\s*(.*?)\]', text_response)
            if yt_match:
                yt_keywords = [kw.strip() for kw in yt_match.group(1).split(',') if kw.strip()]
                text_response = re.sub(r'\[YT_SEARCH:\s*.*?\]', '', text_response).strip()
            
            clean_text_for_sharing = re.sub(r'<[^>]+>', '', text_response).strip()
            whatsapp_msg = f"🛡️ *AI કૃષિ કવચ - સ્માર્ટ રિપોર્ટ ({st.session_state.live_location})* 🛡️\n\n{clean_text_for_sharing}\n\nસૌજન્ય: ચિત્રાસર પ્રાથમિક શાળા પ્રોજેક્ટ"
            
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            
            if voice_enabled:
                audio_clean_text = re.sub(r'[*#_🚨💡🌿🧪🌾📊🌦️🧮📞]', ' ', clean_text_for_sharing)
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
            
            st.markdown("<div class='report-greeting'>✅ તમારો સ્માર્ટ રિપોર્ટ તૈયાર છે:</div>", unsafe_allow_html=True)
            st.markdown(text_response)
            
            # 🌟 સ્માર્ટ ડેશબોર્ડ (તમામ રંગીન બટન સાથે) 🌟
            st.markdown("---")
            st.markdown("<h4 style='text-align: center; color: #1b5e20;'>🛠️ ખેડૂત હેલ્પલાઇન અને એક્શન ડેશબોર્ડ</h4>", unsafe_allow_html=True)
            
            html_buttons = '<div class="action-container">'
            
            encoded_msg = urllib.parse.quote(whatsapp_msg)
            html_buttons += f'<a href="https://api.whatsapp.com/send?text={encoded_msg}" target="_blank" class="action-btn btn-wa">💬 WhatsApp માં રિપોર્ટ મોકલો</a>'
            
            for kw in yt_keywords:
                yt_query = urllib.parse.quote(f"{kw} banavvani rit")
                html_buttons += f'<a href="https://www.youtube.com/results?search_query={yt_query}" target="_blank" class="action-btn btn-yt">📺 {kw} બનાવતા શીખો (વિડીયો)</a>'
            
            maps_url = "https://www.google.com/maps/search/Agro+center+near+me"
            html_buttons += f'<a href="{maps_url}" target="_blank" class="action-btn btn-map">📍 નજીકનો એગ્રો સ્ટોર શોધો</a>'
            
            html_buttons += f'<a href="tel:1551" class="action-btn btn-call">📞 શું કોલ કરવો છે? 1551 ડાયલ કરો</a>'
            html_buttons += f'<a href="https://pmfby.gov.in/" target="_blank" class="action-btn btn-pm">🌾 પાક વીમા યોજના (PMFBY)</a>'
            
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
            scanner_placeholder.empty()
            st.error(f"⚠️ ગૂગલ સર્વર એરર: {error_msg}")
            st.info("કૃપા કરીને 30 સેકન્ડ પછી ફરીથી સ્કેન કરો. (અથવા નવી API Key નાખો).")
