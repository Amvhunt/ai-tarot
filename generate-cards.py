import base64
from openai import OpenAI
import os
import argparse

style = "Ace of Wands, mystical tarot card, detailed, high resolution"
quality = "high"
output_dir = "generated-cards"

CARDS = [
  {
    "number": 0,
    "name": "The Fool",
    "description": "A youth with a knapsack on a staff stepping at the edge of a cliff, with a small dog beside him",
    "meaning": "The beginning of a journey, spontaneity, freedom"
  },
  {
    "number": 1,
    "name": "The Magician",
    "description": "A figure stands behind a table with symbols of the four elements, staff raised upwards",
    "meaning": "Willpower, skill, manifestation of power"
  },
  {
    "number": 2,
    "name": "The High Priestess",
    "description": "A woman sits between two pillars with a book on her lap, a crescent at her feet",
    "meaning": "Intuition, hidden knowledge, sacred wisdom"
  },
  {
    "number": 3,
    "name": "The Empress",
    "description": "A wealthy woman surrounded by fertile fields and forests, wearing a crown of stars",
    "meaning": "Fertility, creativity, maternal care"
  },
  {
    "number": 4,
    "name": "The Emperor",
    "description": "A powerful man on a stone throne with symbols of authority",
    "meaning": "Structure, order, stability"
  },
  {
    "number": 5,
    "name": "The Hierophant",
    "description": "A spiritual mentor in robes between two acolytes",
    "meaning": "Tradition, teaching, spiritual values"
  },
  {
    "number": 6,
    "name": "The Lovers",
    "description": "A pair stands in a tranquil garden, bathed in a gentle celestial glow that symbolizes their unity",
    "meaning": "Love, choice, harmony"
  },
  {
    "number": 7,
    "name": "The Chariot",
    "description": "A warrior in a chariot drawn by sphinxes",
    "meaning": "Control, victory, determination"
  },
  {
    "number": 8,
    "name": "Strength",
    "description": "A woman gently tames a lion",
    "meaning": "Inner strength, patience, courage"
  },
  {
    "number": 9,
    "name": "The Hermit",
    "description": "An old man with a lantern and staff walks through the mountains",
    "meaning": "Solitude, search for truth, wisdom"
  },
  {
    "number": 10,
    "name": "Wheel of Fortune",
    "description": "A rotating wheel with the letters T-A-R-O and creatures at its edges",
    "meaning": "Fate, change, cycles"
  },
  {
    "number": 11,
    "name": "Justice",
    "description": "A woman holding a sword and scales, seated on a throne",
    "meaning": "Balance, responsibility, fairness"
  },
  {
    "number": 12,
    "name": "The Suspension",
    "description": "A calm individual is shown effortlessly resting in mid-air, supported by one leg from a smooth horizontal structure. Their other leg is bent, arms at ease, eyes softly focused downward in deep thought.",
    "meaning": "Shift in perception, conscious pause, exploring new perspectives"
  },
  {
    "number": 13,
    "name": "Death",
    "description": "A skeleton on a horse enters a crowd, people falling around",
    "meaning": "Ending, transformation, new beginning"
  },
  {
    "number": 14,
    "name": "Temperance",
    "description": "An angel pours water from one cup into another",
    "meaning": "Balance, moderation, harmony"
  },
  {
    "number": 15,
    "name": "The Tempter",
    "description": "A tall, enigmatic figure with subtle horns stands behind two individuals subtly bound by glowing threads, their expressions a mix of curiosity and unease",
    "meaning": "Illusion of control, allure of desire, facing one's inner patterns"
  },
  {
    "number": 16,
    "name": "The Tower",
    "description": "A tower struck by lightning, collapsing with people falling",
    "meaning": "Upheaval, shock, liberation"
  },
  {
    "number": 17,
    "name": "The Star",
    "description": "A serene figure kneels near a tranquil pool, gently guiding streams of water as a radiant star shines above, illuminating the calm night",
    "meaning": "Renewed hope, inner clarity, spiritual inspiration"
  },
  {
    "number": 18,
    "name": "The Moon",
    "description": "A path between two towers under a moon with a face",
    "meaning": "Illusion, subconscious, intuition"
  },
  {
    "number": 19,
    "name": "The Sun",
    "description": "Two children dancing under a bright sun and sunflowers",
    "meaning": "Joy, success, enlightenment"
  },
  {
    "number": 20,
    "name": "Judgment",
    "description": "An angel blows a trumpet, the dead rising from graves",
    "meaning": "Rebirth, outcome, call to action"
  },
  {
    "number": 21,
    "name": "The World",
    "description": "A harmonious figure in motion stands within a circular frame of greenery, encircled by emblems representing the four universal forces",
    "meaning": "Completion, wholeness, fulfillment"
  },
  {
    "number": 1,
    "name": "Ace of Wands",
    "description": "A hand out of a cloud holds a blossoming wand",
    "meaning": "New beginnings, inspiration, potential"
  },
  {
    "number": 2,
    "name": "Two of Wands",
    "description": "A person holds a globe while leaning on a wand",
    "meaning": "Planning, decisions, first steps"
  },
  {
    "number": 3,
    "name": "Three of Wands",
    "description": "A figure on a cliff looking at ships in the distance",
    "meaning": "Waiting for results, expansion of horizons"
  },
  {
    "number": 4,
    "name": "Four of Wands",
    "description": "Two wands tied with a wreath under an arch",
    "meaning": "Celebration, stability, home"
  },
  {
    "number": 5,
    "name": "Five of Wands",
    "description": "Five youths brandishing wands compete with each other",
    "meaning": "Conflict, competition, challenge"
  },
  {
    "number": 6,
    "name": "Six of Wands",
    "description": "A victorious rider on horseback wearing a wreath",
    "meaning": "Victory, recognition, triumph"
  },
  {
    "number": 7,
    "name": "Seven of Wands",
    "description": "A person defends a hill from attackers",
    "meaning": "Standing up for oneself, perseverance"
  },
  {
    "number": 8,
    "name": "Eight of Wands",
    "description": "Eight wands flying through the sky",
    "meaning": "Rapid events, news, movement"
  },
  {
    "number": 9,
    "name": "Nine of Wands",
    "description": "A weary warrior holds a wand, surrounded by others",
    "meaning": "Endurance, caution, preparedness"
  },
  {
    "number": 10,
    "name": "Ten of Wands",
    "description": "A man carrying a heavy bundle of wands",
    "meaning": "Burden, responsibility, overload"
  },
  {
    "number": 11,
    "name": "Page of Wands",
    "description": "A youth holding a wand against a desert backdrop",
    "meaning": "New ideas, messages, enthusiasm"
  },
  {
    "number": 12,
    "name": "Knight of Wands",
    "description": "A warrior on a charging horse with a raised wand",
    "meaning": "Passion, determination, energy"
  },
  {
    "number": 13,
    "name": "Queen of Wands",
    "description": "A woman with a wand and a black cat at her feet",
    "meaning": "Charisma, confidence, independence"
  },
  {
    "number": 14,
    "name": "King of Wands",
    "description": "A man with a wand and a salamander on his shield",
    "meaning": "Vision, leadership, courage"
  },
  {
    "number": 1,
    "name": "Ace of Cups",
    "description": "A hand out of a cloud holds a cup overflowing with water",
    "meaning": "Emotions, love, new relationships"
  },
  {
    "number": 2,
    "name": "Two of Cups",
    "description": "A man and woman exchange cups",
    "meaning": "Union, harmony, partnership"
  },
  {
    "number": 3,
    "name": "Three of Cups",
    "description": "Three women raising cups in a toast",
    "meaning": "Joy, friendship, celebration"
  },
  {
    "number": 4,
    "name": "Four of Cups",
    "description": "A person sits under a tree with cups in front",
    "meaning": "Contemplation, apathy, missed opportunities"
  },
  {
    "number": 5,
    "name": "Five of Cups",
    "description": "A figure mourns over overturned cups",
    "meaning": "Loss, regret, sorrow"
  },
  {
    "number": 6,
    "name": "Six of Cups",
    "description": "Children exchanging cups near a house",
    "meaning": "Nostalgia, memories, innocence"
  },
  {
    "number": 7,
    "name": "Seven of Cups",
    "description": "A person choosing among seven cups of illusions",
    "meaning": "Fantasy, choices, illusion"
  },
  {
    "number": 8,
    "name": "Eight of Cups",
    "description": "A figure walking away from eight cups toward mountains",
    "meaning": "Search for meaning, disappointment, departure"
  },
  {
    "number": 9,
    "name": "Nine of Cups",
    "description": "A contented man before nine cups",
    "meaning": "Wish fulfillment, comfort, satisfaction"
  },
  {
    "number": 10,
    "name": "Ten of Cups",
    "description": "A happy family under a rainbow of cups",
    "meaning": "Family, happiness, harmony"
  },
  {
    "number": 11,
    "name": "Page of Cups",
    "description": "A youth gazes at a fish in a cup",
    "meaning": "Creativity, imagination, new feelings"
  },
  {
    "number": 12,
    "name": "Knight of Cups",
    "description": "A rider holds a cup in hand",
    "meaning": "Romance, invitation, idealism"
  },
  {
    "number": 13,
    "name": "Queen of Cups",
    "description": "A queen holding a cup against a backdrop of sea and lilies",
    "meaning": "Empathy, compassion, emotional maturity"
  },
  {
    "number": 14,
    "name": "King of Cups",
    "description": "A king with a cup on his throne, surrounded by water symbols",
    "meaning": "Emotional balance, compassion, diplomacy"
  },
  {
    "number": 1,
    "name": "Ace of Swords",
    "description": "A hand out of a cloud holds a sword with a wreath on the blade",
    "meaning": "Idea, truth, mental clarity"
  },
  {
    "number": 2,
    "name": "Two of Swords",
    "description": "A blindfolded woman holds two crossed swords",
    "meaning": "Indecision, balance, stalemate"
  },
  {
    "number": 3,
    "name": "Three of Swords",
    "description": "A heart pierced by three swords against a backdrop of clouds",
    "meaning": "Heartbreak, sorrow, emotional pain"
  },
  {
    "number": 4,
    "name": "Four of Swords",
    "description": "A knight lies in a church with swords hanging above him",
    "meaning": "Rest, recovery, meditation"
  },
  {
    "number": 5,
    "name": "Five of Swords",
    "description": "A person gathers swords while two walk away dejected",
    "meaning": "Conflict, defeat, ego"
  },
  {
    "number": 6,
    "name": "Six of Swords",
    "description": "A figure in a boat moves toward calm shores",
    "meaning": "Transition, moving on, relief"
  },
  {
    "number": 7,
    "name": "Seven of Swords",
    "description": "A person steals swords while looking back",
    "meaning": "Deception, strategy, stealth"
  },
  {
    "number": 8,
    "name": "Eight of Swords",
    "description": "A woman bound and surrounded by sharp swords",
    "meaning": "Restriction, fear, self-imposed limitations"
  },
  {
    "number": 9,
    "name": "Nine of Swords",
    "description": "A person in darkness clutching their head",
    "meaning": "Anxiety, nightmares, worry"
  },
  {
    "number": 10,
    "name": "Ten of Swords",
    "description": "A figure lies with ten swords in their back",
    "meaning": "Betrayal, endings, collapse"
  },
  {
    "number": 11,
    "name": "Page of Swords",
    "description": "A youth holding a sword, watching alertly",
    "meaning": "Observation, news, curiosity"
  },
  {
    "number": 12,
    "name": "Knight of Swords",
    "description": "A rider charging forward with a sword",
    "meaning": "Determination, focus, impulsiveness"
  },
  {
    "number": 13,
    "name": "Queen of Swords",
    "description": "A woman with a sword and a raven in the sky background",
    "meaning": "Clarity, honesty, independence"
  },
  {
    "number": 14,
    "name": "King of Swords",
    "description": "A king with a sword and an eagle on his shield",
    "meaning": "Logic, authority, justice"
  },
  {
    "number": 1,
    "name": "Ace of Pentacles",
    "description": "A hand out of a cloud holds a golden pentacle",
    "meaning": "Material opportunity, prosperity"
  },
  {
    "number": 2,
    "name": "Two of Pentacles",
    "description": "A person juggling two pentacles",
    "meaning": "Balance, adaptability, flexibility"
  },
  {
    "number": 3,
    "name": "Three of Pentacles",
    "description": "Three craftsmen building a cathedral",
    "meaning": "Skill, collaboration, quality work"
  },
  {
    "number": 4,
    "name": "Four of Pentacles",
    "description": "A figure holds one pentacle and clutches three others to their chest",
    "meaning": "Conservation, greed, stability"
  },
  {
    "number": 5,
    "name": "Five of Pentacles",
    "description": "Two beggars outside a church in the snow",
    "meaning": "Financial hardship, isolation, need"
  },
  {
    "number": 6,
    "name": "Six of Pentacles",
    "description": "A wealthy person distributes coins to the poor",
    "meaning": "Generosity, charity, fair distribution"
  },
  {
    "number": 7,
    "name": "Seven of Pentacles",
    "description": "A farmer rests, looking at growing plants",
    "meaning": "Patience, assessment of investment"
  },
  {
    "number": 8,
    "name": "Eight of Pentacles",
    "description": "A youth diligently working on a pentacle",
    "meaning": "Diligence, learning, skill development"
  },
  {
    "number": 9,
    "name": "Nine of Pentacles",
    "description": "A woman in a garden with grapes and a bird",
    "meaning": "Abundance, independence, self-sufficiency"
  },
  {
    "number": 10,
    "name": "Ten of Pentacles",
    "description": "A family standing in front of a grand home",
    "meaning": "Legacy, stability, family wealth"
  },
  {
    "number": 11,
    "name": "Page of Pentacles",
    "description": "A youth studying a pentacle thoughtfully",
    "meaning": "New ventures, learning, opportunity"
  },
  {
    "number": 12,
    "name": "Knight of Pentacles",
    "description": "A rider with a pentacle stands on the ground",
    "meaning": "Practicality, reliability, patience"
  },
  {
    "number": 13,
    "name": "Queen of Pentacles",
    "description": "A woman surrounded by pentacles and flowers",
    "meaning": "Nurturing, comfort, material abundance"
  },
  {
    "number": 14,
    "name": "King of Pentacles",
    "description": "A king seated on a throne holding a pentacle, a bull at his feet",
    "meaning": "Wealth, stability, leadership"
  }
]

