
import stanza

nlp = stanza.Pipeline(
    lang="he",
    dir=r"C:\Users\kuperbergz\PycharmProjects\CleverCheck\server\my_model\stanza-he",
    processors="tokenize,pos,lemma",
    download_method=None
)

#doc = nlp("המחשב מנהלת את משאבי המחשב")
#for sent in doc.sentences:
    #for word in sent.words:
        #print(word.text, "->", word.lemma)