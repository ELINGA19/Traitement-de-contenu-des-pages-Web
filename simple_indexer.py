from typing import List, Dict, Set
import os
import re

class SimpleIndexer:
    def __init__(self):
        self.index: Dict[str, Set[str]] = {}
        self.documents_lines: Dict[str, List[str]] = {}

    def index_documents(self, docs_paths: List[str], encoding: str = 'utf-8'):
        for path in docs_paths:
            self.index_document(path, encoding)

    def index_document(self, file_path: str, encoding: str = 'utf-8'):
        if not os.path.isfile(file_path):
            return

        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
        except Exception:
            return

        self.documents_lines[file_path] = [line.strip() for line in lines]

        for line in lines:
            clean_line = self._clean_line(line)
            words = clean_line.split()
            for word in words:
                if word not in self.index:
                    self.index[word] = set()
                self.index[word].add(file_path)

    def _clean_line(self, line: str) -> str:
        line = line.lower()
        line = re.sub(r"[^a-z0-9\s]", " ", line)
        line = re.sub(r"\s+", " ", line).strip()
        return line

    def search_word(self, word: str) -> Dict[str, List[int]]:
        word = word.lower()
        result = {}
        if word not in self.index:
            return result

        docs = self.index[word]
        for doc in docs:
            lines = self.documents_lines.get(doc, [])
            line_numbers = []
            for i, line in enumerate(lines, start=1):
                clean_line = self._clean_line(line)
                if word in clean_line.split():
                    line_numbers.append(i)
            result[doc] = line_numbers
        return result

    def print_search_results(self, word: str):
        results = self.search_word(word)
        if not results:
            print(f"Le mot '{word}' n'a été trouvé dans aucun document.")
            return

        print(f"Recherche du mot '{word}':")
        for doc, lines in results.items():
            print(f"- Document: {doc}")
            print(f"  Occurrences aux lignes: {lines}")

if __name__ == "__main__":
    indexer = SimpleIndexer()
    files = ['doc1.txt', 'doc2.txt']
    indexer.index_documents(files)

    mot = 'exemple'
    indexer.print_search_results(mot)
