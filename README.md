# Role-Playing Game Chatbot

This is a Python script that simulates a conversation between a player and a non-playable character (NPC) in a role-playing game. The script uses the LangChain library to create a chatbot that responds to the player's input with dialogues based on predefined NPC profiles.

## Setup

1. Ensure you have Python 3.11.2 installed.
2. Clone the repository:
    ```bash
    git clone https://github.com/JeromeSolis/rpgpt.git
    ```
3. Navigate to the directory and install the required packages:
    ```bash
    pip install -r requirements.txt`
    ```
4. Create a `.env` file (use the `.env.template` as a boilerplate) in the same directory as the script and set your environment variables. For example, if you're using an OpenAI API key, your `.env` file should look like this:
    ```bash
    OPENAI_API_KEY=your_api_key_here
    ```

## How to play

1. Navigate to the directory where the game script is located.
2. Start the game with the command:   
    ```bash
    python rpgpt.py -p [platform]
    ```
    Replace `[platform]` with either `macos` or `windows` depending on your operating system.

3. Follow the on-screen prompts to play the game. The player can input text, and the NPC will respond based on its predefined profile and the conversation history.
4. Type `exit` at any time to end the game.