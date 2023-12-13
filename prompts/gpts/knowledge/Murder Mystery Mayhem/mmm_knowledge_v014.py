import random
import re
import json
import itertools
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import zipfile
import io
from PIL import Image

game_state = {}


#Characters
characters = {
    "The Aristocrat": "Lady Agatha Harrington - The wealthy, sophisticated matriarch of the family, often hosting lavish events at her opulent estate.",
    "The Butler": "Barnaby Wadsworth - The loyal and discreet servant, always attending to the needs of the household with a keen eye for detail.",
    "The Gardener": "Hazel Thorne - The quiet and skilled horticulturist, tending to the lush grounds and gardens, often harboring a secret or two.",
    "The Socialite": "Felicity Devereux - The charming and glamorous party-goer, always seeking attention and eager to share the latest gossip.",
    "The Mysterious Stranger": "Sebastian Blackwood - The enigmatic and alluring outsider, arriving with an air of secrecy and capturing the curiosity of those around them.",
    "The Heir": "Cassandra Worthington - The privileged and often naive young scion, set to inherit the family fortune, but grappling with the responsibilities and expectations that come with it.",
    "The Eccentric Inventor": "Algernon Pembleton - The quirky and brilliant mind, constantly tinkering with bizarre gadgets and inventions, sometimes to the detriment of those around them.",
    "The Disgraced Doctor": "Dr. Lucius Grimshaw - The once-renowned physician, fallen from grace and seeking redemption, haunted by a dark past.",
    "The Retired Colonel": "Col. Percival Montgomery - The stern and disciplined military man, upholding order and decorum, while hiding a softer side beneath his gruff exterior.",
    "The Fortune Teller": "Madame Mystique - The enigmatic and captivating clairvoyant, offering insights into the unknown and revealing hidden truths, while shrouded in an aura of mystery.",
    "The Magician": "Maximillian DeLune - The charismatic and skilled illusionist, enthralling the audience with his mesmerizing tricks and deft sleight of hand, always concealing his true intentions."
}

#Directions for roleplay
#Directions for roleplay
roleplay_directions = {
  "The Aristocrat": "Speak elegantly, with pride in your heritage. Share high society anecdotes and insights with a polite yet assertive tone.",
  "The Butler": "Remain formal and respectful. Offer observations about the household and its members, speaking precisely.",
  "The Gardener": "Speak calmly about your gardening passion. Share observations from the gardens and interesting plant facts.",
  "The Socialite": "Be flirtatious and confident. Share gossip, aiming to charm the detective and mention your social connections.",
  "The Mysterious Stranger": "Speak cryptically, hinting at secrets. Respond with riddles and offer intriguing puzzles to the detective.",
  "The Heir": "Speak with youthful innocence, sharing dreams and seeking advice on your future responsibilities.",
  "The Eccentric Inventor": "Talk enthusiastically about inventions and ideas. Share quirky anecdotes and display your latest creation.",
  "The Disgraced Doctor": "Speak somberly, being cautious about your past. Offer medical insights and express a desire for redemption.",
  "The Retired Colonel": "Command authority in your tone, sharing military stories and upholding discipline. Show occasional vulnerability.",
  "The Fortune Teller": "Use a mysterious tone, offering fortunes. Use dramatic gestures and hint at personal and others' secrets.",
  "The Magician": "Be theatrical and playful. Perform small tricks, hint at their secrets, and entertain with magic."
}

#Locations
locations = {
    "The Grand Hall": "A spacious area for large gatherings",
    "The Library": "A quiet place filled with books and knowledge",
    "The Dining Room": "A large room for enjoying exquisite meals",
    "The Ballroom": "An extravagant room for dancing and socializing",
    "The Bedrooms": "Additional cozy chambers for a good night's rest",
    "The Servant’s Quarters": "Modest living quarters for the household staff",
    "The Gardens": "Manicured lawns and picturesque flower beds",
    "The Entrance Hall": "A grand entryway to welcome esteemed guests",
    "The Study": "A private workspace filled with intellectual pursuits",
    "The Drawing Room": "An elegant room for leisurely conversation",
    "The Billiard Room": "A competitive setting for billiards and camaraderie",
    "The Stables": "Well-kept stables for housing horses",
    "The Lounge": "A comfortable room to relax and socialize",
    "The Conservatory": "A lush, green sanctuary for plants and relaxation",
    "The Kitchen": "A bustling hub of culinary creation",
    "The Guest Rooms": "Inviting accommodations for overnight visitors",
    "The Boathouse": "A charming building for storing boats and watercraft",
}

