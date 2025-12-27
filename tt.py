from db2 import get_doctors, get_doctor_by_specialty, book_appointment
from stt_tts2 import speak, listen
# from test_book_appointment import extract_specialization_semantic
# from tt import extract_specialization
# ---------------- LANGUAGE ----------------
def choose_language():
    speak("Please choose language: Hindi or English", "en")
    choice = listen().lower()
    if "hindi" in choice or "हिंदी" in choice:
        return "hi"
    return "en"

# ---------------- INTENT ----------------
# def detect_intent(text):
#     t = text.lower()
#     if any(w in t for w in ["doctor", "डॉक्टर"]):
#         return "doctor_info"
#     if any(w in t for w in ["appointment", "अपॉइंटमेंट", "book"]):
#         return "appointment"
#     if any(w in t for w in ["no", "नहीं", "exit", "bye"]):
#         return "exit"
#     return "unknown"
def detect_intent(text):
    t = text.lower().strip()

    if any(w in t for w in ["doctor", "docter", "doctors", "physician"]):
        return "doctor_info"

    if any(w in t for w in ["appointment", "appoint", "book", "schedule"]):
        return "appointment"

    if any(w in t for w in ["exit", "bye", "no", "stop"]):
        return "exit"

    return "unknown"


# ---------------- PROBLEM → SPECIALIZATION ----------------
def extract_specialization(text):
    mapping = {
        "Cardiologist": ["heart", "दिल"],
        "Dermatologist": ["skin", "चमड़ी"],
        "ENT": ["ear", "nose", "throat", "ent"],
        "Orthopedic": ["bone", "हड्डी"],
        "Pediatrician": ["child", "baby", "बच्चा"],
        "Neurologist": ["brain", "दिमाग"]
    }
    for spec, words in mapping.items():
        for w in words:
            if w in text.lower():
                return spec
    return None

# ---------------- MAIN FLOW ----------------
def main():
    lang = choose_language()

    welcome = {
        "en": "Welcome to Hospital Assistant. How can I help you?",
        "hi": "हॉस्पिटल सहायक में आपका स्वागत है। आप क्या जानना चाहते हैं?"
    }
    speak(welcome[lang], lang)

    while True:
        query = listen(lang= lang)
        intent = detect_intent(query)

        # EXIT
        if intent == "exit":
            bye = {
                "en": "Thank you. Have a nice day.",
                "hi": "धन्यवाद। आपका दिन शुभ हो।"
            }
            speak(bye[lang], lang)
            break

        # DOCTOR INFO
        if intent == "doctor_info":
            doctors = get_doctors()

            if lang == "en":
                response = "Available doctors are:\n"
                for d in doctors:
                    response += f"{d[0]} - {d[1]} ({d[2]}, {d[3]})\n"
            else:
                response = "उपलब्ध डॉक्टर हैं:\n"
                for d in doctors:
                    response += f"{d[0]} - {d[1]} ({d[2]}, {d[3]})\n"

            speak(response, lang)

            ask_book = {
                "en": "Do you want to book an appointment?",
                "hi": "क्या आप अपॉइंटमेंट बुक करना चाहते हैं?"
            }
            speak(ask_book[lang], lang)

            ans = listen().lower()
            if any(w in ans for w in ["yes", "हाँ", "haan"]):
                ask_problem = {
                    "en": "Please tell me your problem.",
                    "hi": "कृपया अपनी समस्या बताएं।"
                }
                speak(ask_problem[lang], lang)

                problem_text = listen()
                spec = extract_specialization(problem_text)

                if not spec:
                    speak(
                        "Sorry, no suitable doctor found." if lang == "en"
                        else "माफ़ कीजिए, उपयुक्त डॉक्टर नहीं मिला।",
                        lang
                    )
                    continue

                doctor = get_doctor_by_specialty(spec)
                if not doctor:
                    speak(
                        "Doctor not available right now." if lang == "en"
                        else "अभी डॉक्टर उपलब्ध नहीं है।",
                        lang
                    )
                    continue

                doctor_name, specialization, days, time = doctor
                book_appointment(doctor_name, problem_text)

                confirm = {
                    "en": f"Your appointment with {doctor_name} is booked for tomorrow at 10 AM.",
                    "hi": f"आपकी अपॉइंटमेंट {doctor_name} के साथ कल सुबह 10 बजे बुक हो गई है।"
                }
                speak(confirm[lang], lang)

        else:
            speak(
                "Sorry, I did not understand." if lang == "en"
                else "माफ़ कीजिए, मैं समझ नहीं पाई।",
                lang
            )

if __name__ == "__main__":
    main()
