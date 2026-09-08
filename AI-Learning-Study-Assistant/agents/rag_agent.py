class RAGAgent:
    def __init__(self, retriever):
        self.retriever = retriever

    def get_context(self, question):
        results = self.retriever.search(question, top_k=4)
        if not results:
            return "No course material has been indexed yet."
        return "\n\n---\n\n".join(results)
