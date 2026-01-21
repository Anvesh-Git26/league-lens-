import os
import requests
from langchain_openai import ChatOpenAI

class LiveCommentaryEngine:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

    def generate_commentary(self, match_state: dict):
        """
        Takes live JSON data (e.g., from Kafka or API) and generates spirited commentary.
        """
        prompt = f"""
        You are an excited cricket commentator. 
        Current situation: {match_state['batter']} is on strike. 
        Bowler: {match_state['bowler']}. 
        Outcome: {match_state['outcome']}.
        Generate a 1-sentence commentary line.
        """
        response = self.llm.invoke(prompt)
        return response.content

    def text_to_speech(self, text: str):
        """
        Sends text to ElevenLabs API for audio generation.
        """
        url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM" # Default voice ID
        headers = {
            "xi-api-key": self.elevenlabs_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open("commentary_output.mp3", "wb") as f:
                f.write(response.content)
            return "commentary_output.mp3"
        return None