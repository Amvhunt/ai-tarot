# ai-tarot

Already generated tarot cards: [https://evgenyigumnov.github.io/ai-tarot](https://evgenyigumnov.github.io/ai-tarot)

## Installation
```
pip install -r requirements.txt
```
## Usage
Edit `generate-cards.py` and set style of tarot cards: 
```
style = "Funny, comic style"
```

## Run
```
python generate-cards.py -k YOUR_OPENAI_API_KEY
```

## Result
Check result in folder `generated-cards`. Remove files you don't like and launch again the script for regeneration deleted cards.

## Share your Tarot deck via pull request
All new cards will be added to the repository in folder `static/deck/DECK_ID`.