parser = argparse.ArgumentParser(
  description="Generate Tarot Card Images with OpenAI API"
)
parser.add_argument(
  "-k", "--api_key",
  required=True,
  help="Key OpenAI API (required)"
)

args = parser.parse_args()

client = OpenAI(api_key=args.api_key)

model = "gpt-image-1"

os.makedirs(output_dir, exist_ok=True)


def generate_and_save(prompt: str, filepath: str):
  if os.path.exists(filepath):
    print(f"File already exists: {filepath}")
    return
  img = client.images.generate(
    model=model,
    prompt=prompt,
    n=1,
    size="1024x1536",
    quality=quality
  )
  image_bytes = base64.b64decode(img.data[0].b64_json)
  with open(filepath, "wb") as f:
    f.write(image_bytes)
    print(f"Created: {filepath}")

prompt = f""""
Draw the back of the tarot card in style: {style}
"""

generate_and_save(prompt, output_dir + "/-1.png")

i = 0
for card in CARDS:
    filepath = os.path.join(output_dir, f"{i}.png")

    if os.path.exists(filepath):
        print(f"File already exists: {filepath}")
        i += 1
        continue

    number = f"""
    "number": {card["number"]},
    """
    number_desc = "Write the card number: top center only for major arcana"
    if i>21:
        number = ""
        number_desc = ""
    prompt = f"""
    {number}
    "name": "{card["name"]}",
    "description": "{card["description"]}",
    "meaning": "{card["meaning"]}"

    Background: Light
    Write the card name: bottom center.
    {number_desc}

    Draw this tarot card in style: {style}   
    """

    print(prompt)
    generate_and_save(prompt, filepath)
    i += 1
