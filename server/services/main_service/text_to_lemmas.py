from typing import List

import stanza
# -----------------------------
# אתחול Stanza
# -----------------------------

nlp = stanza.Pipeline(
    lang="he",
    dir=r"C:\Users\kuperbergz\PycharmProjects\CleverCheck\server\my_model\stanza-he",
    processors="tokenize,pos,lemma",
    download_method=None
)

# -----------------------------
# פונקציה לעבודה על צורת בסיס
# -----------------------------
def text_to_lemmas(text: str) -> List[str]:
    doc = nlp(text)
    lemmas = [word.lemma for sent in doc.sentences for word in sent.words]
    return lemmas

print(text_to_lemmas("מערכת ההפעלה מנהלת את משאבי המחשב"))