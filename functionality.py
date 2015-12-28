from spacy.en import English
from glob import glob
from collections import defaultdict
from tqdm import tqdm

nlp = English()
# Need a method to extract named entities and the sentences containing
# them.

# Extract entities in a spacy.tokens.doc.Doc object (parsed sentence)
def extract_entities(sentence):
    return map(lambda x:x.string, list(sentence.ents))

# Need a method which accepts a named entity and parent sentence
# and sends them to the data structure
def commit_sentence_entities(sentence, entities):
    dictionary = defaultdict(list)
    for entity in entities:
        dictionary[entity.string].append(sentence.string)
    return dictionary

def read_process_files(pattern):
    filenames = glob(pattern)
    files = [open(f, 'r').read().decode('utf8') for f in filenames]
    processed = []
    for f in tqdm(files):
        processed.append(nlp(f))
    return processed
