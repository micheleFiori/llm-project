import pandas as pd
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
import spacy
from sklearn.metrics.pairwise import cosine_similarity

class Examples_manager:
    def __init__(self, filename):
        self.examples_df = pd.read_csv(filename)
        self.model_embeddings = SentenceTransformer('all-MiniLM-L6-v2')

    #TODO SCEGLIERE SE FARE SIMILARITY TRA TESTI O VETTORI DI CONSISTENZA
    def get_most_similar_examples(self, context, similarity = 'cosine', k):
        if similarity == 'cosine':
            most_similar_examples = self.text_similarity_cosine(context, self.examples_df, k)
        if similarity == 'jaccard':
            most_similar_examples = self.text_similarity_jaccard(context, self.examples_df, k)

        return most_similar_examples
    

    def text_similarity_cosine(self, context, pool_examples, k):
        cosine_similarities = [util.cos_sim(self.model_embeddings.encode(context, convert_to_tensor=True), self.model_embeddings.encode(doc, convert_to_tensor=True)) for doc in pool_examples['context']]
        document_similarity_scores = [(i, score[0][0].cpu().numpy()) for i, score in enumerate(cosine_similarities)]
        sorted_similarity_scores = sorted(document_similarity_scores, key=lambda x: x[1], reverse=True)

        return [{ 'context': pool_examples['context'][s[0]], 'expected_output': pool_examples['activities'][s[0]]} for s in sorted_similarity_scores][:k]
        #return sorted_similarity_scores

    def text_similarity_jaccard(self, context, pool_examples, k):

        preprocessed_documents = [self.preprocess_text(doc) for doc in pool_examples['context']]
        preprocessed_query = self.preprocess_text(context)

        jaccard_similarities = [self.jaccard_similarity(preprocessed_query, doc) for doc in preprocessed_documents]
        document_similarity_scores = [(i, score) for i, score in enumerate(jaccard_similarities)]
        sorted_similarity_scores = sorted(document_similarity_scores, key=lambda x: x[1], reverse=True)

        return [{ 'context': pool_examples['context'][s[0]], 'expected_output': pool_examples['activities'][s[0]]} for s in sorted_similarity_scores][:k]
        #return sorted_similarity_scores

    @staticmethod
    def preprocess_text(text):
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())
        #words = [ps.stem(word) for word in words if word.isalpha()]
        #words = [word for word in words if word not in stop_words] #DA VEDERE SE HA SENSO TOGLIERE LE STOPWORDS (IMO NO)
        return set(words)
    

    @staticmethod
    def jaccard_similarity(set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union