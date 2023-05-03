from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

llm = OpenAI(temperature=0.76)


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
