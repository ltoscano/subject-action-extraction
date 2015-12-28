from spacy.en import English
from spacy import parts_of_speech
from nltk.corpus import stopwords
nlp = English()

def subject_verb(doc):

    def noun_exists_in_tree(token_list):
        if any(map(lambda x: x.pos == parts_of_speech.NOUN, token_list)):
            return True
        elif any(map(lambda x: noun_exists_in_tree(x.children), token_list)):
            return True
        return False

    # To hold the previous subject name outside the loop in case the next
    # sentence refers to the subject as He/She.
    subject_holder = ""

    holder = []
    for sent in list(doc.sents):
        if sent.root.pos == parts_of_speech.VERB:
            subject = filter(lambda x: x.dep_ in ['nsubj', 'nsubjpass'], sent.root.children)[0]
            if subject.tag_ == 'PRP':
                subject = subject_holder
            else:
                subject = "".join([x.string for x in subject.subtree])
                subject_holder = subject
            children = filter(lambda x: x.dep_ not in ['nsubj','nsubpass'], sent.root.children)
            #children = filter(
            #                lambda x: x.pos != parts_of_speech.PUNCT, children
            #           )
            children = filter(lambda x:
                                noun_exists_in_tree(x.children) or
                                x.pos == parts_of_speech.NOUN,
                                children
                       )
            for child in children:
                child_string = "".join([x.string for x in child.subtree])
                if child.dep_ == 'conj' and child.pos == parts_of_speech.VERB:
                    holder.append(" ".join([subject, child_string]))
                else:
                    holder.append(" ".join([subject, sent.root.string, child_string)])
    return holder
