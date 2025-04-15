"""
Google Gemini API client for LLM Chat Indexer.
"""

from typing import Dict, Any, List, Optional, Union

import google.generativeai as genai

from config.settings import GEMINI_API_KEY


class GeminiClient:
    """
    Client for interacting with Google's Gemini API.
    """
    
    def __init__(self, api_key: str = GEMINI_API_KEY, model_name: str = "gemini-pro"):
        """
        Initialize the Gemini client with API key and model.
        
        Args:
            api_key (str): The Gemini API key.
            model_name (str): The Gemini model to use.
            
        Raises:
            ValueError: If the API key is not provided.
        """
        if not api_key:
            raise ValueError("Gemini API key is required. Set it in the .env file.")
        
        self.api_key = api_key
        self.model_name = model_name
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Get the model
        self.model = genai.GenerativeModel(model_name)
    
    def generate_text(self, prompt: str, temperature: float = 0.7, 
                     max_tokens: Optional[int] = None) -> str:
        """
        Generate text using the Gemini API.
        
        Args:
            prompt (str): The prompt to send to the model.
            temperature (float): Controls randomness in generation (0.0 to 1.0).
            max_tokens (Optional[int]): Maximum number of tokens to generate.
            
        Returns:
            str: The generated text.
            
        Raises:
            Exception: If there's an error in the API call.
        """
        try:
            generation_config = {
                "temperature": temperature,
            }
            
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Error generating text with Gemini: {str(e)}")
    
    def generate_summary(self, text: str, summary_type: str = "gist", 
                        temperature: float = 0.3) -> str:
        """
        Generate a summary of the provided text.
        
        Args:
            text (str): The text to summarize.
            summary_type (str): Type of summary to generate ('gist' or 'key_points').
            temperature (float): Controls randomness in generation.
            
        Returns:
            str: The generated summary.
        """
        if summary_type == "gist":
            prompt = (
                "Please provide a concise summary of the following conversation. "
                "Focus on the main topics discussed and the overall context. "
                "Keep the summary brief (2-3 sentences).\n\n"
                f"Conversation:\n{text}"
            )
        elif summary_type == "key_points":
            prompt = (
                "Extract the key points from the following conversation. "
                "Format your response as a bullet-point list of the most important information, "
                "insights, or decisions. Focus on substance, not conversation flow.\n\n"
                f"Conversation:\n{text}"
            )
        else:
            prompt = (
                f"Summarize the following conversation in the style of {summary_type}:\n\n"
                f"Conversation:\n{text}"
            )
        
        return self.generate_text(prompt, temperature=temperature)
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities from the provided text using Gemini.
        
        Args:
            text (str): The text to extract entities from.
            
        Returns:
            List[Dict[str, Any]]: List of extracted entities with their types.
        """
        prompt = (
            "Extract the key entities from the following text. "
            "For each entity, provide its type (person, organization, location, concept, etc.) "
            "and any relevant attributes. Format your response as a JSON array of objects, "
            "where each object has 'entity', 'type', and 'attributes' fields.\n\n"
            f"Text:\n{text}"
        )
        
        response = self.generate_text(prompt, temperature=0.2)
        
        # Note: In a real implementation, you would parse the JSON response
        # Here we're returning the raw text as the parsing would depend on the actual response format
        return response
