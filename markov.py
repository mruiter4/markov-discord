"""Generate Markov text from text files."""

from random import choice
import re
from string import punctuation
import os
import discord

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    with open(file_path) as file: 
        text_string = file.read()
        text_string = text_string.replace("\n", " ")
        text_string = text_string.replace("--", "")
        text_string = text_string.replace("  ", " ")
        #text_string = re.sub(r"(punctuation)+", "%%%", text_string)
    return text_string

def make_chains(input_text, n=2):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """
    chains = {}

    #create a list of words from the input_text
    word_list = input_text.split()

    #loop through the words and create unique tuple keys
    for i in range(len(word_list)-2):
        #create tuple with word and the next word
        key = tuple(word_list[i:i+n])

        if key in chains:
            chains[key].append(word_list[i+2])
        else:
            chains[key] = [word_list[i+2]]

    return chains

def make_text(chains):
    """Return text from chains"""
    
    words = []
    starting_keys = []

    #make a list of keys that start with capital
    for key in chains.keys():
        if key[0].istitle():
            starting_keys.append(key)
    
    #create 'paragraphs'
    for i in range(2):
        #random key from the keys that are capitalized
        link = choice(starting_keys)
        words.extend(link)
        next_word = choice(chains[link])
        words.append(next_word)

    
    
        #continue making new keys and adding words until a key is not in dict.
        #or a word with punctuation is added; This makes a sentence
        while True:
            link = (link[1], next_word)
            if link in chains:
                next_word = choice(chains[link])
                words.append(next_word)
                if next_word.endswith(('.', '!', '?')):
                    break
            else:
                break

    return " ".join(words)

input_path = "austin.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text,2)

# Produce random text
random_text = make_text(chains)




#DISCORD
client = discord.Client()


@client.event
async def on_ready():
    print(f'Successfully connected! Logged in as {client.user}.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Tell me'):
        await message.channel.send(random_text)


client.run(os.environ['DISCORD_TOKEN'])