ex_clues = {
"Ask the housekeeper": "Witness saw them elsewhere",
"Search victim's belongings": "Records of longstanding friendship",
"Dust crime scene for prints": "No evidence was found at the crime scene",
"Ask the groundskeeper": "They were seen far away from the crime scene",
"Examine call log": "They made a phone call during the crime",
"Ask the maid": "They were being attended around the time of the crime",
"Review telegram records": "They sent a telegram at the time of the murder",
"Inspect gift records": "They recently sent a thoughtful gift to the victim",
"Review financial records": "They paid off a debt to the victim before the murder",
"Examine correspondence": "They had a cordial relationship with the victim",
"Investigate personal effects": "Their belongings show no signs of involvement",
"Examine luggage": "Their clothes have no traces of blood or evidence",
"Review guest interactions": "They had only positive interactions with the victim",
"Inspect medical records": "They recently helped the victim with a medical issue",
"Check newspaper archives": "They collaborated with the victim on a charity event",
"Examine social circles": "They shared many mutual friends with the victim"
}

inc_clues = {
"Search victim's belongings": "Suspicious message to the victim",
"Review guest interactions": "Argued with the victim",
"Dust crime scene for prints": "Fingerprints at crime scene",
"Ask the bartender": "They were drinking heavily before the murder",
"Investigate victim's clothes": "Their lighter found near the body",
"Inspect crime scene": "Their personal item found at the crime scene",
"Review financial records": "They owed victim a large sum of money",
"Investigate luggage": "Their clothes found with bloodstains",
"Check the mail": "They received a threatening letter from the victim",
"Ask the housekeeper": "They had a heated argument with the victim recently",
"Examine correspondence": "Their typed note was found threatening the victim",
"Investigate secret passages": "They were seen entering a secret passage near the crime scene",
"Examine call log": "They had a suspicious call with the victim before the murder",
"Examine social circles": "They had a long-standing feud",
"Analyze handwriting": "Their handwriting matches a threatening note to the victim"
}

#Motives
strong_motives = [
    "Blackmail threat", "Romantic jealousy", "Revenge for past betrayal", "Covering up a crime", "Stopping a scandal", "Protecting family secrets", "Eliminating a political rival", "Greed for a valuable item", "Sabotaging a competitor", "Seizing power", "Avenging a loved one", "Hiding a secret identity", "Suppressing evidence", "Eliminating a threat", "Desperation for financial gain"
]

weak_motives = [
    "Petty argument", "Social embarrassment", "Small misunderstanding", "Lost a minor bet", "Minor Property damage", "Small debt owed", "Professional jealousy", "Disagreement over taste", "Criticism of fashion", "Academic rivalry", "Gossip spread", "Neighboring dispute", "Sports team rivalry", "Trespassing on property", "Prank gone wrong"
]

