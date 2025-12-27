import sys
sys.path.append('hospital-assistant')
from db2 import book_appointment
from tt import extract_specialization
from stt_tts2 import listen
test_inputs = [
    "heart",
    "heart pain",
    "my heart is hurting",
    "bone",
    "bone fracture",
    "bones mein dard",
    "mere dil mein dard hai",
    "ear problem",
    "skin allergy"
]

for text in test_inputs:
    print("\nUser said:", text)
    result = extract_specialization(text)
    print("Detected specialization:", result)
print("listening:----------")
problem_text = listen()
print("DEBUG user said:", problem_text)


# # Test the book_appointment function
# try:
#     book_appointment("Dr. Sharma", "Heart problem")
#     print("Appointment booked successfully!")
# except Exception as e:
#     print(f"Error: {e}")
# from sentence_transformers import SentenceTransformer, util
# import torch

# # Load model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Specialization reference sentences
# SPECIALIZATION_DB = {
#     "Cardiologist": [
#         "heart problem",
#         "chest pain",
#         "dil mein dard",
#         "heart pain"
#     ],
#     "Orthopedic": [
#         "bone fracture",
#         "joint pain",
#         "haddi mein dard",
#         "bone pain"
#     ],
#     "Dermatologist": [
#         "skin allergy",
#         "skin problem",
#         "rashes on skin"
#     ],
#     "ENT": [
#         "ear pain",
#         "nose problem",
#         "throat infection"
#     ],
#     "Neurologist": [
#         "brain problem",
#         "headache",
#         "migraine"
#     ],
#     "Pediatrician": [
#         "child fever",
#         "baby health problem"
#     ]
# }

# # Precompute embeddings
# spec_embeddings = {}
# for spec, sentences in SPECIALIZATION_DB.items():
#     spec_embeddings[spec] = model.encode(sentences, convert_to_tensor=True)

# def extract_specialization_semantic(text, threshold=0.55):
#     user_embedding = model.encode(text, convert_to_tensor=True)

#     best_spec = None
#     best_score = 0

#     for spec, emb in spec_embeddings.items():
#         scores = util.cos_sim(user_embedding, emb)
#         max_score = torch.max(scores).item()

#         if max_score > best_score:
#             best_score = max_score
#             best_spec = spec

#     if best_score >= threshold:
#         return best_spec, round(best_score, 2)

#     return None, best_score


# # ---------------- TESTING ----------------
# test_inputs = [
#     "heart",
#     "heart pain",
#     "my heart is hurting",
#     "bone",
#     "bone fracture",
#     "bones mein dard",
#     "mere dil mein dard hai",
#     "ear problem",
#     "skin allergy"
# ]

# for text in test_inputs:
#     spec, score = extract_specialization_semantic(text)
#     print(f"\nUser said: {text}")
#     print("Detected:", spec)
#     print("Confidence:", score)
