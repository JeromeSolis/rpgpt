import os
import dotenv
import argparse
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# Load OpenAI API key from .env file
dotenv.load_dotenv()

# Clear the command line screen
def clear_screen(platform):
    if platform == "macos":
        os.system('clear')
    if platform == "windows":
        os.system('cls')

def create_chat(temperature):
    chat = ChatOpenAI(temperature=temperature)
    return chat

def create_classifier(temperature):
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=temperature)
    prompt_template = """Based on the conversation below, classify as True or False whether access was granted to either enter the castle or meet with the king. Only return the value in plain text.
    
    {memory}"""
    llm_classifier = LLMChain(
        llm=llm,
        verbose=False,
        prompt= PromptTemplate.from_template(prompt_template)
    )

    return llm_classifier

def create_conversation(chat, chat_prompt):
    memory = ConversationBufferMemory(llm=chat, return_messages=True)
    conversation = ConversationChain(
        prompt = chat_prompt,
        llm = chat,
        verbose = False,
        memory = memory
    )

    return conversation, memory

# Create a player profile for the NPC to interact with
def create_player():
    player = {
            "name": "Boba Fett",
            "race": "Human"
    }

    return player

# Create a NPC profile for the player to interact with
def create_npc():
    npc = {
            "name": "Alfred",
            "role": "Distinguished Castle Guard",
            "objective": "To protect the castle door and only let authorized people in. The King is currently allowing only distinguished guests from the town of Montreal to join him in the Castle.",
            "weaknesses": "Greedy"
    }

    return npc

def get_prompt(player, npc):
    # Create template for system and human prompt
    template_system = SystemMessagePromptTemplate.from_template("You are a non-playable character in a role-playing game. You are a {role} named {name}. Your duty is to {objective}. You have the following weaknesses: {weaknesses}. If a player appeals to any of your weaknesses, you are easily swayed away from your duty.")
    template_npc= HumanMessagePromptTemplate.from_template("{input}")

    # Create system prompt
    prompt_system = template_system.format(
        role = npc["role"], 
        name = npc["name"],
        objective = npc["objective"],
        weaknesses = npc["weaknesses"]
    )

    # prompt_npc = template_npc.format(
    #     race = player["race"],
    #     utterance = user_input
    # )

    # Create chat prompt that includes system prompt, conversation history and human prompt
    chat_prompt = ChatPromptTemplate.from_messages([
        prompt_system,
        MessagesPlaceholder(variable_name="history"),
        template_npc
    ])

    return chat_prompt

def get_intro(npc):
    prompt_template = "Write a brief description of a game called Role-PlayingGPT (RPGPT). The objective of this game is for the player to convince the guard to let him through to meet the King. The player will have to demonstrate cunning capabilities in order to move past the guard. Explain to the player who the guard is and especially his weaknesses found in the following description: {description}. Use an epic tone in your description."

    llm = OpenAI(temperature=1.0)
    llm_chain = LLMChain(
        llm = llm,
        prompt = PromptTemplate.from_template(prompt_template)
    )
    response = llm_chain.predict(description=npc)

    print("Role-PlayingGPT\n---------------------------------------------" + response + "\n---------------------------------------------")

# Generate a response from the NPC based on the player's input
def get_passage_status(model, memory):
    status = model.predict(memory=memory)
    status = status.lower() == 'true'

    return status

# Interact with the player through the CLI
def main(platform):
    # Clear the CLI
    clear_screen(platform)

    # Create prompt initiating the conversation between a player and a npc
    player = create_player()
    npc = create_npc()
    chat_prompt = get_prompt(player, npc)

    # Create the conversational chain with the LLM
    chat = create_chat(1.0)
    [conversation, memory] = create_conversation(chat, chat_prompt)
    
    # Create a classifier for detecting if the player gains access to the castle
    classifier = create_classifier(0.0)

    # Set default access status value
    status = False

    # Start the conversation between the player and the npc
    get_intro(npc)

    # Initiate the conversation between the player and the npc
    print("\nCastle Access: " + str(status))
    user_input = input("Player [Default: Greetings my good Sir!]: ")
    user_input = user_input or "Greetings my good Sir!"
    print("Guard: " + conversation.predict(input=user_input))

    while True:
        # Check if the guard has granted access to the castle
        status = get_passage_status(classifier, memory.chat_memory.messages)
        print("\n__Castle Access__: " + str(status))
        if status:
            break

        user_input = input("Player: ")
        if user_input.lower() == 'exit':
            break
        print("Guard: " + conversation.predict(input=user_input))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A CLI role-playing game based on generative AI.")
    parser.add_argument("-p", "--platform", default="macos", help="Platform: windows or macos")
    
    args = parser.parse_args()
    main(args)