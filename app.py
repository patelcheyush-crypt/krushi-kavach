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
.app-header { background: linear-gradient(135deg, #1b5e20, #2e7d32); padding: 20px; border-radius: 0 0 25px 25px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(27, 94, 32, 0.4); margin-top: -60px; margin-bottom: 20px; }
.app-header h1 { font-size: clamp(26px, 6vw, 36px); font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); color: white;}
.app-header p { font-size: clamp(14px, 3vw, 16px); margin: 5px 0 0 0; opacity: 0.9; }
.info-card { background: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); margin-bottom: 25px; border-top: 5px solid #ff9800; text-align: center; }
.info-title { color: #1b5e20; font-size: clamp(20px, 4vw, 24px); font-weight: 900; margin-bottom: 5px; }
.info-text { font-size: clamp(14px, 3vw, 16px); color: #424242; margin-bottom: 5px; line-height: 1.5; }
.info-date-venue { color: #d32f2f; font-weight: 900; font-size: clamp(15px, 3vw, 17px); margin-bottom: 10px; background-color: #ffebee; padding: 5px; border-radius: 8px; display: inline-block; }
.custom-card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.06); margin-bottom: 25px; border-top: 5px solid #4caf50; }
.section-title { color: #1b5e20; font-size: clamp(18px, 4vw, 22px); font-weight: bold; margin-bottom: 15px; border-bottom: 2px dashed #c8e6c9; padding-bottom: 10px; }
div.stButton > button:first-child { background: linear-gradient(90deg, #43a047, #2e7d32); color: white; border-radius: 50px; font-size: clamp(16px, 4vw, 20px); font-weight: bold; padding: 12px 20px; border: none; box-shadow: 0 6px 15px rgba(46, 125, 50, 0.4); transition: 0.3s; width: 100%; }
div.stButton > button:first-child:hover { transform: scale(1.02); }
.report-greeting { font-size: clamp(20px, 4.5vw, 24px); color: #e65100; font-weight: bold; text-align: center; margin-bottom: 15px; border-bottom: 2px solid #ffe0b2; padding-bottom: 10px; }
.action-container { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 25px; }
.action-btn { padding: 12px 15px; border-radius: 12px; text-decoration: none !important; font-weight: bold; font-size: clamp(14px, 3vw, 16px); flex: 1 1 180px; text-align: center; color: white !important; box-shadow: 0 4px 10px rgba(0,0,0,0.15); transition: 0.3s; }
.btn-wa { background: linear-gradient(135deg, #25D366, #128C7E); }
.btn-yt { background: linear-gradient(135deg, #FF0000, #cc0000); }
.btn-map { background: linear-gradient(135deg, #4285F4, #0d47a1); }
.btn-call { background: linear-gradient(135deg, #9C27B0, #6A1B9A); }
.btn-pm { background: linear-gradient(135deg, #f39c12, #d35400); }
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

# --- વિજ્ઞાન મેળાની વિગતો ---
st.markdown("""
<div class="info-card">
    <div class="info-title">શ્રી ચિત્રાસર પ્રાથમિક શાળા</div>
    <div class="info-text">મુ. ચિત્રાસર, તા. ખેડા, જી. ખેડા</div>
    <div class="info-highlight">નવાગામ ક્લસ્ટર કક્ષાનું વિજ્ઞાન, ગણિત અને પર્યાવરણ પ્રદર્શન : ૨૦૨૬-૨૭</div>
    <div class="info-date-venue">📍 સ્થળ: ચલીન્દ્રા પ્રાથમિક શાળા &nbsp;|&nbsp; 📅 તારીખ: ૦૯/૧૦/૨૦૨૬</div>
    <hr style='border: 1px dashed #e0e0e0; margin: 15px 0;'>
    <div class="info-text"><b>મુખ્ય વિષય:</b> ટકાઉ અને વિકસિત ભારત માટે વિજ્ઞાન, ટેકનોલોજી અને ઈનોવેશન</div>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: left; background: #f9fbe7; padding: 15px; border-radius: 10px; margin-top:15px;">
        <div style="margin-bottom: 10px;"><b>👨‍🎓 બાળ વૈજ્ઞાનિકો:</b><br>૧. મેઘાબેન દશરથભાઈ સોઢાપરમાર<br>૨. ડિમ્પલબેન કાનજીભાઈ ઠાકોર</div>
        <div><b>👨‍🏫 માર્ગદર્શક શિક્ષક:</b><br>ચેયુષભાઈ એન પટેલ</div>
    </div>
</div>
""", unsafe_allow_html=True)

try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    st.error("⚠️ API Key મળતી નથી! કૃપા કરીને Streamlit ના સિક્યોરિટી સેટિંગમાં 'OPENAI_API_KEY' ઉમેરો.")
    st.stop()

# 🌟 ઓટોમેટિક લોકેશન સિસ્ટમ 🌟
def get_auto_location():
    try:
        res = requests.get('https://ipapi.co/json/', timeout=3).json()
        if 'city' in res and res['city']:
            return f"{res['city']}, {res['region']}"
    except:
        pass
    try:
        res = requests.get('http://ip-api.com/json/', timeout=3).json()
        if res.get('status') == 'success':
            return f"{res.get('city')}, {res.get('regionName')}"
    except:
        pass
    return "Bhavnagar, Gujarat"

if 'live_location' not in st.session_state:
    st.session_state.live_location = get_auto_location()

# 🌟 ભાષા પસંદગી 🌟
languages = {
    "ગુજરાતી (Gujarati)": "gu", "हिंदी (Hindi)": "hi", "मराठी (Marathi)": "mr", "বাংলা (Bengali)": "bn",
    "తెలుగు (Telugu)": "te", "தமிழ் (Tamil)": "ta", "ಕನ್ನಡ (Kannada)": "kn", "ଓଡ଼ିଆ (Odia)": "or",
    "മലയാളം (Malayalam)": "ml", "ਪੰਜਾਬੀ (Punjabi)": "pa", "English": "en"
}
selected_lang = st.selectbox("તમારી ભાષા પસંદ કરો (Select Language):", list(languages.keys()), label_visibility="collapsed")
target_lang_code = languages[selected_lang]
target_lang_name = selected_lang.split(' ')[0]

ui_dict = {
    "gu": {"loc": "📍 લાઈવ લોકેશન:", "photo": "📸 પાક/છોડનો ફોટો પાડો", "help": "💡 શ્રેષ્ઠ નિદાન માટે: બીમાર પાંદડાનો અને આખા છોડનો એમ ૨-૩ ફોટા પાડો.", "btn_up": "અહીં ક્લિક કરી ફોટો પાડો", "btn_scan": "🚀 વિશ્લેષણ કરો", "scan_msg": "🔍 AI સ્કેન કરી રહ્યું છે...", "dash": "🛠️ ખેડૂત/ગાર્ડન હેલ્પલાઇન ડેશબોર્ડ", "wa": "💬 WhatsApp માં શેર કરો", "agro": "📍 નજીકનો એગ્રો/નર્સરી સ્ટોર", "call": "📞 કિસાન કોલ સેન્ટર", "pm": "🌾 પાક વીમા યોજના", "dl": "📄 રિપોર્ટ સેવ કરો", "audio": "🔊 ઓડિયો રિપોર્ટ સાંભળો", "visitors": "👁️ કુલ મુલાકાતીઓ:"},
    "hi": {"loc": "📍 लाइव लोकेशन:", "photo": "📸 फसल/पौधे की फोटो लें", "help": "💡 सर्वोत्तम निदान के लिए: बीमार पत्ते और पूरे पौधे की 2-3 फोटो लें।", "btn_up": "फोटो अपलोड करने के लिए क्लिक करें", "btn_scan": "🚀 विश्लेषण करें", "scan_msg": "🔍 AI स्कैन कर रहा है...", "dash": "🛠️ हेल्पलाइन डैशबोर्ड", "wa": "💬 WhatsApp पर शेयर करें", "agro": "📍 नजदीकी एग्रो/नर्सरी स्टोर", "call": "📞 किसान कॉल सेंटर", "pm": "🌾 फसल बीमा योजना", "dl": "📄 रिपोर्ट सेव करें", "audio": "🔊 ऑडियो रिपोर्ट सुनें", "visitors": "👁️ कुल विज़िटर:"},
    "en": {"loc": "📍 Live Location:", "photo": "📸 Take Crop/Plant Photo", "help": "💡 For best diagnosis: Take 2-3 photos including a close-up and full plant.", "btn_up": "Click here to upload photo", "btn_scan": "🚀 Analyze Plant", "scan_msg": "🔍 AI is scanning...", "dash": "🛠️ Action Dashboard", "wa": "💬 Share on WhatsApp", "agro": "📍 Find Agro/Nursery Store", "call": "📞 Kisan Call Center", "pm": "🌾 Crop Insurance (PMFBY)", "dl": "📄 Save Report", "audio": "🔊 Enable Audio Report", "visitors": "👁️ Total Visitors:"}
}
ui = ui_dict.get(target_lang_code, ui_dict["en"])

st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

# 🌟 ઓટોમેટિક લોકેશન દર્શાવશે 🌟
st.success(f"{ui['loc']} **{st.session_state.live_location}**")
voice_enabled = st.toggle(ui['audio'], value=True)

# 🌟 લાઈવ વિઝિટર કાઉન્ટર 🌟
st.markdown(f"""
<div style='margin-top: 15px; padding-top: 15px; border-top: 1px dashed #c8e6c9; text-align: center;'>
    <span style='font-weight: bold; color: #1b5e20; margin-right: 10px;'>{ui['visitors']}</span>
    <img src="https://api.visitorbadge.io/api/visitors?path=ai_krushi_kavach_project_2026&countColor=%232e7d32" alt="Visitor Count" style="vertical-align: middle;">
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- ફોટો અપલોડ ---
st.markdown(f"<div class='custom-card'><div class='section-title'>{ui['photo']}</div>", unsafe_allow_html=True)
st.info(ui['help'])
uploaded_files = st.file_uploader(ui['btn_up'], type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# --- પ્રોસેસિંગ (ChatGPT GPT-4o-Mini) ---
if uploaded_files:
    image_preview = st.empty()
    with image_preview.container():
        st.markdown(f"<div class='custom-card'><div class='section-title'>🖼 ({len(uploaded_files)})</div>", unsafe_allow_html=True)
        cols = st.columns(len(uploaded_files))
        for idx, file in enumerate(uploaded_files):
            cols[idx].image(file, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button(ui['btn_scan']):
        image_preview.empty()
        scanner_placeholder = st.empty()
        
        first_file = uploaded_files[0]
        base64_img_preview = base64.b64encode(first_file.getvalue()).decode('utf-8')
        mime_type_preview = "image/jpeg" if first_file.name.endswith(('jpg', 'jpeg')) else "image/png"
        
        scanner_html = f"""
        <div class='custom-card' style='text-align:center;'>
            <div class='section-title'>{ui['scan_msg']}</div>
            <div class="scanner-container" style="max-width: 400px; margin: 0 auto;">
                <img src="data:{mime_type_preview};base64,{base64_img_preview}" class="scanner-img" />
                <div class="scanner-line"></div>
            </div>
        </div>
        """
        scanner_placeholder.markdown(scanner_html, unsafe_allow_html=True)

        weather_details = "લોકેશનની ચોક્કસ માહિતી ઉપલબ્ધ નથી."
        if st.session_state.live_location:
            try:
                geo_res = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={st.session_state.live_location}&count=1", timeout=5).json()
                if "results" in geo_res and len(geo_res["results"]) > 0:
                    lat, lon = geo_res["results"][0]["latitude"], geo_res["results"][0]["longitude"]
                    w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_probability_max&timezone=auto&forecast_days=3", timeout=5).json()
                    
                    today = w_res["daily"]["precipitation_probability_max"][0]
                    tomorrow = w_res["daily"]["precipitation_probability_max"][1]
                    day_after = w_res["daily"]["precipitation_probability_max"][2]
                    
                    max_rain = max(today, tomorrow, day_after)
                    weather_details = f"આજે વરસાદની શક્યતા {today}% છે. 3 દિવસમાં વધુમાં વધુ વરસાદની શક્યતા {max_rain}% છે."
            except:
                pass

        # 🌟 નવો માસ્ટર પ્રોમ્પ્ટ: કાગળના ફોટા માટે AI ને કડક સૂચના (Demo Bypass) 🌟
        smart_prompt = f"""
        CRITICAL INSTRUCTION: You are an Expert Agriculture Scientist participating in a School Science Fair Demonstration. 
        IMPORTANT: The user might upload images of PRINTED PHOTOS ON PAPER, drawings, or pictures on a computer/mobile screen to demonstrate plant diseases. YOU MUST NOT REFUSE TO ANSWER. DO NOT say "I cannot assist with that". Treat any image of a plant/leaf (even if it's on paper or screen) as a REAL plant and analyze the disease shown in the photo completely.

        Analyze ALL provided images together. Determine if it is a 'Farm Crop' or 'Home/Garden Plant'.
        Provide response STRICTLY and HIGHLY DETAILED in {target_lang_name} language. 
        Make the analysis highly structured, descriptive, and exactly like an expert's detailed report. Do NOT give short answers.
        
        FORMATTING: Use proper Markdown Headings (###).
        
        ### ૧. પાક/છોડ અને રોગની સંપૂર્ણ ઓળખ: 
        (Provide accurate name. Detail the exact symptoms you see. Explain thoroughly).
        
        ### ૨. રોગની અસર અને નુકસાની (Severity %): 
        (Provide percentage. If Farm Crop >= 80%, advise PMFBY. Tell them how bad the situation is).
        
        ### ૩. હવામાન અને છંટકાવની સલાહ ({st.session_state.live_location}):
        ({weather_details}. Based on this, explain clearly when is the exact best time to spray).
        
        ### ૪. પ્રાકૃતિક/ઓર્ગેનિક ઉપાય (સ્ટેપ-બાય-સ્ટેપ રીત):
        (Give 2 detailed natural remedies. Explain EXACTLY how to make it, ingredients needed, and how to mix it. Give highly detailed guidance. Farm: 15-liter pump ratio. Garden: 1-Liter bottle).
        
        ### ૫. રાસાયણિક દવા (વૈકલ્પિક - ચોક્કસ નામ સાથે):
        (Provide specific chemical formulation/medicine name and detailed exact dosage).
        
        ### ૬. દવાની ગણતરી અને સાવચેતી: 
        (Farm: 3 pumps per 1 Bigha / 24 Guntha. Explain safety precautions thoroughly).
        
        [YT_SEARCH: Keyword1, Keyword2]
        """

        contents_parts = [{"type": "text", "text": smart_prompt}]
        for file in uploaded_files:
            b64_img = base64.b64encode(file.getvalue()).decode('utf-8')
            m_type = "image/jpeg" if file.name.endswith(('jpg', 'jpeg')) else "image/png"
            contents_parts.append({
                "type": "image_url",
                "image_url": {"url": f"data:{m_type};base64,{b64_img}"}
            })

        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": contents_parts}],
            "max_tokens": 2000,
            "temperature": 0.4
        }
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
        url = "https://api.openai.com/v1/chat/completions"
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                text_response = response.json()['choices'][0]['message']['content']
                scanner_placeholder.empty()
                
                yt_keywords = []
                yt_match = re.search(r'\[YT_SEARCH:\s*(.*?)\]', text_response)
                if yt_match:
                    yt_keywords = [kw.strip() for kw in yt_match.group(1).split(',') if kw.strip()]
                    text_response = re.sub(r'\[YT_SEARCH:\s*.*?\]', '', text_response).strip()
                
                clean_text_for_sharing = re.sub(r'<[^>]+>', '', text_response).strip()
                whatsapp_msg = f"🛡️ AI કૃષિ કવચ - સ્માર્ટ રિપોર્ટ ({st.session_state.live_location}) 🛡️\n\n{clean_text_for_sharing}\n\nસૌજન્ય: ચિત્રાસર પ્રાથમિક શાળા પ્રોજેક્ટ"
                
                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                
                # 🌟 ઓડિયો માટે અદ્યતન ક્લીનિંગ (માત્ર ચોખ્ખું લખાણ વંચાશે) 🌟
                if voice_enabled:
                    audio_clean_text = clean_text_for_sharing
                    for char in ['*', '#', '_', '-', '🚨', '💡', '🌿', '🧪', '🌾', '📊', '🌦️', '🧮', '📞', '📍', '💬', '📺', '[', ']']:
                        audio_clean_text = audio_clean_text.replace(char, '')
                    
                    try:
                        tts = gTTS(text=f"નમસ્કાર ખેડૂત મિત્ર. તમારો રિપોર્ટ આ મુજબ છે. {audio_clean_text}", lang=target_lang_code)
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)
                        audio_b64 = base64.b64encode(fp.read()).decode()
                        st.markdown(f'''<audio autoplay controls><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>''', unsafe_allow_html=True)
                    except:
                        pass
                
                st.markdown(text_response)
                
                st.markdown("---")
                st.markdown(f"<h4 style='text-align: center; color: #1b5e20;'>{ui['dash']}</h4>", unsafe_allow_html=True)
                
                html_buttons = '<div class="action-container">'
                encoded_msg = urllib.parse.quote(whatsapp_msg)
                html_buttons += f'<a href="https://api.whatsapp.com/send?text={encoded_msg}" target="_blank" class="action-btn btn-wa">{ui["wa"]}</a>'
                
                for kw in yt_keywords:
                    yt_query = urllib.parse.quote(f"{kw} organic remedy")
                    html_buttons += f'<a href="https://www.youtube.com/results?search_query={yt_query}" target="_blank" class="action-btn btn-yt">📺 {kw} (YouTube)</a>'
                
                maps_url = "https://www.google.com/maps/search/Agro+center+near+me"
                html_buttons += f'<a href="{maps_url}" target="_blank" class="action-btn btn-map">{ui["agro"]}</a>'
                html_buttons += f'<a href="tel:1551" class="action-btn btn-call">{ui["call"]}</a>'
                html_buttons += f'<a href="https://pmfby.gov.in/" target="_blank" class="action-btn btn-pm">{ui["pm"]}</a>'
                html_buttons += '</div>'
                
                st.markdown(html_buttons, unsafe_allow_html=True)
                
                st.write("") 
                st.download_button(
                    label=ui["dl"],
                    data=whatsapp_msg,
                    file_name="Crop_Shield_Report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                st.markdown("
