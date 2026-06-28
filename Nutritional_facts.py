import json
import redis
from log_file import setup_logging
logger = setup_logging('Nutritional_facts')


class NutritionDataManager:
    def __init__(self, host='localhost', port=6379):
        logger.info("Initializing NutritionDataManager")
        self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)

        self.nutrition_data = {
            "Taco": self.default_values(226, 9, 12),
            "Taquito": self.default_values(200, 7, 10),
            "apple_pie": self.default_values(296, 3, 14),
            "burger": self.default_values(295, 17, 13),
            "butter_naan": self.default_values(310, 8, 9),
            "chai": self.default_values(120, 3, 5),
            "chapati": self.default_values(104, 3, 1),
            "cheesecake": self.default_values(321, 6, 22),
            "chicken_curry": self.default_values(240, 18, 15),
            "chole_bhature": self.default_values(427, 12, 20),
            "dal_makhani": self.default_values(330, 14, 18),
            "dhokla": self.default_values(160, 8, 4),
            "fried_rice": self.default_values(250, 6, 9),
            "ice_cream": self.default_values(207, 4, 11),
            "idli": self.default_values(58, 2, 0.4),
            "jalebi": self.default_values(150, 1, 8),
            "kaathi_rolls": self.default_values(350, 15, 18),
            "kadai_paneer": self.default_values(300, 14, 22),
            "kulfi": self.default_values(180, 5, 10),
            "masala_dosa": self.default_values(250, 6, 8),
            "momos": self.default_values(230, 9, 7),
            "omelette": self.default_values(154, 11, 12),
            "paani_puri": self.default_values(180, 4, 6),
            "pakode": self.default_values(312, 6, 20),
            "pav_bhaji": self.default_values(400, 9, 18),
            "pizza": self.default_values(266, 11, 10),
            "samosa": self.default_values(262, 5, 17),
            "sushi": self.default_values(200, 8, 3),
            "Baked Potato": self.default_values(161, 4, 0.2),
            "Crispy Chicken": self.default_values(320, 22, 18),
            "Donut": self.default_values(260, 3, 14),
            "Fries": self.default_values(365, 4, 17),
            "Hot Dog": self.default_values(290, 10, 26),
            "Sandwich": self.default_values(250, 12, 8)
        }
        logger.info("Nutrition data dictionary created successfully")

    def default_values(self, calories, protein, fat):
        logger.debug(f"Generating nutrition values for calories={calories}")
        return {
            "calories": calories,
            "protein_g": protein,
            "fat_g": fat,
            "carbohydrates_g": round(calories * 0.12, 2),
            "fiber_g": round(protein * 0.5, 2),
            "sugar_g": round(calories * 0.05, 2),
            "sodium_mg": round(calories * 2.5, 2),
            "cholesterol_mg": round(fat * 3, 2)
        }

    def save_to_json(self, filename="nutrition.json"):
        try:
            with open(filename, "w") as file:
                json.dump(self.nutrition_data, file, indent=4)
            logger.info("JSON file created successfully")
        except Exception as e:
            logger.error(f"Error saving JSON file: {e}")

    def send_to_redis(self):
        try:
            for food, values in self.nutrition_data.items():
                self.redis_client.set(food, json.dumps(values))
            logger.info("Data sent to Redis successfully")
        except Exception as e:
            logger.error(f"Error sending data to Redis: {e}")


logger.info("Script execution started")

manager = NutritionDataManager()
manager.save_to_json()
manager.send_to_redis()

logger.info("Script execution completed")