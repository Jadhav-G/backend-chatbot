# from flask import Flask, render_template, request, jsonify
# from MedQuard import *





from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from MedQuard import answer_query
from datetime import timedelta
import sqlite3
import re

# model_path = "gpt2"

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
app.secret_key = "mediqa_secret_key"
app.permanent_session_lifetime = timedelta(minutes=60)
DB_PATH = "mediqa.db"

# -------------------- Helper Function --------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------- Keyword Detector --------------------
def is_medical_query(query):
    medical_keywords = [ 
        "fever", "pain", "headache", "diabetes", "medicine", "treatment", "disease",
        "pain", "headache", "diabetes", "medicine", "treatment", "disease",
        "symptom", "health", "infection", "blood", "heart", "kidney", "cough", "cold",
        "fracture", "injury", "doctor", "hospital", "covid", "bp", "pressure",
        "cholesterol", "virus", "cancer", "therapy", "vaccine", "checkup", "nutrition","disease", "symptom", "treatment", "medicine", "doctor", "nurse",
        "hospital", "clinic", "health", "wellness", "pain", "fever", "infection",
        "diabetes", "heart", "lungs", "stomach", "blood", "allergy", "asthma",
        "depression", "sleep", "injury", "fracture", "virus", "bacteria", "pill",
        "tablet", "injection", "vaccine", "checkup", "therapy", "diagnosis","disease", "symptom", "treatment", "medicine", "doctor", "pain", "fever",
        "infection", "diabetes", "sugar", "bp", "blood", "heart", "virus", "health",
        "body", "injury", "cough", "covid", "flu", "headache", "allergy", "therapy",
        "surgery", "hospital", "nurse", "tablet", "capsule", "vaccine", "diet", "fitness","disease", "symptom", "treatment", "medicine", "doctor", "nurse", "hospital", "clinic",
        "health", "wellness", "pain", "fever", "infection", "diabetes", "cancer", "covid",
        "covid-19", "coronavirus", "flu", "virus", "bacteria", "antibiotic", "heart", "liver",
        "kidney", "lungs", "stomach", "brain", "spine", "blood", "bp", "cholesterol", "sugar",
        "injury", "fracture", "sprain", "allergy", "asthma", "pneumonia", "bronchitis", "thyroid",
        "hormone", "periods", "fertility", "pregnancy", "delivery", "gynecology", "cardiology",
        "neurology", "dermatology", "headache", "migraine", "toothache", "back pain",
        "stomach pain", "joint pain", "eye pain", "ear pain", "neck pain", "shoulder pain",
        "muscle pain", "leg pain", "arm pain", "fatigue", "weakness", "dizziness", "vomiting",
        "nausea", "diarrhea", "constipation", "cold", "cough", "runny nose", "sore throat",
        "sinus", "tonsils", "ear infection", "eye infection", "skin infection", "itching",
        "rash", "acne", "pimple", "eczema", "dry skin", "hair fall", "dandruff", "baldness",
        "sweating", "dehydration", "thirst", "appetite", "obesity", "weight gain", "weight loss",
        "diet", "nutrition", "vitamin", "protein", "calcium", "iron", "minerals", "exercise",
        "workout", "yoga", "gym", "meditation", "stress", "anxiety", "depression", "anger",
        "sleep", "insomnia", "dream", "mental health", "therapy", "counseling", "addiction",
        "smoking", "alcohol", "drugs", "medicine overdose", "rehab", "detox", "chest pain",
        "heart attack", "stroke", "bp high", "bp low", "sugar level", "thyroid level",
        "pulse", "oxygen", "spo2", "temperature", "fever cold", "body pain", "burn", "wound",
        "cut", "bleeding", "first aid", "bandage", "ointment", "cream", "tablet", "capsule",
        "syrup", "injection", "vaccine", "booster", "mask", "sanitizer", "gloves", "PPE",
        "quarantine", "isolation", "sanitation", "cleanliness", "hand wash", "soap", "disinfectant",
        "ambulance", "emergency", "paramedic", "ICU", "oxygen cylinder", "ventilator",
        "blood test", "urine test", "x-ray", "mri", "ct scan", "ultrasound", "report", "result",
        "hospital bed", "doctor appointment", "consultation", "follow-up", "checkup", "health camp",
        "medical record", "health insurance", "medical report", "lab test", "ECG", "EEG",
        "blood pressure", "glucose test", "cholesterol test", "thyroid test", "vitamin test",
        "pregnancy test", "urine infection", "UTI", "bladder", "kidney stone", "liver problem",
        "jaundice", "hepatitis", "gas", "acidity", "ulcer", "heartburn", "indigestion", "bloating",
        "appendix", "appendicitis", "diarrhea", "constipation", "vomit", "food poisoning",
        "gastritis", "acidity", "chest burn", "reflux", "stomach infection", "stomach ache",
        "digestion", "colon", "intestine", "rectum", "anus", "bowel", "urination", "pee", "poop",
        "period pain", "menstrual cramps", "vaginal infection", "pregnant", "baby", "childbirth",
        "breastfeeding", "breast pain", "breast lump", "menopause", "ovulation", "fertility problem",
        "infertility", "contraceptive", "birth control", "condom", "ivf", "sexual health",
        "erection", "libido", "semen", "sperm", "penis", "vagina", "uterus", "ovary", "cervix",
        "testis", "prostate", "hormonal imbalance", "hair loss", "pimples", "skin glow", "diet plan",
        "healthy food", "junk food", "cholesterol level", "blood sugar", "sugar test",
        "bp monitor", "blood donor", "blood donation", "organ donor", "plasma", "transfusion",
        "sleep problem", "sleep disorder", "breathing problem", "asthma attack", "inhaler",
        "nebulizer", "allergy tablet", "painkiller", "antibiotic", "antacid", "paracetamol",
        "ibuprofen", "aspirin", "cetirizine", "dolo", "disprin", "crocin", "vicks", "betadine",
        "detol", "band aid", "plaster", "thermometer", "stethoscope", "bp machine", "glucometer",
        "pulse oximeter", "sanitizer", "mask", "vicks", "ointment", "bandage", "cream",
        "eczema cream", "rash cream", "allergy cream", "eye drop", "nasal spray", "ear drop",
        "toothpaste", "toothbrush", "mouthwash", "floss", "dentist", "tooth decay", "cavity",
        "gum pain", "dental care", "eye doctor", "spectacles", "contact lens", "eye test",
        "vision", "cataract", "glaucoma", "blurred vision", "hearing loss", "ear wax",
        "ENT doctor", "speech problem", "voice problem", "throat pain", "tonsil", "cough syrup",
        "cold tablet", "flu medicine", "runny nose", "sneezing", "fever tablet", "body pain tablet",
        "stomach tablet", "digestion medicine", "anti vomiting", "laxative", "gas tablet",
        "sleeping pill", "anxiety medicine", "depression medicine", "stress relief", "therapy",
        "counselor", "psychologist", "psychiatrist", "mental illness", "panic attack",
        "fear", "phobia", "anger issues", "suicide", "self harm", "help line", "emergency number",
        "health awareness", "dental checkup", "eye checkup", "full body checkup", "doctor visit",
        "consult doctor", "call doctor", "online doctor", "telemedicine", "health tips",
        "home remedy", "natural cure", "herbal medicine", "ayurveda", "homeopathy", "naturopathy",
        "unani", "exercise daily", "drink water", "eat fruits", "avoid junk food", "sleep well",
        "walk", "running", "cycling", "swimming", "hiking", "breathing exercise", "stretching",
        "healthy habit", "immunity booster", "vitamin c", "vitamin d", "protein powder",
        "protein shake", "energy drink", "green tea", "detox water", "sugar control", "bp control",
        "stress control", "mental peace", "positive mind", "mindfulness", "emotional balance",
        "happiness", "fitness goal", "diet chart", "meal plan", "water intake", "steps count",
        "yoga pose", "sun salutation", "pranayama", "meditation time", "work life balance",
        "office stress", "study stress", "exam stress", "sleep schedule", "eye strain",
        "computer vision", "screen time", "blue light", "neck stiffness", "backache", "posture",
        "ergonomics", "hand pain", "shoulder stiffness", "knee pain", "ankle pain", "muscle cramp",
        "leg swelling", "arm weakness", "fatigue", "sleepy", "tired", "body weakness",
        "low energy", "cold hand", "cold feet", "dehydrated", "heat stroke", "sunburn", "rash",
        "mosquito bite", "insect bite", "snake bite", "dog bite", "animal bite", "first aid kit",
        "emergency medicine", "CPR", "paramedic", "rescue", "ambulance service", "hospital staff",
        "nursing", "healthcare worker", "public health", "WHO", "CDC", "health department",
        "health ministry", "disease prevention", "healthcare awareness", "vaccine drive",
        "sanitary pad", "menstrual hygiene", "period hygiene", "baby care", "child care",
        "newborn", "infant", "immunization", "vaccine schedule", "child nutrition",
        "school health", "teen health", "women health", "men health", "senior citizen health",
        "elderly care", "home nurse", "family doctor", "primary care", "emergency care",
        "ICU care", "operation", "surgery", "minor surgery", "major surgery", "eye operation",
        "heart surgery", "knee replacement", "hip replacement", "appendix operation",
        "c-section", "delivery operation", "plastic surgery", "skin care", "anti aging",
        "wrinkles", "face glow", "beauty tips", "hair growth", "healthy hair", "shampoo",
        "conditioner", "hair oil", "hair serum", "face wash", "face cream", "sunscreen",
        "lip balm", "moisturizer", "body lotion", "massage", "spa", "relax", "healing",
        "self care", "well being", "lifestyle", "balanced diet", "healthy routine",
        "disease prevention", "health monitoring", "early diagnosis", "checkup reminder",
        "medicine reminder", "health tracker", "pulse rate", "heart rate", "oxygen monitor",
       "blood monitor", "temperature monitor", "fitbit", "smartwatch", "wearable device",
        "telehealth", "chatbot", "AI doctor", "health assistant", "virtual doctor","immune", "immunity", "immunization", "immune system","hydration", "dehydrated", "water intake", "drink water", "fluids","anemia", "haemoglobin", "iron deficiency", "fatigue", "weakness",
        "malaria", "mosquito", "infection", "parasite", "fever", "chills","dose", "missed dose", "medicine schedule", "prescription", "tablet","weight", "obesity", "fat", "calories", "metabolism", "diet plan", "exercise","hemoglobin", "iron", "blood cells", "red blood cells", "oxygen level",
        "coffee", "caffeine", "energy", "addiction", "sleep", "blood pressure","focus", "concentration", "brain health", "mental focus", "memory","breastfeeding", "lactation", "milk supply", "infant feeding", "mother care","pregnancy", "morning sickness", "vomiting", "nausea", "pregnant women","child", "kids", "infant", "children", "immunity", "growth", "nutrition",
        "pain relief", "home remedy", "remedy", "healing process", "wellness tip", "healthy habit",
"recovery", "rehabilitation", "body temperature", "chills", "sweating", "fainting",
"blood loss", "high fever", "low fever", "disease control", "symptom checker",
"patient", "outpatient", "inpatient", "pharmacy", "chemist", "drugstore",
"medical advice", "diagnosis", "diagnose", "treatment plan", "therapy session",
"doctor consultation", "online consultation", "teleconsultation", "medical history",
"medical advice", "prescription drug", "medical condition", "medical issue",
"physical health", "mental wellbeing", "mental health support", "emotional health",
"stress relief", "wellbeing", "fitness routine", "exercise plan", "gym routine",
"health tips", "nutritional value", "calorie intake", "vitamin deficiency",
"mineral deficiency", "food supplement", "protein intake", "hydration level",
"immune booster", "antioxidant", "detox", "cleansing", "body detox", "balanced meal",
"meal plan", "healthy recipe", "health drink", "herbal drink", "green juice",
"fatigue recovery", "tiredness", "back pain relief", "muscle stretch", "pain therapy",
"joint stiffness", "swelling", "inflammation", "pain management", "chronic pain",
"acute pain", "emergency room", "hospitalization", "medical care", "healthcare",
"health facility", "doctor advice", "patient care", "blood donor", "health campaign",
"preventive care", "disease awareness", "health risk", "health test", "screening test",
"annual checkup", "routine checkup", "self examination", "breast self exam",
"skin care routine", "eye care", "dental hygiene", "oral care", "brushing teeth",
"hand hygiene", "sleep hygiene", "body hygiene", "clean environment", "healthy environment",
"immunity support", "recovery time", "body healing", "wellbeing support","headache", "fever", "cough", "sore throat", "nausea", "vomiting", "diarrhea", "prescription", "medication", "over-the-counter", "antibiotics", "painkiller", "vaccine", "blood pressure", "heart rate", "cholesterol", "blood sugar", "diabetes management", "nutrition", "healthy diet", "exercise", "weight management", "hydration", "vitamins", "mental health", "stress relief", "anxiety", "depression", "insomnia", "therapy", "symptom checker", "diagnosis", "treatment", "prognosis", "medical history", "clinic", "pharmacy", "urgent care", "telehealth", "telemedicine", "patient portal", "physical therapy", "surgery", "post-op", "rehabilitation", "first aid", "CPR", "dermatology", "cardiology", "neurology", "pediatrics", "oncology", "radiology", "blood test", "urine test", "X-ray", "MRI scan", "CT scan", "ultrasound", "biopsy", "allergy", "asthma", "infection", "virus", "bacteria", "contagious", "outbreak",
"abdominal pain", "joint pain", "muscle pain", "chest pain", "back pain", "sprain", "strain", "fracture", "concussion", "head injury", "burn", "cut", "wound care", "bleeding", "bruise", "blister", "rash", "itchy skin", "eczema", "psoriasis", "acne", "sunburn", "cold symptoms", "flu symptoms", "sinusitis", "bronchitis", "pneumonia", "indigestion", "heartburn", "constipation", "acid reflux", "food poisoning", "dehydration", "malnutrition", "obesity", "anemia", "arthritis", "osteoporosis", "dementia", "Alzheimer's", "Parkinson's", "stroke", "heart attack", "hypertension", "hypotension", "insomnia", "sleep apnea", "migraine", "Vertigo", "dizziness", "fatigue", "lethargy", "weakness", "fainting", "seizure", "epilepsy", "thyroid", "hormone imbalance", "menopause", "pregnancy", "prenatal care", "postnatal care", "fertility", "infertility", "birth control", "STD", "UTI", "kidney stones", "liver disease", "hepatitis", "cirrhosis", "gastroenteritis", "GERD", "IBS", "Crohn's disease", "ulcer", "appendicitis", "cancer", "tumor", "chemotherapy", "radiation therapy", "biopsy", "remission", "palliative care", "hospice", "mental wellness", "counseling", "psychiatry", "psychology", "trauma", "phobia", "addiction", "substance abuse", "rehab", "detox", "emergency", "paramedic", "ambulance", "triage", "intensive care", "ICU", "vital signs", "immunization", "booster shot",
"headache", "fever", "cough", "cold", "flu", "sore throat", "runny nose", "tired", "sleep", "stress", "anxiety", "pain", "ache", "stomach ache", "eat healthy", "nutrition", "vitamins", "hydration", "drink water", "exercise", "fitness", "wellness", "self-care", "hygiene", "wash hands", "soap", "clean", "brush teeth", "dental care", "skin care", "sunscreen", "cut", "scrape", "bruise", "band-aid", "first aid", "medicine", "take medicine", "pain reliever", "pharmacy", "prescription", "doctor", "checkup", "appointment", "rest", "energy", "dizzy", "nausea", "rash", "itchy", "swelling", "burn", "ice pack", "calories", "healthy food", "weight", "rest",
"headache", "fever", "cough", "cold", "flu", "sore throat", "runny nose", "sneezing", "tired", "fatigue", "sleepy", "energy", "stress", "anxiety", "nervous", "sad", "mood", "pain", "ache", "stomach ache", "back pain", "muscle ache", "dizzy", "nausea", "vomiting", "diarrhea", "constipation", "heartburn", "indigestion", "appetite", "eat", "drink", "sleep", "rest", "exercise", "walk", "stretch", "relax", "self-care", "hygiene", "wash", "wash hands", "soap", "clean", "shower", "bath", "brush teeth", "floss", "dental care", "oral hygiene", "skin care", "lotion", "sunscreen", "sunburn", "rash", "itchy", "pimple", "acne", "food", "diet", "nutrition", "healthy food", "healthy eating", "vegetables", "fruit", "water", "drink water", "hydration", "thirsty", "vitamins", "calories", "sugar", "salt", "protein", "weight", "hunger", "snack", "meal", "breakfast", "lunch", "dinner", "cut", "scrape", "scratch", "bruise", "bump", "burn", "blister", "swelling", "band-aid", "bandage", "first aid", "ice pack", "wound", "health", "wellness", "fitness", "body", "mind", "doctor", "nurse", "pharmacy", "medicine", "pills", "checkup", "appointment", "symptom"
,
        "stress", "anxiety", "pain", "ache", "symptom"
    ]
    query_lower = query.lower()
    return any(word in query_lower for word in medical_keywords)

