# Alan Turing - Discord bot
A Discord bot to remind you important moments of the day and make your life beautiful.

### Example:
![Alan Turing Example](https://i.imgur.com/Aa5HDcX.png)

## How to add reminders ?
1. Go to **src** > **Calendar.py**
2. Copy an existing reminder, or create a basic one.

**Example**:

```Reminder("A simple reminder", 'mon-fri', 16, 0, [Message(("This is reminder with a simple message",))])```

## How does it works ?
Currently, *Rachel Thomas* can be:
- be called within Discord... 
- send messages to remember the channels' members to do important things like
their appointment, going to Google Meet, etc.

*Rachel Thomas* use a **set of pre-written tenses** to generate a random message.

## Command list
- *!adduser* :  Add the author in users mentioned on future reminders
- *!removeuser* : Remove the author in users mentioned on future reminders
- *!addtoken <token_becode>* : Add becode token to the author (The token can be generated in your beCode profiles)
- 
## TO DO:
- Ajouter la différence masculin/féminin pour les noms des évènements
- Permettre au bot de choisir le déterminant approprié lors de l'emploi de noms d'évènements.