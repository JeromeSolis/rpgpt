# Role-Playing Game Chatbot

This is a Python script that simulates a conversation between a player and a non-playable character (NPC) in a role-playing game. The script uses the LangChain library to create a chatbot that responds to the player's input with dialogues based on predefined NPC profiles.

## Setup

1. Install the required dependencies by running the following command:

```bash
pip install -r requirements.txt`
```


2. Create a `.env` file in the same directory as the script and set your environment variables. For example, if you're using an OpenAI API key, your `.env` file should look like this:

```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the script to start the interactive conversation between the player and the NPC. The player can input text, and the NPC will respond based on its predefined profile and the conversation history.

```bash
python rpgpt.py
```