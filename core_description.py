import random

# Expanded haircuts for both Male and Female characters (including modern styles and cuts)
hair_male = {
    "short": [
        "Buzz Cut", "Undercut", "Crew Cut", "Faux Hawk", "Slicked Back", "Caesar Cut", "Textured Crop", "Side Part", 
        "Spiky", "Military Cut", "High Fade", "Ivy League", "Pompadour", "Quiff", "Flat Top", "Taper Fade", "Bald Fade",
        "Modern Caesar Cut", "Disconnected Undercut", "Low Fade", "Temple Fade", "Crew Fade", "High and Tight"
    ],
    "medium": [
        "Wavy Fringe", "Side Swept", "Middle Part", "Layered", "Curly Bob", "Messy Waves", "Bro Flow", "Textured Shag", 
        "Modern Mullet", "Shaggy Waves", "Loose Curls", "Undercut with Top Long", "Textured Top with Fade", "Pompadour with Fade"
    ],
    "long": [
        "Man Bun", "Ponytail", "Straight Locks", "Braided", "Dreadlocks", "Half-Up Bun", "Viking Braids", "Shoulder-Length Waves", 
        "Long Shag", "Flowing Locks", "Surfer Hair", "Layered Long Hair", "Top Knot", "Half Up Half Down", "Loose Beach Waves"
    ]
}

hair_female = {
    "short": [
        "Pixie", "Bob", "Lob", "Shaggy Bob", "Buzz Cut", "Asymmetrical Bob", "Sleek Blunt Cut", "Curly Bob", 
        "Boyish Crop", "Layered Pixie", "Undercut Pixie", "Fluffed Up Bob", "Angular Cut", "Choppy Bob", "Modern Pixie Cut",
        "Side Shaved Pixie", "Side Shaved Bob", "Side Shaved Asymmetrical Cut", "Side Shaved Curly Bob",
        "Side Shaved Mohawk", "Side Shaved Fade", "Side Shaved Bob with Undercut", "Side Shaved Pixie with Pompadour",
        "Side Shaved Bob with Textured Top", "Side Shaved Curly Pixie", "Side Shaved Bowl Cut", "Side Shaved Tapered Cut",
        "Side Shaved Messy Bob", "Side Shaved Fauxhawk", "Side Shaved Asymmetrical Bob with Long Fringe",
        "Side Shaved High Fade Pixie"
    ],
    "medium": [
        "Shoulder-Length Waves", "Wavy Lob", "Textured Layers", "Curtain Bangs", "Side Swept Bangs", "Crimped", 
        "Medium Shag", "Vintage Waves", "Feathered Layers", "Straight Lob", "Half-Updo", "Soft Razored Layers", "Messy Lob",
        "Side Shaved Medium Cut", "Side Shaved Wavy Lob", "Side Shaved Layered Hair",
        "Side Shaved Lob with Curls", "Side Shaved Layered Pixie Cut", "Side Shaved Textured Lob", "Side Shaved Blunt Cut",
        "Side Shaved Wavy Bob", "Side Shaved Undercut Lob", "Side Shaved Curly Lob", "Side Shaved Bob with Layers",
        "Side Shaved Messy Curls", "Side Shaved Choppy Bob", "Side Shaved Curly Shag", "Side Shaved Vintage Waves with Fade"
    ],
    "long": [
        "Mermaid Waves", "Straight Layers", "Voluminous Curls", "French Braid", "Fishtail Braid", "Crown Braid", "Twisted Bun", 
        "Side Ponytail", "High Ponytail", "Twin Tails", "Flowing Locks", "Loose Ringlets", "Bubble Braid", "Waterfall Braid", 
        "Braided Bun", "Layered Curls", "Spiral Curls", "Glam Waves", "Bohemian Waves", "Loose Curls with a Middle Part",
        "Side Shaved Long Hair", "Side Shaved Layered Locks",
        "Side Shaved Long Textured Hair", "Side Shaved Straight Long Hair", "Side Shaved Mermaid Waves with Undercut",
        "Side Shaved Layered Waves", "Side Shaved Long Curly Hair", "Side Shaved Long Wavy Locks", "Side Shaved Long Bob with Layers",
        "Side Shaved Braided Long Hair", "Side Shaved Long Pixie with Curls", "Side Shaved Ponytail with Undercut",
        "Side Shaved Long Curly Beach Waves", "Side Shaved Glamorous Waves"
    ]
}

# Expanded eye colors and other features
eye_colors = {
    "natural": ["Brown", "Blue", "Green", "Hazel", "Gray", "Amber"],
    "fantasy": ["Gold", "Silver", "Crimson", "Purple", "Turquoise", "Heterochromatic", "Gradient (Blue-to-Green)", "Glowing"]
}

skin_tones = ["Porcelain", "Ivory", "Fair", "Olive", "Bronze", "Caramel", "Tawny", "Chocolate", "Ebony"]
accessories = ["Glasses", "Sunglasses", "Earrings", "Necklaces", "Chokers", "Bracelets", "Gloves", "Scarves", "Belts", "Brooches", "Rings", "Crowns", "Tiaras", "Watches", "Goggles", "Amulets", "Masks"]