#Functions
def initialize_game_state():
    global game_state

    # Create a temporary copy of characters dictionary
    temp_characters = characters.copy()

    # Randomly select murderer, victim, and other guests
    murderer_key = random.choice(list(temp_characters.keys()))
    murderer = temp_characters[murderer_key]
    del temp_characters[murderer_key]

    victim_key = random.choice(list(temp_characters.keys()))
    victim = temp_characters[victim_key]
    del temp_characters[victim_key]

    # Update the number of other guests to 4 (total guests including murderer is 5)
    other_guests_keys = random.sample(list(temp_characters.keys()), 4)
    other_guests = [temp_characters[key] for key in other_guests_keys]

    # Assign alibis
    non_murderer_guest_keys = [key for key in other_guests_keys]
    true_alibi_keys = random.sample(non_murderer_guest_keys, 2)  # Select two guests for a true alibi

    # Assign no alibi to remaining guests
    no_alibi_keys = [key for key in non_murderer_guest_keys if key not in true_alibi_keys]

    # The murderer always has no alibi
    no_alibi_keys.append(murderer_key)

    # Update all_characters to include only characters in play, excluding the victim
    all_characters = [murderer_key] + other_guests_keys



    # Assign motives, excluding the victim
    character_motives = {}

    # Assign strong motive to the murderer
    character_motives[murderer_key] = random.choice(strong_motives)
    strong_motives.remove(character_motives[murderer_key])

    # Assign strong and weak motives for true alibi characters
    character_motives[true_alibi_keys[0]] = random.choice(strong_motives)
    strong_motives.remove(character_motives[true_alibi_keys[0]])

    character_motives[true_alibi_keys[1]] = random.choice(weak_motives)
    weak_motives.remove(character_motives[true_alibi_keys[1]])

    # Assign strong and weak motives for fake alibi/no alibi characters
    remaining_characters = list(set(all_characters) - set(true_alibi_keys) - {murderer_key})
    random.shuffle(remaining_characters)

    character_motives[remaining_characters[0]] = random.choice(strong_motives)
    strong_motives.remove(character_motives[remaining_characters[0]])

    character_motives[remaining_characters[1]] = random.choice(weak_motives)
    weak_motives.remove(character_motives[remaining_characters[1]])

    # Create a list of characters with no alibi or fake alibi and strong motives
    fake_alibi_no_alibi_strong_motive_keys = [key for key, motive in character_motives.items() if motive in strong_motives and key != murderer_key]

    motive_knowledge = {}

    # Create a list of all characters
    all_characters_list = list(all_characters)

    # Rotate the list of all characters to the right by one
    rotated_characters = all_characters_list[-1:] + all_characters_list[:-1]

    # Pair each character in the original list with the next two characters in the rotated list
    # Pair each character in the original list with two other characters, ensuring they do not get their own motive
    for i, char_key in enumerate(all_characters_list):
        # Determine the indices for two characters who are not the current character
        first_index = (i + 1) % len(all_characters_list)
        second_index = (i + 2) % len(all_characters_list)

        motive_knowledge[char_key] = {
            all_characters_list[first_index]: character_motives[all_characters_list[first_index]],
            all_characters_list[second_index]: character_motives[all_characters_list[second_index]],
        }



    # Assign clues
    # Assign incriminating clue to the murderer
    inc_clue_keys = [murderer_key]

    # Assign exonerating clue to the 2nd most suspicious guest with a fake/no alibi and a strong motive
    ex_clue_keys = [key for key in fake_alibi_no_alibi_strong_motive_keys if key != murderer_key]

    # Assign clues for the remaining guests
    remaining_keys = [key for key in all_characters if key not in inc_clue_keys + ex_clue_keys]
    clue_keys = inc_clue_keys + ex_clue_keys + remaining_keys

    character_clues = {}

    for char_key in inc_clue_keys:
        selected_clue_key = random.choice(list(inc_clues.keys()))
        character_clues[char_key] = {selected_clue_key: inc_clues[selected_clue_key]}
        del inc_clues[selected_clue_key]

    for char_key in ex_clue_keys:
        selected_clue_key = random.choice(list(ex_clues.keys()))
        character_clues[char_key] = {selected_clue_key: ex_clues[selected_clue_key]}
        del ex_clues[selected_clue_key]

    for char_key in remaining_keys:
        if random.choice([True, False]):
            selected_clue_key = random.choice(list(inc_clues.keys()))
            character_clues[char_key] = {selected_clue_key: inc_clues[selected_clue_key]}
            del inc_clues[selected_clue_key]
        else:
            selected_clue_key = random.choice(list(ex_clues.keys()))
            character_clues[char_key] = {selected_clue_key: ex_clues[selected_clue_key]}
            del ex_clues[selected_clue_key]

    # Assign clue knowledge
    clue_knowledge = {char: {} for char in all_characters}
    shuffled_characters = all_characters.copy()
    random.shuffle(shuffled_characters)

    # Creating the new dictionaries
    guest_descriptions = {}
    guest_roleplay = {}

    for character in shuffled_characters:
        guest_descriptions[character] = characters[character]
        guest_roleplay[character] = roleplay_directions[character]

    for idx, char_key in enumerate(shuffled_characters):
        clue_receiver = shuffled_characters[(idx + 1) % len(shuffled_characters)]
        clue_knowledge[clue_receiver] = {char_key: character_clues[char_key]}

    game_state["clue_knowledge"] = clue_knowledge

    # Randomly select a location from locations
    location_dict = random.choice(list(locations.values()))

    # Look up the corresponding key in locations
    location = list(locations.keys())[list(locations.values()).index(location_dict)]

    game_state = {
        "murderer": murderer_key,
        "victim": victim_key,
        "all_guests": shuffled_characters,
        "other_guests": other_guests_keys,
        "true_alibi": (true_alibi_keys[0], true_alibi_keys[1]),
        "no_alibi": no_alibi_keys,
        "character_motives": character_motives,
        "motive_knowledge": motive_knowledge,
        "clues": character_clues,
        "clue_knowledge": clue_knowledge,
        "location": location,
        "guest_descriptions": guest_descriptions,
        "guest_roleplay": guest_roleplay,
    }

    return game_state

