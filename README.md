# Alan Turing - Discord bot
A Discord bot to remind you important moments of the day.

### Example:
![Alan Turing Example](https://i.imgur.com/Aa5HDcX.png)

## How to add reminders ?
1. Go to **src** > **Routes.py**
2. Copy an existing reminder, or create a basic one.

**Example**:

```Reminder("A simple reminder", 'mon-fri', 16, 0, [Message(("This is reminder with a simple message",))])```

## How does it works ?
Currently, *Allan Turing* can't be called within Discord... It simply send
messages to remember the channels' members to do important things like
their appointment, going to Google Meet, etc.

*Alland Turing* use a **set of pre-written tenses** to generate a random message.

## TO DO:
- Ajouter la différence masculin/féminin pour les noms des évènements
- Permettre au bot de choisir le déterminant approprié lors de l'emploi de noms d'évènements.