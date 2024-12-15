import random

# Importing the core description function from description.py (as assumed to be in the same directory)
from description import generate_core_description

def prompt_check(user_prompt):
    # Check for missing details in the user's prompt
    required_details = ["gender", "hair", "eye color", "skin tone", "clothing", "accessory", "pose", "expression", "body part", "theme"]
    
    # Initialize the missing details
    missing_details = []

    # Check which details are missing in the user's prompt
    user_prompt_lower = user_prompt.lower()

    # For each required detail, check if it's in the user's prompt
    for detail in required_details:
        if detail not in user_prompt_lower:
            missing_details.append(detail)
    
    # If there are missing details, add them from the core description
    if missing_details:
        print(f"Missing details: {missing_details}")
        
        # Generate a core description to fill the missing details
        core_description = generate_core_description(user_prompt)

        # Add missing details from the core description
        for missing in missing_details:
            if missing == "gender" and "female" not in user_prompt_lower and "male" not in user_prompt_lower:
                user_prompt += f" gender: {core_description['Gender']}"
            elif missing == "hair" and "hair" not in user_prompt_lower:
                user_prompt += f" hair: {core_description['Hair Style']}"
            elif missing == "eye color" and "eye" not in user_prompt_lower:
                user_prompt += f" eye color: {core_description['Eye Color']}"
            elif missing == "skin tone" and "skin tone" not in user_prompt_lower:
                user_prompt += f" skin tone: {core_description['Skin Tone']}"
            elif missing == "clothing" and "clothing" not in user_prompt_lower:
                user_prompt += f" clothing: {core_description['Clothing']}"
            elif missing == "accessory" and "accessory" not in user_prompt_lower:
                user_prompt += f" accessory: {core_description['Accessories']}"
            elif missing == "pose" and "pose" not in user_prompt_lower:
                user_prompt += f" pose: {core_description['Pose']}"
            elif missing == "expression" and "expression" not in user_prompt_lower:
                user_prompt += f" expression: {core_description['Expression']}"
            elif missing == "body part" and "body part" not in user_prompt_lower:
                user_prompt += f" body part: {core_description['Body Part Detail']}"
            elif missing == "theme" and "theme" not in user_prompt_lower:
                user_prompt += f" theme: {core_description['Theme']}"
        
        print(f"Updated user prompt: {user_prompt}")
        return user_prompt
    else:
        print("No details missing. The user prompt is complete.")
        return user_prompt


# Example usage of the prompt_check function:
user_input = "I want a female character with wavy hair, blue eyes, and a trendy outfit."
updated_prompt = prompt_check(user_input)
print(updated_prompt)