def show_characters():
    # Open the zip file
    with zipfile.ZipFile("/mnt/data/characters.zip", "r") as characters_zip:
        # Create a 2x3 grid of subplots with black background and no axis number values
        fig, axes = plt.subplots(2, 3, figsize=(10, 6), facecolor='black')

        # Set the first subplot (0, 0) to display "The Detective.jpg"
        detective_image_path = "The Detective.jpg"
        with characters_zip.open(detective_image_path) as file:
            detective_image = Image.open(io.BytesIO(file.read()))
        axes[0, 0].imshow(detective_image)
        axes[0, 0].set_title("The Detective", color='white')
        axes[0, 0].axis('off')

        # Loop through the remaining subplots
        for i in range(2):
            for j in range(3):
                # Skip the first subplot, as it's already occupied by the detective
                if i == 0 and j == 0:
                    continue

                # Get the character name from the "all_guests" list
                character_name = game_state["all_guests"].pop(0)

                # Create the image path for the character
                character_image_path = f"{character_name}.jpg"
                with characters_zip.open(character_image_path) as file:
                    character_image_data = file.read()

                # Display the character image using PIL (Pillow)
                character_image = Image.open(io.BytesIO(character_image_data))
                axes[i, j].imshow(character_image)
                axes[i, j].set_title(character_name, color='white')
                axes[i, j].axis('off')

        # Adjust layout and display the grid of images
        plt.tight_layout()
        plt.show()

def show_character(character_name):
    # Path to the zip file containing character images
    zip_file_path = '/mnt/data/characters.zip'

    # Open the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as characters_zip:
        # Construct the file name for the character image
        character_image_file = f"{character_name}.jpg"

        # Check if the file exists in the zip
        if character_image_file in characters_zip.namelist():
            # Read the image file
            with characters_zip.open(character_image_file) as file:
                character_image = Image.open(io.BytesIO(file.read()))

            # Get the size of the image
            width, height = character_image.size

            # Adjust the size for display, assuming 165 dpi
            fig_width, fig_height = width / 165, height / 165

            # Create a figure with a size that matches the image
            fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='black')

            # Adjust padding and title font size
            plt.subplots_adjust(top=0.85, bottom=0.15, left=0.15, right=0.85)
            ax.set_title(character_name, color='white', fontsize=10)  # Adjust font size as needed

            # Display the image
            ax.imshow(character_image)
            ax.axis('off')  # Hide the axis

            # Display the image
            plt.show()
        else:
            print(f"Image for '{character_name}' not found in the zip file.")
            
def show_location(location_name):
    # Path to the zip file containing location images
    zip_file_path = '/mnt/data/locations.zip'

    # Open the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as locations_zip:
        # Construct the file name for the location image
        location_image_file = f"{location_name}.jpg"

        # Check if the file exists in the zip
        if location_image_file in locations_zip.namelist():
            # Read the image file
            with locations_zip.open(location_image_file) as file:
                location_image = Image.open(io.BytesIO(file.read()))

            # Get the size of the image
            width, height = location_image.size

            # Adjust the size for display, assuming 165 dpi
            fig_width, fig_height = width / 165, height / 165

            # Create a figure with a size that matches the image
            fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='black')

            # Adjust padding and title font size
            plt.subplots_adjust(top=0.85, bottom=0.15, left=0.15, right=0.85)
            ax.set_title(location_name, color='white', fontsize=10)  # Adjust font size as needed

            # Display the image
            ax.imshow(location_image)
            ax.axis('off')  # Hide the axis

            # Display the image
            plt.show()
        else:
            print(f"Image for '{location_name}' not found in the zip file.")            

# Example usage
#display_character("The Socialite")