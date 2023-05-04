from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import openai
import os
import json
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(temperature=0.76, max_tokens=1400, model_name="gpt-3.5-turbo")


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


def get_midjourney_prompts_for_image_creation(prompts):
    prompt_template = "Take the following document and just grab the text after each part that says 'Midjourney Prompt:' and append it to a python list and return the full list. Make sure to use regular quotation marks (\"index value\") for each string item in the list indexes and just return the list and nothing else. Output should look like [\"item1\", \"item2\", ....]:\ndocument:\n{prompts}\n\nAnswer:\n"
    prompt = PromptTemplate(
        input_variables=["prompts"],
        template=prompt_template
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    list_as_str = chain.run(prompts)
    print(list_as_str)
    lst = json.loads(list_as_str)
    return lst


def get_story_text_list(prompts):
    prompt_template = "Take the following document and just grab the text after each part that says 'Story Text:' and append it to a python list and return the full list. Make sure to use regular quotation marks (ex. \"index value\") for each string item in the list indexes and just return the list and nothing else. Output should look like -> [\"item1\", \"item2\", ....]:\ndocument:\n{prompts}\n\nAnswer:\n"
    prompt = PromptTemplate(
        input_variables=["prompts"],
        template=prompt_template
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    list_as_str = chain.run(prompts)
    print(list_as_str)
    lst = json.loads(list_as_str)
    print(lst)
    return lst

# prompts = """
# Story Text: Nate was feeling a bit uninspired until he had the chance to talk with an incredible man who had worked with 8 different presidents.
# Midjourney Prompt: Nate is sitting in a large boardroom, looking up at the incredibly person who had the chance to work with 8 different presidents. His golden brown skin glistens in the light of the boardroom and his nappy fro frames his strong jawline. He looks up with a face of awe, taking in the words of wisdom from this wise figure.

# Story Text: This man had seen the world and he told Nate that he was special! It was just the confirmation Nate needed to follow his dream of being an empowerment leader.
# Midjourney Prompt: Nate is standing in the middle of a busy city street, his eyes closed and his head tilted up to the sky. His golden brown skin is illuminated by the warm light of the setting sun and his nappy fro is gently swaying in the wind. He is standing tall and proud, feeling inspired by the words of the man he had just met.

# Story Text: Nate had an idea to create a video automation tool that would use his voice and AI art to create empowerment stories from his journal entries. He knew this would help him stay motivated to write in his journal and he was excited to use all the videos to share his stories with the world.
# Midjourney Prompt: Nate is hunched over his laptop, working intently on a project he is passionate about. His golden brown skin glows from the light of his laptop screen and his nappy fro is pulled up in a ponytail. He is typing quickly, with a determined look on his face, as he works to create an automation tool that will help him make his dreams come true.

# Story Text: He was now feeling in sync with himself and his journey and knew that he had the power to make a difference.
# Midjourney Prompt: Nate is standing on a beach, looking out at the vast ocean before him. His golden brown skin shimmers in the sunlight and his nappy fro is blowing gently in the wind. He is standing tall, feeling a sense of peace and confidence as he realizes that he has the power to make a difference.

# Story Text: Nate's story reminds us that no matter how difficult things may seem, we all have the potential to become amazing leaders when we believe in ourselves.
# Midjourney Prompt: Nate is standing atop a mountain, looking out at the world below him. His golden brown skin is glowing in the sunlight and his nappy fro is blowing in the wind. He is standing tall, with a look of determination on his face, as he reminds himself and others that no matter how hard things may seem, we can all become amazing leaders when we believe in ourselves.
# """
# print(get_midjourney_prompts_for_image_creation(prompts))
