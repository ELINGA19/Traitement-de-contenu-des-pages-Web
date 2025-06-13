from typing import List, Tuple
from collections import Counter
from simple_indexer import SimpleIndexer

class DocumentRetriever:
    def __init__(self, indexer: SimpleIndexer):
        self.indexer = indexer

    def normalize_words(self, words: List[str]) -> List[str]:
        return [word.lower() for word in words]

    def search(self, query_words: List[str]) -> List[Tuple[str, int]]:
        if not self.indexer.index:
            return []

        query_words = self.normalize_words(query_words)
        doc_scores = Counter()

        for word in query_words:
            for doc in self.indexer.index.get(word, []):
                doc_scores[doc] += 1

        return doc_scores.most_common()

    def print_search_results(self, query_words: List[str]):
        results = self.search(query_words)
        if not results:
            print("Aucun document ne correspond à la requête.")
            return

        print(f"Résultats pour la requête : {' '.join(query_words)}")
        for doc, score in results:
            print(f"- Document : {doc} | Score de pertinence : {score}")

if __name__ == "__main__":
    indexer = SimpleIndexer()
    files = ['doc1.txt', 'doc2.txt']
    indexer.index_documents(files)

    retriever = DocumentRetriever(indexer)
    query = ['exemple', 'test']
    retriever.print_search_results(query)