# -------------------- More Info Detector --------------------
def wants_more_info(query):
    more_info_keywords = ["more", "details", "explain", "expand", "tell me more", "in detail"]
    query_lower = query.lower()
    return any(kw in query_lower for kw in more_info_keywords)

# -------------------- Home --------------------
@app.route('/')
def index():
    if "user" in session:
        return redirect(url_for('chat'))
    return render_template('index.html')

# -------------------- Signup --------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "user" in session:
        return redirect(url_for('chat'))

    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing = cur.fetchone()
        if existing:
            conn.close()
            return render_template('signup.html', error="Email already registered. Please log in.")

        cur.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
                    (fname, lname, email, password))
        conn.commit()
        conn.close()

        session["user"] = fname
        session["email"] = email
        session.permanent = True
        return redirect(url_for('chat'))

    return render_template('signup.html')

# -------------------- Login --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session:
        return redirect(url_for('chat'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user["first_name"]
            session["email"] = user["email"]
            session.permanent = True
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error="Invalid email or password.")

    return render_template('login.html')

# -------------------- Logout --------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# -------------------- Chat Page --------------------
@app.route('/chat')
def chat():
    if "user" not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chats WHERE user_email = ? ORDER BY created_at DESC", (session["email"],))
    chats = cur.fetchall()

    messages = []
    current_chat_id = None
    if chats:
        last_chat_id = chats[0]['id']
        current_chat_id = last_chat_id
        cur.execute("SELECT * FROM messages WHERE chat_id = ? ORDER BY id ASC", (last_chat_id,))
        messages = cur.fetchall()

    conn.close()
    return render_template('chat.html', username=session["user"], chats=chats, messages=messages, current_chat_id=current_chat_id)

# -------------------- New Chat --------------------
@app.route('/new_chat')
def new_chat():
    if "user" not in session:
        return redirect(url_for('login'))

    # ✅ Clear old chat session
    session.pop('current_chat_id', None)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO chats (user_email, title) VALUES (?, ?)", (session["email"], "New Chat"))
    conn.commit()
    chat_id = cur.lastrowid
    conn.close()

    # ✅ Store this chat in session
    session['current_chat_id'] = chat_id

    return redirect(url_for('chat_view', chat_id=chat_id))

# -------------------- Chat View --------------------
@app.route('/chat/<int:chat_id>')
def chat_view(chat_id):
    if "user" not in session:
        return redirect(url_for('login'))

    session['current_chat_id'] = chat_id  # ✅ track current chat

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chats WHERE user_email = ? ORDER BY created_at DESC", (session["email"],))
    chats = cur.fetchall()
    cur.execute("SELECT * FROM messages WHERE chat_id = ? ORDER BY id ASC", (chat_id,))
    messages = cur.fetchall()
    conn.close()

    return render_template('chat.html', username=session["user"], chats=chats, messages=messages, current_chat_id=chat_id)

# -------------------- Ask Chatbot --------------------
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get('question', '').strip()
    chat_id = data.get('chat_id', None)

    if not question:
        return jsonify({'answer': 'Please ask a valid question.'})

    greetings = ["hi","Hi","Hello", "Hey","Hiii", "Hii" "hello", "hey", "hii", "hiii"]
    if question in greetings:
        return jsonify({
            "answer": "Hello! I'm your AI Health Assistant. How can I help you today?"
        })
   
    identity_questions = [
        "who are you", "what is your name", "who is this", "tell me about yourself"
    ]
    for q in identity_questions:
        if q in question:
            return jsonify({
                "answer": "I am MediQA, your AI Health Assistant. I am designed to help you with medical information and first-level health guidance."
            })


    # --- Developer Identification Intent ---
    developer_questions = [
        "who is your developer", "who developed you", "your creator",
        "who made you", "who built you", "who created you"
    ]
    
    q_lower = question.lower()
    for q in developer_questions:
        if q in q_lower:
            return jsonify({
                "answer": (
                    "I  was  designed by Mr. Ganesh Namdev Jadhav, under  the  guidance  of "
                    "Prof. Pallavi Patil (B.Tech guide) and \n Prof. Pravin More (Honors project guide). "
                    "I provide general medical information and first-level guidance to help you understand medical concerns."
                )
            })

    # --- Existing logic preserved ---
    if wants_more_info(question):
        response = "🩺 Sure! Here are more detailed insights:\n" + answer_query(session.get("last_question", question))
    elif not is_medical_query(question):
        response = "💡 This seems non-medical. I can only assist with health-related queries."
    else:
        response = answer_query(question).strip()
        if len(response.split()) > 85:
            response = " ".join(response.split()[:85]) + "..."

    # --- end ---

    conn = get_db_connection()
    cur = conn.cursor()

    #  Use same chat_id for the session until "New Chat" clicked
    if not chat_id:
        chat_id = session.get('current_chat_id')
        if not chat_id:
            cur.execute("INSERT INTO chats (user_email, title) VALUES (?, ?)", (session["email"], "New Chat"))
            conn.commit()
            chat_id = cur.lastrowid
            session['current_chat_id'] = chat_id

    cur.execute("INSERT INTO messages (chat_id, user_email, question, answer) VALUES (?, ?, ?, ?)",
                (chat_id, session["email"], question, response))
    conn.commit()
    conn.close()

    session["last_question"] = question
    return jsonify({'answer': response})

# -------------------- Run Flask --------------------
if __name__ == '__main__':
    app.run(debug=True)
