from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import openai
import os
import json
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

llm = OpenAI(temperature=0.76, max_tokens=1400)


def create_story(journal_entry):

    # define prompt template
    prompt_template = "Take the following journal entry and turn it into an empowering story for children. Begin the story with an inteesting opener to catch the attention of the children and capture the personality of the main character (which is me, Nate), then describe how the main character overcomes the challenge you feel like the journal is mentioning. Make this nuanced and esocentric in nature and end with a positive message that helps children grow and see a bigger part of life. Make sure the story is within the length of 45secs to 1min.\n\nJournal Entry:\n{journal_entry}\n\nStory:\n"

    prompt = PromptTemplate(
        input_variables=["journal_entry"],
        template=prompt_template,
    )

    # create LLMChain object
    chain = LLMChain(llm=llm, prompt=prompt)

    # generate voiceover script
    story = chain.run(journal_entry)

    # create prompt template to get a interesting title for the story
    story_title_prompt = "Give a title for the following children's story. Make sure it has a great attention grabber as a name.\n\nStory:\n{story}\n\nTitle:\n"

    story_title_prompt_template = PromptTemplate(
        input_variables=["story"],
        template=story_title_prompt
    )

    chain = LLMChain(llm=llm, prompt=story_title_prompt_template)

    story_title = chain.run(story)

    # print script
    return ({
        "story": story,
        "story_title": story_title
    })


def create_midjourney_prompts_from_story(story):
    # define prompt template
    prompt_template = "Given the children story, split the story into 7 even sections and then generate very descriptive midjourney ai art prompts that creates a high level of engagement about that specific part of the story. The prompts should always describe Nate as a black man with golden brown skintone, strong jaw line, nappy hair fro. From that point, you can describe him for appropriate for the scene, whether thats age, timeframe, weather, location, etc. Pretty, i want to keep the same description of Nate so that midjourney keeps the original image of Nate intact as it generates different scenes from the original from the plot of the story. I need you to return this as a json list of objects that looks like this:\n keys: text and midjourney_prompt. the text represents the text from the original story that will be read when that image is shown. The text need to all add up to be the whole original story when all values for the text keys are concatenated together. \n\nStory:\n{story}\n\nPrompts:\n"

    prompt = PromptTemplate(
        input_variables=["story"],
        template=prompt_template
    )

    # create LLMChain object
    chain = LLMChain(llm=llm, prompt=prompt)

    prompts = chain.run(story)

    return prompts


def format_midjourney_data_for_notion(prompts):
    prompt_template = "Take the following json list and format it in the following way as a string:\nStory Text: text key from object\nMidjourney Prompt: midjourney_prompt key from object\n\nStory Text: text key from object\nMidjourney Prompt: midjourney_prompt key from object\n\n...json list:\n{prompts}\n\n"

    prompt = PromptTemplate(
        input_variables=["prompts"],
        template=prompt_template
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run(prompts)
