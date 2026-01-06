from duckduckgo_search import DDGS
import streamlit as st

class SearchIntegrator:
    def __init__(self):
        self.ddgs = DDGS()

    def perform_search(self, query, max_results=5):
        """إجراء بحث سريع على الإنترنت وجلب النتائج"""
        try:
            results = self.ddgs.text(query, max_results=max_results)
            search_data = ""
            for i, r in enumerate(results):
                search_data += f"\n[{i+1}] Source: {r['title']}\nContent: {r['body']}\nURL: {r['href']}\n"
            return search_data
        except Exception as e:
            print(f"Search Engine Error: {e}")
            return "No live data could be retrieved at this moment."

    def format_search_prompt(self, user_query, search_results):
        """دمج نتائج البحث مع سؤال المستخدم لإرسالها لـ Gemini"""
        prompt = (
            f"You are WORM-GPT with LIVE INTERNET ACCESS. "
            f"Below is the real-time search data from the web for the user's request. "
            f"Use this data to provide an up-to-date and accurate response.\n\n"
            f"SEARCH DATA:\n{search_results}\n\n"
            f"USER QUESTION: {user_query}\n\n"
            f"Provide a technical, detailed response based on this live information."
        )
        return prompt
