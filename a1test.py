import json
import os
import logging
from dotenv import load_dotenv
from ai71 import AI71

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

AI71_API_KEY = "ai71-api-4b173abc-bb49-4079-8379-31e3a94e5c04"
ai71_client = AI71(AI71_API_KEY)

def generate_meal_plan(description, diet_type, skill_level, length, meal_types):
    logger.info(f"Generating meal plan for: {description}, {diet_type}, {skill_level}, {length}, {meal_types}")

    prompt = f"""
    The user wants a meal plan with the following description: {description}. The user wants it to be for a {diet_type} diet and with a {skill_level} difficulty level for creating the meals. The meal plan should be for {length} days, with each day containing the following meals: {', '.join(meal_types)}. You will generate a one-sentence detailed description for each meal and output it in this JSON structure without any other details or comments:
{{ "mealPlan": {{ "days": [ {{ "date": "provide only number", "meals": {{ "meal_name": "string one sentence detailed description of that meal", "meal_name": "as many meals as provided by the user for one date" }} }} ] }}}}

You MUST ensure that the meals are unique and related to the user's preferences.

Use passive descriptions that do not directly address the user. Provide the general name of the meal along with its details.

Ensure that the meals are unique and tailored to the user's preferences.

Create {length} different days and meals. Be sure to include all {length} meals.
    """

    try:
        response = ai71_client.chat.completions.create(
            model="tiiuae/falcon-180B-chat",
            messages=[
                {"role": "system", "content": "You are a meal plan generator that creates recipe ideas based on the number of days and the number of meals per day, and outputs them in a specific JSON structure. "},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        meal_plan = response.choices[0].message.content.strip()
        logger.info(f"Generated meal plan:\n{meal_plan}")
        
        return {"meal_plan": meal_plan}

    except Exception as e:
        logger.error(f"Error generating meal plan: {str(e)}")
        return {"error": f"Failed to generate meal plan: {str(e)}"}

def test_meal_plan_generation():
    test_input = {
        "description": "Healthy meals for a busy week",
        "dietType": "Vegetarian",
        "skillLevel": "Intermediate",
        "length": "Three Days",
        "mealTypes": ["Breakfast", "Lunch", "Dinner"]
    }

    result = generate_meal_plan(
        test_input["description"],
        test_input["dietType"],
        test_input["skillLevel"],
        test_input["length"],
        test_input["mealTypes"]
    )

    print("Test Input:")
    print(json.dumps(test_input, indent=2))
    print("\nGenerated Meal Plan:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_meal_plan_generation()