# Expanded body parts and body details (height, physique, etc.)
body_parts_male = {
    "Head": ["Strong Jawline", "Square Jaw", "Sharp Features", "High Cheekbones", "Facial Hair", "Beard", "Clean-shaven"],
    "Torso": ["Broad Chest", "V-shaped Torso", "Defined Abs", "Muscular Back", "Flat Stomach", "Chest Hair", "Toned Arms"],
    "Arms": ["Muscular Biceps", "Toned Forearms", "Veiny Arms", "Fur-covered Arms"],
    "Legs": ["Long Legs", "Thick Thighs", "Slim Legs", "Athletic Legs", "Hairy Legs"],
    "Hands": ["Large Hands", "Rough Hands", "Well-groomed Nails", "Scarred Hands"],
    "Feet": ["Big Feet", "Large Toes", "Calloused Soles"],
    "Neck": ["Thick Neck", "Defined Neck", "Tattoos", "Neck Chains"],
    "Waist": ["Slim Waist", "Muscular Waist", "V-shaped Waist"],
    "Chest": ["Broad Chest", "Chiseled Chest", "Hairless Chest"],
    "Back": ["Toned Back", "Wide Back", "Tattooed Back"],
    "Shoulders": ["Wide Shoulders", "Athletic Shoulders", "Broad Shoulders"]
}

body_parts_female = {
    "Head": ["Soft Jawline", "Round Face", "High Cheekbones", "Delicate Features", "Full Lips", "Dimpled Chin", "Clear Skin"],
    "Torso": ["Hourglass Figure", "Slim Waist", "Curvy Torso", "Flat Stomach", "Busty", "Sculpted Shoulders"],
    "Arms": ["Slim Arms", "Toned Arms", "Long Arms", "Delicate Hands", "Soft Skin", "Tattooed Arms"],
    "Legs": ["Long Legs", "Slim Legs", "Curvy Legs", "Athletic Legs", "Toned Thighs", "Hairless Legs"],
    "Hands": ["Delicate Hands", "Well-groomed Nails", "Small Hands", "Soft Hands"],
    "Feet": ["Small Feet", "Soft Soles", "Well-manicured Toes"],
    "Neck": ["Graceful Neck", "Delicate Neck", "Tattooed Neck", "Necklaces"],
    "Waist": ["Small Waist", "Curvy Waist", "Narrow Waist", "Toned Waist"],
    "Chest": ["Full Bust", "Small Bust", "Busty", "Perky Breasts"],
    "Back": ["Graceful Back", "Toned Back", "Small of Back", "Tattooed Back"],
    "Shoulders": ["Delicate Shoulders", "Soft Shoulders", "Athletic Shoulders"]
}

# Expanded poses and body details
poses = ["Standing with Hands on Hips", "Crossed Arms", "One Hand in Pocket", "Leaning Against Wall", "Stretching", 
         "Arms Raised", "Holding Object", "Sitting Cross-legged", "Leaning on Elbow", "Dynamic Running Pose", 
         "Twisting Mid-air", "Jumping", "Spinning Weapon", "Punching", "Dancing", "Flying", "Crying", "Laughing", 
         "Sitting on Ground", "Lying Down", "Resting on Knees"]

# Function to generate a random core description based on a user's prompt
def generate_core_description(prompt=""):
    # Default gender is chosen if no specific prompt is given, otherwise determine gender from the prompt
    gender = "female" if "female" in prompt.lower() else "male"

    # Randomly select the hair style based on the gender and hair length mentioned
    hair_length = "long" if "long" in prompt.lower() else "medium" if "medium" in prompt.lower() else "short"
    hair_style = random.choice(hair_female[hair_length]) if gender == "female" else random.choice(hair_male[hair_length])

    # Randomly choose the other features
    eye_color = random.choice(eye_colors["natural"])
    skin_tone = random.choice(skin_tones)
    clothing_style = random.choice(
        ["Hoodie", "T-shirt", "Jeans", "Bomber Jacket", "Leather Jacket", "Suit", "Tank Top"] if gender == "male" 
        else ["Crop Top", "Blazer", "High-waisted Skirt", "Jumpsuit", "Sundress", "Oversized Sweater", "Leggings", "Denim Jacket"]
    )
    accessory = random.choice(accessories)
    pose = random.choice(poses)
    expression = random.choice(["Happy", "Angry", "Sad", "Surprised", "Smirking", "Mischievous", "Blushing", "Crying", "Determined", "Confident", "Dreamy", "Melancholy", "Shocked"])
    body_part = random.choice(list(body_parts_male.keys()) if gender == "male" else list(body_parts_female.keys()))
    body_detail = random.choice(body_parts_male[body_part] if gender == "male" else body_parts_female[body_part])
    theme = random.choice(["Fantasy", "Gothic", "Steampunk", "Cyberpunk", "Sci-Fi", "Medieval", "Urban", "Nature", "Post-apocalyptic"])

    # Return the generated description
    description = {
        "Gender": gender,
        "Hair Style": hair_style,
        "Eye Color": eye_color,
        "Skin Tone": skin_tone,
        "Clothing": clothing_style,
        "Accessories": accessory,
        "Pose": pose,
        "Expression": expression,
        "Body Part Detail": body_detail,
        "Theme": theme
    }

    return description
