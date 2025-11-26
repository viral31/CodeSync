import google.genai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backend directory
load_dotenv()

class AutocompleteService:
    @staticmethod
    def get_suggestion(code: str, cursor_position: int, language: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        
        # Debug: Print full API key
        
        
        # Fallback to mock suggestions if no API key
        if not api_key:
            return AutocompleteService._get_mock_suggestion(code, language)
        
        try:
            client = genai.Client(api_key=api_key)
            
            # Handle empty code
            if not code.strip():
                return "# Start typing..."
            
            system_prompt = "You are a code completion assistant. Only return the next line of code. No explanations, no comments, no markdown formatting. Just the raw code line."
            user_prompt = f"Complete this {language} code:\n{code}\n\nNext line:"
            
            prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt]
            )
            
            suggestion = response.text.strip()
            
            # Clean up the response
            if suggestion.startswith('```'):
                lines = suggestion.split('\n')
                suggestion = '\n'.join(lines[1:-1]) if len(lines) > 2 else suggestion
            
            return suggestion[:100]  # Limit length
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return AutocompleteService._get_mock_suggestion(code, language)
    
    @staticmethod
    def _get_mock_suggestion(code: str, language: str) -> str:
        suggestions = {
            "python": ["def main():", "if __name__ == '__main__':", "import os", "print()"],
            "javascript": ["function main() {", "const result = ", "console.log()", "if (condition) {"]
        }
        
        current_line = code.split('\n')[-1].strip()
        lang_suggestions = suggestions.get(language, suggestions["python"])
        
        if current_line.endswith(':'):
            return "    pass"
        elif 'def ' in current_line:
            return "    return"
        else:
            return lang_suggestions[len(current_line) % len(lang_suggestions)]