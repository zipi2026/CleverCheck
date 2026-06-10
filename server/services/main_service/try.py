# import spacy
#
# nlp = spacy.blank("he")
#
# doc = nlp("המחשב לא מחובר לרשת")
#
# for token in doc:
#     print(token.text, token.dep_)

#import stanza

#stanza.download("he")
#from sentence_transformers import SentenceTransformer


#model = SentenceTransformer(
 #   r"C:\Users\kuperbergz\PycharmProjects\CleverCheck\server\my_model"
#)
#print(model)

#from transformers import AutoConfig

#cfg = AutoConfig.from_pretrained(
 #   r"C:\Users\kuperbergz\PycharmProjects\CleverCheck\server\my_model\onlplabalephbertbase",
  #   local_files_only=True
#)

#print(cfg)

# שימוש בספריה כמו hebrew-nlp או spaCy עם מודול עברי
#from hebrew_tokenizer import tokenize
#
# text = "ניהול משאבי המחשב"
# tokens = list(tokenize(text))  # המרה לרשימה
# print(tokens)
# tokens → ['ניהול', 'משאב', 'מחשב']

# אפשר לבצע השוואה על השורשים/lemmas במקום על המילים הגולמיות
#for token in tokenize("ניהול משאבי המחשב"):
 #   print(repr(token))


import json

with open(
    r"C:\Users\kuperbergz\PycharmProjects\CleverCheck\server\my_model\stanza-he\resources.json",
    encoding="utf8"
) as f:
    data = json.load(f)

print(data.keys())
print(data)