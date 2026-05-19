
# from sentence_transformers import SentenceTransformer

# 1. Load a pretrained Sentence Transformer model
# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# The sentences to encode
# sentences = [
#     "The weather is lovely today.",
#     "It's so sunny outside!",
#     "He drove to the stadium.",
# ]

# 2. Calculate embeddings by calling model.encode()
# embeddings = model.encode(sentences)
# print(embeddings.shape)
# [3, 384]

# 3. Calculate the embedding similarities
# similarities = model.similarity(embeddings, embeddings)
# print(similarities)
# tensor([[1.0000, 0.6660, 0.1046],
#         [0.6660, 1.0000, 0.1411],
#         [0.1046, 0.1411, 1.0000]])



# אני רוצה כזה דבר בעברית
# מעולה! אפשר ליצור גרסה כזו בעברית בדיוק באותו רעיון, עם **SentenceTransformers** שמכיל מודלים שתומכים בעברית. אני אסביר איך עושים את זה צעד־צעד:


### 1️⃣ התקנת ספריות


### 2️⃣ קוד לדוגמה בעברית


from sentence_transformers import SentenceTransformer, util

# טוענים מודל שתומך בעברית
model = SentenceTransformer(r"C:\Users\kuperbergz\PycharmProjects\CleverCheck\server\my_model")

# תשובה של התלמיד ותשובה נכונה
student_answer = "השמש זורחת במזרח"
correct_answer = "הכיוון של זריחת השמש הוא ממערב"

# 1. יצירת Embeddings
emb1 = model.encode(student_answer, convert_to_tensor=True)
emb2 = model.encode(correct_answer, convert_to_tensor=True)

# 2. חישוב דמיון קוסינוס
similarity = util.pytorch_cos_sim(emb1, emb2)

# 3. הדפסה
print("Cosine similarity:", similarity.item())

