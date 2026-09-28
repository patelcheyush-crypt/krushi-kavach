import streamlit as st
import requests
import base64
from gtts import gTTS
import io
import urllib.parse
import re
import time

# પેજ સેટિંગ (મોબાઈલ અને ડેસ્કટોપ બંને માટે ઓપ્ટિમાઈઝ્ડ)
st.set_page_config(page_title="AI કૃષિ કવચ | સાયન્સ ફેર 2026-27", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# મુખ્ય ડિઝાઇન (Responsive CSS)
st.markdown("""
<style>
/* મોબાઈલ અને પીસી બંને માટે રિસ્પોન્સિવ લેઆઉટ */
.stApp { background-color: #f0fdf4; }

.school-box { background-color: #ffffff; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; border-top: 5px solid #166534; margin-bottom: 15px; }
.school-name { font-size: clamp(24px, 4vw, 32px); color: #166534; font-weight: 900; margin: 0; }
.location { font-size: clamp(16px, 3vw, 20px); color: #4b5563; font-weight: 700; margin-top: 5px; }

.event-box { background-color: #dcfce7; padding: 12px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; border: 2px solid #bbf7d0; margin-bottom: 15px; }
.event-text { font-size: clamp(16px, 3vw, 20px); color: #15803d; font-weight: 800; margin: 0; }

.theme-box { background-color: #ecfdf5; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; border: 2px solid #34d399; margin-bottom: 15px; }
.theme-title { font-size: 18px; color: #047857; font-weight: bold; margin-bottom: 5px; }
.theme-text { font-size: clamp(15px, 2.5vw, 17px); color: #1f2937; font-weight: 800; line-height: 1.4; }
.theme-subtext { font-size: 14px; color: #4b5563; font-weight: 600; }

.project-box { background: linear-gradient(135deg, #16a085, #27ae60); padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 6px 12px rgba(0,0,0,0.15); margin-bottom: 25px; }
.project-title { font-size: clamp(24px, 4vw, 30px); color: #ffffff; font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }

.result-box { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 8px solid #27ae60; box-shadow: 0 6px 12px rgba(0,0,0,0.1); font-size: clamp(16px, 3vw, 18px); line-height: 1.8; color: #1f2937; margin-top:20px; overflow-x: auto; }

/* સ્કેનર એનિમેશન - મોબાઈલ સ્ક્રીન મુજબ સેટ */
.scanner-container { position: relative; display: inline-block; border: 3px solid #27ae60; border-radius: 10px; overflow: hidden; width: 100%; max-width: 600px; box-shadow: 0 0 15px rgba(39, 174, 96, 0.5); margin: 0 auto; display: block; }
.scanner-img { width: 100%; display: block; }
.scanner-line { position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: #39ff14; box-shadow: 0 0 10px #39ff14, 0 0 20px #39ff14, 0 0 30px #39ff14; animation: scan 2s infinite linear; }
@keyframes scan { 0% { top: 0%; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 100%; opacity: 0; } }

.blinking-warning { animation: alert-blink 1s infinite; padding: 15px; border-radius: 10px; font-size: clamp(18px, 3.5vw, 22px); font-weight: 900; text-align: center; margin: 20px 0; box-shadow: 0 4px 15px rgba(255, 0, 0, 0.5); border: 3px solid #ff0000; }
@keyframes alert-blink { 0% { background-color: #ffffff; color: #ff0000; } 50% { background-color: #ff0000; color: #ffffff; } 100% { background-color: #ffffff; color: #ff0000; } }

.location-box { background-color: #e3f2fd; padding: 15px; border-radius: 12px; border: 2px solid #90caf9; margin-top:10px; margin-bottom:20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.weather-title { font-size: clamp(18px, 3.5vw, 22px); color: #1565c0; font-weight: bold; margin-bottom: 10px; }

/* રિસ્પોન્સિવ સ્માર્ટ બટન */
div.stButton > button:first-child { background: linear-gradient(90deg, #15803d, #16a34a); color: white; border-radius: 8px; font-size: clamp(16px, 3vw, 20px); font-weight: 900; padding: 15px 10px; border: none; box-shadow: 0 6px 15px rgba(22, 163, 74, 0.4); transition: 0.3s; width: 100%; white-space: normal; height: auto; }
div.stButton > button:first-child:hover { background: linear-gradient(90deg, #166534, #15803d); box-shadow: 0 8px 20px rgba(22, 101, 52, 0.6); transform: scale(1.02); }

/* મોબાઈલ ફ્રેન્ડલી એક્શન બટન્સ (YouTube, WhatsApp) */
.action-container { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 25px; }
.action-btn { padding: 12px 15px; border-radius: 8px; text-decoration: none !important; font-weight: bold; font-size: clamp(14px, 2.5vw, 16px); flex: 1 1 200px; text-align: center; color: white !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s; }
.action-btn:hover { opacity: 0.9; transform: translateY(-2px); }
.btn-wa { background-color: #25D366; border: 2px solid #128C7E; }
.btn-gw { background-color: #4285F4; border: 2px solid #0d47a1; }
.btn-map { background-color: #34A853; border: 2px solid #1b5e20; }
.btn-yt { background-color: #FF0000; border: 2px solid #b71c1c; }
.btn-pm { background-color: #f39c12; border: 2px solid #e67e22; }

/* મોબાઈલ માટે ઓડિયો પ્લેયર 100% પહોળાઈ સેટ */
audio { width: 100%; }
</style>
""", unsafe_allow_html=True)

# હેડર સેક્શન
st.markdown("""
<div class="school-box">
    <div class="school-name">🏫 ચિત્રાસર પ્રાથમિક શાળા</div>
    <div class="location">તાલુકો: ખેડા, જિલ્લો: ખેડા</div>
</div>

<div class="event-box">
    <div class="event-text">🔬 નવાગામ ક્લસ્ટર કક્ષાનું વિજ્ઞાન, ગણિત અને પર્યાવરણ પ્રદર્શન વર્ષ 2026-27 🔬</div>
</div>

<div class="theme-box">
    <div class="theme-title">મુખ્ય વિષય :</div>
    <div class="theme-text">ટકાઉ અને વિકસિત ભારત માટે વિજ્ઞાન, ટેકનોલોજી અને ઈનોવેશન</div>
    <hr style="margin: 10px 0; border-color: #a7f3d0;">
    <div class="theme-title">વિભાગ :</div>
    <div class="theme-text">1. (A) બહેતર જીવન માટે આર્ટિફિશિયલ ઇન્ટેલિજન્સ</div>
</div>

<div class="project-box">
    <div class="project-title">🛡️ કૃતિનું નામ : AI કૃષિ કવચ</div>
</div>
""", unsafe_allow_html=True)

# --- GitHub અને મોબાઈલ માટે 100% સુરક્ષિત API સિસ્ટમ ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("⚠️ API Key મળતી નથી! કૃપા કરીને Streamlit Settings -> Secrets માં 'GEMINI_API_KEY' નાખો.")
    st.stop()

# ભાષા પસંદગી
languages = {"ગુજરાતી (Gujarati)": "gu", "हिंदी (Hindi)": "hi", "मराठी (Marathi)": "mr", "English": "en"}
selected_lang = st.selectbox("🌍 રિપોર્ટની ભાષા પસંદ કરો (Language):", list(languages.keys()))
target_lang_code = languages[selected_lang]
target_lang_name = selected_lang.split(' ')[0]

st.markdown("""
<div style="background-color: #fff3cd; border-left: 6px solid #ffc107; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); font-size: clamp(14px, 2.5vw, 16px);">
💡 <b>ખેડૂત મિત્રો માટે સ્માર્ટ ટિપ (પૈસા બચાવો):</b><br>
જો એક જ ખેતરમાં અલગ-અલગ જગ્યાએ જુદા-જુદા રોગ દેખાતા હોય, તો આખા ખેતરમાં એકસરખી મોંઘી દવા છાંટવાની ભૂલ ન કરવી. અલગ-અલગ પાંદડાના ફોટા પાડીને વારાફરતી સ્કેન કરો. જ્યાં જેવો રોગ, ત્યાં તેવી જ દવા વાપરો અને ખોટો ખર્ચ બચાવો!
</div>
""", unsafe_allow_html=True)

# કેમેરા અને ગેલેરી (મોબાઈલમાં સીધો કેમેરા ખુલશે)
st.markdown("### 📸 ૧. પાકનો ફોટો આપો:")
tab1, tab2 = st.tabs(["📷 લાઈવ કેમેરાથી ફોટો પાડો", "📂 ગેલેરીમાંથી ફોટો પસંદ કરો"])

with tab1:
    camera_file = st.camera_input("તમારા મોબાઈલ કે લેપટોપનો કેમેરા ચાલુ કરો")
with tab2:
    gallery_file = st.file_uploader("અથવા ગેલેરીમાંથી જૂનો ફોટો અપલોડ કરો...", type=["jpg", "jpeg", "png"])

uploaded_file = camera_file if camera_file is not None else gallery_file

# લોકેશન ઇનપુટ (મોબાઈલ માટે ઓટો-સ્ટેકિંગ કોલમ્સ)
st.markdown("""
<div class='location-box'>
<div class='weather-title'>📍 ૨. તમારું લોકેશન પસંદ કરો (સ્માર્ટ હવામાન સલાહ માટે)</div>
""", unsafe_allow_html=True)

location_method = st.radio("", [
    "૧. 📍 ઑટોમેટિક મારું લાઈવ લોકેશન લો (સૌથી ફાસ્ટ)", 
    "૨. પિનકોડ દ્વારા", 
    "૩. લિસ્ટમાંથી પસંદ કરીને", 
    "૪. ⏭️ મારે હવામાનની માહિતી નથી જોઈતી"
])

search_query_for_weather = ""
display_location_name = ""

if location_method.startswith("૧"):
    try:
        ip_res = requests.get('http://ip-api.com/json/', timeout=5).json()
        if ip_res['status'] == 'success':
            auto_city = ip_res['city']
            search_query_for_weather = auto_city
            display_location_name = f"Live Location ({auto_city})"
            st.success(f"📍 તમારું લોકેશન પકડાઈ ગયું છે: {auto_city}")
        else:
            st.warning("લોકેશન મળ્યું નહિ, કૃપા કરીને પિનકોડ નો ઉપયોગ કરો.")
    except:
        st.warning("ઇન્ટરનેટ કનેક્શનના કારણે લોકેશન મળ્યું નહિ.")
        
elif location_method.startswith("૨"):
    pincode = st.text_input("તમારા ગામનો ૬ આંકડાનો પિનકોડ લખો:", placeholder="દા.ત. 387411")
    if pincode and len(pincode) == 6 and pincode.isdigit():
        try:
            pin_url = f"https://api.postalpincode.in/pincode/{pincode}"
            pin_res = requests.get(pin_url, timeout=5).json()
            if pin_res[0]['Status'] == 'Success':
                district_from_pin = pin_res[0]['PostOffice'][0]['District']
                search_query_for_weather = district_from_pin
                display_location_name = f"પિનકોડ {pincode} ({district_from_pin})"
            else:
                search_query_for_weather = pincode
                display_location_name = f"પિનકોડ {pincode}"
        except:
            search_query_for_weather = pincode
            display_location_name = f"પિનકોડ {pincode}"
elif location_method.startswith("૩"):
    # Streamlit નાની સ્ક્રીન પર આ કોલમ્સ જાતે જ એકની નીચે એક કરી દેશે
    col1, col2, col3 = st.columns(3)
    with col1:
        states = {"ગુજરાત (Gujarat)": "GJ", "महाराष्ट्र (Maharashtra)": "MH"}
        selected_state = st.selectbox("રાજ્ય (State):", list(states.keys()))
    with col2:
        if states[selected_state] == "GJ":
            districts = {"ખેડા": "Kheda", "ભાવનગર": "Bhavnagar", "રાજકોટ": "Rajkot", "અમદાવાદ": "Ahmedabad"}
        else:
            districts = {"पुणे": "Pune", "नाशिक": "Nashik", "जळगाव": "Jalgaon"}
        selected_district = st.selectbox("જિલ્લો (District):", list(districts.keys()))
    with col3:
        if districts[selected_district] == "Kheda":
            talukas = {"ખેડા": "Kheda", "નડિયાદ": "Nadiad", "કપડવંજ": "Kapadvanj", "ડાકોર": "Dakor"}
        elif districts[selected_district] == "Bhavnagar":
            talukas = {"પાલીતાણા": "Palitana", "ભાવનગર": "Bhavnagar", "ગારીયાધાર": "Gariadhar", "તળાજા": "Talaja"}
        else:
            talukas = {selected_district: districts[selected_district]} 
        selected_taluka = st.selectbox("તાલુકો (Taluka):", list(talukas.keys()))
    
    search_query_for_weather = districts[selected_district] 
    display_location_name = f"{selected_taluka} ({selected_district})"
else:
    search_query_for_weather = "SKIP"
    display_location_name = "લોકેશન આપેલ નથી"

st.markdown("</div>", unsafe_allow_html=True)

# ઓડિયો સેટિંગ (મોબાઈલ માટે)
st.markdown("<div style='background-color:#e8f5e9; padding:10px; border-radius:8px; border:1px solid #c8e6c9; margin-bottom:15px;'>", unsafe_allow_html=True)
voice_enabled = st.checkbox("🔊 રિઝલ્ટ બોલીને સંભળાવો (ઓડિયો ચાલુ રાખો)", value=True)
st.markdown("</div>", unsafe_allow_html=True)

run_ai = False
if uploaded_file is not None:
    base64_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    mime_type = "image/jpeg" if uploaded_file.name.endswith(('jpg', 'jpeg')) else "image/png"
    
    image_placeholder = st.empty()
    image_placeholder.image(uploaded_file, caption='તમે લીધેલો ફોટો', use_container_width=True)
    
    if st.button("🔍 એકસાથે સ્કેન કરો (રોગ, ઉપાય, સચોટ માપ અને હવામાન)"):
        run_ai = True

    if run_ai:
        # સ્કેનર એનિમેશન
        scanner_html = f"""<div class="scanner-container"><img src="data:{mime_type};base64,{base64_image}" class="scanner-img" /><div class="scanner-line"></div></div>"""
        image_placeholder.markdown(scanner_html, unsafe_allow_html=True)
        
        today_rain = tomorrow_rain = day_after_rain = 0
        weather_data_success = False
        
        # હવામાન API કોલ
        if search_query_for_weather != "SKIP" and search_query_for_weather != "":
            try:
                st.info(f"📡 સેટેલાઇટ પરથી '{display_location_name}' ના હવામાનની માહિતી લેવાઈ રહી છે...")
                geo_res = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={search_query_for_weather}&count=1", timeout=5).json()
                if "results" in geo_res and len(geo_res["results"]) > 0:
                    lat = geo_res["results"][0]["latitude"]
                    lon = geo_res["results"][0]["longitude"]
                    w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_probability_max&timezone=auto&forecast_days=3", timeout=5).json()
                    
                    today_rain = w_res["daily"]["precipitation_probability_max"][0]
                    tomorrow_rain = w_res["daily"]["precipitation_probability_max"][1]
                    day_after_rain = w_res["daily"]["precipitation_probability_max"][2]
                    weather_data_success = True
                else:
                    st.warning("⚠️ લોકેશન મળ્યું નહીં.")
            except:
                pass

        try:
            status_placeholder = st.empty()
            best_model = "gemini-3.8-flash"
                
            if weather_data_success:
                max_rain = max(today_rain, tomorrow_rain, day_after_rain)
                
                if max_rain < 50:
                    smart_advice = "હાલમાં વરસાદ પડવાની શક્યતા બહુ જ ઓછી છે. વાતાવરણ એકદમ અનુકૂળ છે, તેથી તમે નિઃસંકોચ દવાનો છંટકાવ કરી શકો છો અને તમારા પાકને ઝડપથી બચાવી શકો છો."
                else:
                    smart_advice = "⚠️ ચેતવણી: આગામી દિવસોમાં વરસાદની શક્યતા વધુ હોવાથી આજે દવા છાંટવાનો ખર્ચ કરતા નહિ. દવા ધોવાઈ જશે અને મહેનત પાણીમાં જશે! વાતાવરણ ચોખ્ખું થાય ત્યારે જ છંટકાવ કરવો."

                weather_instruction = f"""
                **૩. 🌦️ હવામાન ખાતાની આગાહી અને સલાહ ({display_location_name}):**
                - **વરસાદની શક્યતા:** આજે {today_rain}%, કાલે {tomorrow_rain}%, પરમદિવસે {day_after_rain}%.
                - **AI સલાહ:** {smart_advice}
                """
            else:
                weather_instruction = "**૩. 🌦️ હવામાન ખાતાની આગાહી:** \n- લોકેશન પસંદ ન હોવાથી હવામાનની માહિતી ઉપલબ્ધ નથી."
            
            # --- ઓટો-કેલ્ક્યુલેશન જનરેટિવ AI પ્રોમ્પ્ટ ---
            smart_prompt = f"""
            Analyze this crop leaf/plant image. Act as an expert agricultural scientist. Provide response STRICTLY in {target_lang_name} language. 
            
            Format response BEAUTIFULLY using clean spacing, bold text, and bullet points. Strictly follow this exact numbering and structure:
            
            **૧. 🌾 પાક/છોડ અને રોગનું નામ:** [Crop/Plant and Disease Name]
            
            **૨. 📊 રોગની અસર (Severity):** [Percentage %] - [Brief explanation of damage]
            
            {weather_instruction}
            
            **૪. 🚨 તાત્કાલિક પગલાં:** WRAP INSIDE HTML TAG: <div class='blinking-warning'> 🚨 તાત્કાલિક પગલાં: [Action time frame] </div>
            
            **૫. 💡 ઉપાય અને પંપ દીઠ સચોટ માપ (Solutions & Pump Dosage):** 
            - 🌿 **પ્રાકૃતિક/ઓર્ગેનિક ઉપાય:** Suggest 2-3 organic methods (e.g., ખાટી છાશ, લીમડાસ્ત્ર). **AI EXPERT CALCULATION REQUIRED:** State precisely how much to mix in a **15-liter pump** (e.g., પંપ દીઠ ૫૦૦ મિલી અથવા પંપ દીઠ ૧૦૦ ગ્રામ).
            - 🧪 **રાસાયણિક ઉપાય:** Provide chemical alternative. **AI EXPERT CALCULATION REQUIRED:** State the exact required dosage for a **15-liter pump**. ADD NOTE: "💡 ખેડૂત મિત્ર માટે નોંધ: રાસાયણિક દવા પાછળ ₹૧૦૦૦ થી ₹૨૦૦૦ નો ખર્ચ થશે અને જમીનને નુકસાન થશે."
            - 🚨 CRITICAL: If Severity is >= 80%: ADD EXACTLY THIS LINE: "🌾 **પાક વીમા યોજના:** નુકસાનીનું વળતર મેળવવા માટે તાત્કાલિક નીચે આપેલા 'પાક વીમા યોજના' બટન પર ક્લિક કરી અરજી કરો."
            
            **૬. 🧮 જમીન અને પંપ ગણતરી (Field & Pump Calculation):**
            - **૧ વીઘા (૨૪ ગુંઠા) માટે પંપનું માપ:** એક વીઘા જમીનમાં અંદાજે **૩ પંપ (૧૫ લિટર વાળા)** દવાનો છંટકાવ કરવો પડે છે.
            - **ખેડૂત માટે ગણતરીની રીત:** તમારા ખેતરના જેટલા વીઘા હોય તેને ૩ પંપ સાથે ગુણાકાર કરવો (દા.ત., જો ૨ વીઘા હોય તો ૨ ગુણ્યા ૩ બરાબર ૬ પંપ). એ મુજબ કુલ દવા તૈયાર કરવી.
            - **એકમની માહિતી:** ૧ હેક્ટર એટલે અંદાજિત ૪.૧૧ વીઘા (૨૪ ગુંઠાના માપ મુજબ).
            
            **૭. 📞 નિષ્ણાતની સલાહ:** 1551 (Kisan Call Center).
            
            8. 📺 SECRET YOUTUBE TAGS: Look at the organic methods you just suggested. Put ALL their names in a comma-separated list inside this exact tag: `[YT_SEARCH: item1, item2]`.
            """

            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": smart_prompt},
                            {
                                "inlineData": {
                                    "mimeType": mime_type,
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ]
            }
            
            success = False
            last_error = ""
            
            for attempt in range(3): 
                status_placeholder.info(f"⏳ રિપોર્ટ તૈયાર થઈ રહ્યો છે (પ્રયત્ન {attempt + 1}/3)...")
                
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{best_model}:generateContent?key={API_KEY}"
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    status_placeholder.empty() 
                    text_response = result['candidates'][0]['content']['parts'][0]['text']
                    image_placeholder.image(uploaded_file, caption='સ્કેનિંગ પૂર્ણ થયું', use_container_width=True)
                    st.success("એકસાથે વિશ્લેષણ પૂર્ણ!")
                    
                    yt_keywords = ["દેશી દવા"] 
                    yt_match = re.search(r'\[YT_SEARCH:\s*(.*?)\]', text_response)
                    
                    if yt_match:
                        raw_keywords = yt_match.group(1).strip()
                        yt_keywords = [kw.strip() for kw in raw_keywords.split(',') if kw.strip()]
                        text_response = re.sub(r'\[YT_SEARCH:\s*.*?\]', '', text_response).strip()
                    
                    # ઓડિયો પ્લેયર (મોબાઈલ અને પીસી બંનેમાં સપોર્ટેડ)
                    if voice_enabled:
                        clean_text = re.sub(r'<[^>]+>', ' ', text_response) 
                        clean_text = re.sub(r'[*#_\-🚨💡🌿🧪🌾📺📍☁️🟢🛡️📊🧮]', ' ', clean_text) 
                        clean_text = clean_text.replace('%', ' ટકા ') 
                        clean_text = clean_text.replace('...', ' ') 
                        clean_text = re.sub(r'\s+', ' ', clean_text).strip() 
                        
                        if target_lang_code == 'gu':
                            audio_text = f"નમસ્કાર. તમારો રિપોર્ટ આ મુજબ છે: {clean_text}"
                        elif target_lang_code == 'hi':
                            audio_text = f"नमस्कार। आपका रिज़ल्ट इस प्रकार है: {clean_text}"
                        elif target_lang_code == 'mr':
                            audio_text = f"नमस्कार. तुमचा निकाल खालीलप्रमाणे आहे: {clean_text}"
                        else:
                            audio_text = f"Hello. Here is your result: {clean_text}"
                        
                        try:
                            tts = gTTS(text=audio_text, lang=target_lang_code)
                            fp = io.BytesIO()
                            tts.write_to_fp(fp)
                            fp.seek(0)
                            audio_b64 = base64.b64encode(fp.read()).decode()
                            audio_html = f'''<div style="background-color: #e8f5e9; padding: 10px; border-radius: 10px; margin-bottom: 15px; width: 100%; box-sizing: border-box;"><p style="margin:0 0 5px 0; color:#2e7d32; font-weight:bold;">🔊 ઓડિયો રિપોર્ટ (અહીંથી સાંભળો):</p><audio autoplay="true" controls style="width: 100%;"><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio></div>'''
                            st.markdown(audio_html, unsafe_allow_html=True)
                        except:
                            pass 
                    
                    st.markdown(f"<div class='result-box'>{text_response}</div>", unsafe_allow_html=True)
                    
                    whatsapp_message = f"🛡️ *AI કૃષિ કવચ - સ્માર્ટ રિપોર્ટ* 🛡️\n\n{text_response}\n\nઆ રિપોર્ટ ચિત્રાસર પ્રાથમિક શાળાના AI પ્રોજેક્ટ દ્વારા જનરેટ થયો છે."
                    encoded_message = urllib.parse.quote(whatsapp_message)
                    whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_message}"
                    
                    maps_url = "https://www.google.com/maps/search/Agro+center+near+me"
                    pmfby_url = "https://pmfby.gov.in/"
                    
                    html_buttons = '<div class="action-container">'
                    html_buttons += f'<a href="{whatsapp_url}" target="_blank" class="action-btn btn-wa">🟢 રિપોર્ટ WhatsApp કરો</a>'
                    
                    if weather_data_success:
                        google_weather_query = urllib.parse.quote(f"Weather in {display_location_name}")
                        google_weather_url = f"https://www.google.com/search?q={google_weather_query}"
                        html_buttons += f'<a href="{google_weather_url}" target="_blank" class="action-btn btn-gw">☁️ લાઈવ હવામાન જુઓ</a>'
                        
                    html_buttons += f'<a href="{maps_url}" target="_blank" class="action-btn btn-map">📍 નજીકનો એગ્રો સ્ટોર</a>'
                    
                    for kw in yt_keywords:
                        youtube_query = urllib.parse.quote(f"How to make {kw} organic farming in {target_lang_name}")
                        youtube_url = f"https://www.youtube.com/results?search_query={youtube_query}"
                        html_buttons += f'<a href="{youtube_url}" target="_blank" class="action-btn btn-yt">📺 {kw} બનાવતા શીખો</a>'
                        
                    html_buttons += f'<a href="{pmfby_url}" target="_blank" class="action-btn btn-pm">🌾 પાક વીમા યોજના</a>'
                    html_buttons += '</div>'
                    
                    st.markdown(html_buttons, unsafe_allow_html=True)
                    
                    success = True
                    break 
                else:
                    result = response.json()
                    last_error = result.get('error', {}).get('message', 'Unknown Error')
                    time.sleep(3)
            
            if not success:
                status_placeholder.empty()
                st.error(f"ગૂગલનું સર્વર હાલમાં ખૂબ જ વ્યસ્ત છે. કૃપા કરીને થોડીવાર પછી ફરી સ્કેન કરો. (એરર: {last_error})")
                
        except Exception as e:
            st.error(f"ઇન્ટરનેટ કે કનેક્શનની ભૂલ: {e}")