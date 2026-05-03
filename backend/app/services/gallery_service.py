import json
import os
from app.utils.logger import get_logger

logger = get_logger(__name__)

class GalleryService:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.skills_path = os.path.join(self.base_dir, "data", "skills.json")
        self.models_path = os.path.join(self.base_dir, "data", "models.json")
        self.skills = []
        self.models = []
        self.load_data()

    def load_data(self):
        """Loads skills and models data from JSON files."""
        try:
            if os.path.exists(self.skills_path):
                with open(self.skills_path, 'r', encoding='utf-8') as f:
                    self.skills = json.load(f)
                logger.info(f"Loaded {len(self.skills)} skills.")
            
            if os.path.exists(self.models_path):
                with open(self.models_path, 'r', encoding='utf-8') as f:
                    self.models = json.load(f)
                logger.info(f"Loaded {len(self.models)} models.")
        except Exception as e:
            logger.error(f"Failed to load gallery data: {e}")

    def get_all_skills(self):
        return self.skills

    def get_all_models(self):
        return self.models

    def find_skill(self, name_query):
        """Finds a skill by name (case-insensitive partial match)."""
        query = name_query.lower()
        for skill in self.skills:
            if query in skill['name'].lower() or query in skill['id'].lower():
                return skill
        return None

    def find_model(self, name_query):
        """Finds a model by name (case-insensitive partial match)."""
        query = name_query.lower()
        for model in self.models:
            if query in model['name'].lower():
                return model
        return None

# Singleton instance
gallery_service = GalleryService()
