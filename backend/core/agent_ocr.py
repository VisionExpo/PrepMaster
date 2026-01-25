import os
import json
import yaml
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ResumeParser:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash", # Using the fast model you found
            generation_config={"response_mime_type": "application/json"}
        )
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        """Helper to load the YAML config"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(base_dir, "..", "config", "prompts.yaml")
        with open(yaml_path, "r") as f:
            return yaml.safe_load(f)

    def parse(self, file_path):
        print(f"📄 Uploading to Gemini: {file_path}...")
        uploaded_file = genai.upload_file(file_path)

        # LOAD PROMPT FROM YAML
        prompt = self.prompts["system_prompts"]["resume_parser"]

        print("🤖 Analyzing document...")
        response = self.model.generate_content([prompt, uploaded_file])
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            print("⚠️ Error: Gemini returned invalid JSON.")
            return {}