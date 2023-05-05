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
    prompt_template = "Given the transcript to this children story voiceover, split the story into 7 even sections and then generate very descriptive midjourney ai art prompts that creates a high level of engagement about that specific part of the story. The prompts should always describe Nate as a black man with golden brown skintone, strong jaw line, nappy hair fro. From that point, you can describe him for appropriate for the scene, whether thats age, timeframe, weather, location, etc. Dont use the word Nate in the name, rather refer to Nate with descriptions. Generate the prompts so that midjourney keeps the original description of Nate intact. I need you to return this structured in the format of 'Duration:\ntime\nMidjourney Prompt:\nprompt\n\n'(repeat format for rest). The duration will represent how long i should show the image thats generated from the prompt on the voiceover video. \n\nStory:\n{story}\n\nPrompts:\n"

    prompt = PromptTemplate(
        input_variables=["story"],
        template=prompt_template
    )

    # create LLMChain object
    chain = LLMChain(llm=llm, prompt=prompt)

    prompts = chain.run(story)

    return (prompts.split("\n\n"))


def format_midjourney_data_for_notion(prompts):
    prompt_template = "Take the following json list and format it in the following way as a string:\nStart/End Time: start_end_time key from object\nMidjourney Prompt: midjourney_prompt key from object\n\nStart/End Time: start_end_time key from object\nMidjourney Prompt: midjourney_prompt key from object\n\n...json list:\n{prompts}\n\n"

    prompt = PromptTemplate(
        input_variables=["prompts"],
        template=prompt_template
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run(prompts)


def get_midjourney_prompts_for_image_creation(prompts):
    prompt_template = "Take the following document and just grab the text after each part that says 'Midjourney Prompt:' return them all within a document with each prompt on a new line. Output should look like -> prompt\nprompt\nprompt.\nAlso do the same thing for the Start/End Time. Place the text 'Midjourney Prompts' above the midjourney prompts and put Start/End time above the Start/End time portion.:\ndocument:\n{prompts}\n\nAnswer:\n"
    prompt = PromptTemplate(
        input_variables=["prompts"],
        template=prompt_template
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    list_as_str = chain.run(prompts)
    print(list_as_str)
    return
    lst = json.loads(list_as_str)
    return lst


def get_story_time_list(prompts):
    prompt_template = "Take the following document and just grab the text after each part that says 'Story Text:' return them all within a document with each prompt on a new line. Output should look like -> prompt\nprompt\nprompt:\ndocument:\n{prompts}\n\nAnswer:\n"
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


story = """
Once upon a time, there was a boy named Nate. Nate was always exploring new ideas and chasing his dreams. One day, Nate met a man who had worked on 8 different presidential programs with 8 different presidents! This man told Nate that he was special and that he should follow his dream of becoming an empowerment leader. 
Nate was so excited and knew that this was the confirmation he needed to start his journey. He had an idea to create an amazing tool that would allow him to make videos using his own voice and his own journals. This tool would help him create hundreds of empowerment videos that he could share with everyone on social media.
Nate was thrilled with his new plan and knew that his videos would help inspire others to follow their dreams too. He felt like he was in sync with himself and his journey. Nate was now on a mission to help others become empowered and chase their dreams, just like he was. 
The moral of the story is that when you believe in yourself and your ideas, great things can happen. It's important to always follow your dreams and never give up, even if it seems like a challenging journey. With hard work and determination, anything is possible!
"""
