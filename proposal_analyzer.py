import os
import PyPDF2
import docx
import nltk
import openai
from typing import Dict, List, Any

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Simplified NLP processing
def extract_key_topics(text: str, top_n: int = 5) -> List[str]:
    """
    Extract key topics using basic text processing
    """
    # Basic word frequency approach
    words = text.lower().split()
    word_freq = {}
    for word in words:
        if len(word) > 3:  # Filter out very short words
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top topics
    return sorted(word_freq, key=word_freq.get, reverse=True)[:top_n]

class ProposalAnalyzer:
    def __init__(self, api_key: str = None):
        """
        Initialize the Proposal Analyzer with optional OpenAI API key
        """
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        self.supported_extensions = ['.pdf', '.docx', '.txt']

    def extract_text(self, filepath: str) -> str:
        """
        Extract text from various file types
        """
        file_ext = os.path.splitext(filepath)[1].lower()
        
        if file_ext not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        if file_ext == '.pdf':
            return self._extract_pdf_text(filepath)
        elif file_ext == '.docx':
            return self._extract_docx_text(filepath)
        elif file_ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()

    def _extract_pdf_text(self, filepath: str) -> str:
        """Extract text from PDF"""
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return ' '.join([page.extract_text() for page in reader.pages])

    def _extract_docx_text(self, filepath: str) -> str:
        """Extract text from DOCX"""
        doc = docx.Document(filepath)
        return ' '.join([para.text for para in doc.paragraphs])

    def analyze_proposal(self, filepath: str) -> Dict[str, Any]:
        """
        Comprehensive proposal analysis
        """
        try:
            text = self.extract_text(filepath)
        except Exception as e:
            return {"error": f"Failed to extract text: {str(e)}"}
        
        # Basic text processing
        key_topics = extract_key_topics(text)
        
        # Optional: Advanced AI-powered analysis
        recommendation = self._get_ai_recommendation(text)
        
        return {
            "raw_text_length": len(text),
            "key_entities": {topic: "Topic" for topic in key_topics},
            "insights": [
                f"Total words: {len(text.split())}",
                f"Key topics detected: {', '.join(key_topics)}"
            ],
            "recommendation": recommendation
        }

    def _get_ai_recommendation(self, text: str) -> str:
        """
        Optional: Use OpenAI for advanced recommendation
        Requires OpenAI API key
        """
        if not self.client:
            return "Advanced AI recommendation not available. Please set OpenAI API key."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert proposal analyst."},
                    {"role": "user", "content": f"Provide a concise recommendation based on this proposal text: {text[:4000]}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI recommendation error: {str(e)}"

# Example usage
if __name__ == "__main__":
    analyzer = ProposalAnalyzer()
    result = analyzer.analyze_proposal("sample_proposal.pdf")
    print(result)
