import re
import nltk
import numpy as np
from nltk.corpus import wordnet as wn

class ObjectiveTest:

#data= """A common mix-up among aspiring data professionals is the differences between data analysts and data scientists. While there isn’t a clear line between the two roles – depending on the company, data analysts and data scientists may be involved in the same kind of tasks – there are also important differences regarding the nature of the work and the level of expertise in data usage. 

#As for the nature of the work, the data analyst has a rather exploratory and descriptive profile in contrast to the more experimental profile in the case of data scientist. 

#The data analyst form is more about finding patterns in big columns of (structured) data, building visualizations and reports, and communicating insights. 

#On the other hand, data scientists tend to deal with the unexpected through the use of techniques that fall in the realm of predictive analytics. This normally entails developing data models and machine learning algorithms to make predictions about the future.

#As for the level of expertise required for the two roles, data scientists are sometimes considered a more technical version of a data analyst. Overall, data scientists should be more fluent in advanced programming and computing tools. Also, since data scientists are responsible for developing data models and machine learning algorithms, they need to have a solid background in math and statistics. """

    def __init__(self, data, noOfQues):
        
        self.summary = data
        self.noOfQues = noOfQues

    def get_trivial_sentences(self):
        sentences = nltk.sent_tokenize(self.summary)
        trivial_sentences = list()
        for sent in sentences:
            trivial = self.identify_trivial_sentences(sent)
            if trivial:
                trivial_sentences.append(trivial)
            else:
                continue
        return trivial_sentences

    def identify_trivial_sentences(self, sentence):
        tags = nltk.pos_tag(sentence)
        if tags[0][1] == "RB" or len(nltk.word_tokenize(sentence)) < 4:
            return None
        
        noun_phrases = list()
        grammer = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
                {<NN>+<IN|DT>*<NNP>+}
                {<NNP>+<NNS>*}
            """
        chunker = nltk.RegexpParser(grammer)
        tokens = nltk.word_tokenize(sentence)
        pos_tokens = nltk.tag.pos_tag(tokens)
        tree = chunker.parse(pos_tokens)

        for subtree in tree.subtrees():
            if subtree.label() == "CHUNK":
                temp = ""
                for sub in subtree:
                    temp += sub[0]
                    temp += " "
                temp = temp.strip()
                noun_phrases.append(temp)
        
        replace_nouns = []
        for word, _ in tags:
            for phrase in noun_phrases:
                if phrase[0] == '\'':
                    break
                if word in phrase:
                    [replace_nouns.append(phrase_word) for phrase_word in phrase.split()[-2:]]
                    break
            if len(replace_nouns) == 0:
                replace_nouns.append(word)
            break
        
        if len(replace_nouns) == 0:
            return None
        
        val = 99
        for i in replace_nouns:
            if len(i) < val:
                val = len(i)
            else:
                continue
        
        trivial = {
            "Answer": " ".join(replace_nouns),
            "Key": val
        }

        if len(replace_nouns) == 1:
            trivial["Similar"] = self.answer_options(replace_nouns[0])
        else:
            trivial["Similar"] = []
        
        replace_phrase = " ".join(replace_nouns)
        blanks_phrase = ("__________" * len(replace_nouns)).strip()
        expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
        sentence = expression.sub(blanks_phrase, str(sentence), count=1)
        trivial["Question"] = sentence
        return trivial

    @staticmethod
    def answer_options(word):
        synsets = wn.synsets(word, pos="n")

        if len(synsets) == 0:
            return []
        else:
            synset = synsets[0]
        
        hypernym = synset.hypernyms()[0]
        hyponyms = hypernym.hyponyms()
        similar_words = []
        for hyponym in hyponyms:
            similar_word = hyponym.lemmas()[0].name().replace("_", " ")
            if similar_word != word:
                similar_words.append(similar_word)
            if len(similar_words) == 8:
                break
        return similar_words

    def generate_test(self):
        trivial_pair = self.get_trivial_sentences()
        question_answer = list()
        for que_ans_dict in trivial_pair:
            if que_ans_dict["Key"] > int(self.noOfQues):
                question_answer.append(que_ans_dict)
            else:
                continue
        question = list()
        answer = list()
        while len(question) < int(self.noOfQues):
            rand_num = np.random.randint(0, len(question_answer))
            if question_answer[rand_num]["Question"] not in question:
                question.append(question_answer[rand_num]["Question"])
                answer.append(question_answer[rand_num]["Answer"])
            else:
                continue
        return question, answer