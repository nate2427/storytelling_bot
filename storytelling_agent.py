from ai_funcs import create_story, create_midjourney_prompts_from_story, format_midjourney_data_for_notion, get_midjourney_prompts_for_image_creation, get_story_text_list
from notion_journals import read_journal_from_notion, write_voiceover_script_to_notion_page, add_images_to_story
from ai_image_generator import generate_ai_art
from ai_voice_agent import create_voiceover_from_text
from video_agent import generate_empowering_video
import json


def create_story_from_notion_journal(url):
    # get the journal info from the notion page
    journal = read_journal_from_notion(url)
    # create a story from the journal
    story_obj = create_story(journal)
    # write the story to a notion page with the page of the journal
    new_story_url = write_voiceover_script_to_notion_page(
        story_obj["story"], url, name=story_obj["story_title"])
    # return the story to use later to create images for the story
    return {
        "story_url": new_story_url,
        "story": story_obj["story"],
    }


def create_midjourney_prompts(url, story):
    # create prompts from the story
    prompts = create_midjourney_prompts_from_story(story)
    # format the prompts
    formatted_prompts = format_midjourney_data_for_notion(prompts)
    # save formatted prompts to a notion page
    midjourney_prompts_url = write_voiceover_script_to_notion_page(
        formatted_prompts, url, name="Midjourney Prompts", title="Prompts"
    )
    return formatted_prompts, midjourney_prompts_url


def run_journal_to_video(url):
    # create the story from the journal
    story_obj = create_story_from_notion_journal(url)
    # create the midjourney prompts for the story
    midjourney_formatted_prompts, prompts_url = create_midjourney_prompts(
        story_obj["story_url"], story_obj["story"])
    # format the midjourney prompts for easy generation
    midjourney_prompts_list = get_midjourney_prompts_for_image_creation(
        midjourney_formatted_prompts)
    # generate ai art
    ai_art_links = generate_ai_art(midjourney_prompts_list)
    # write the ai art to a notion page
    add_images_to_story(prompts_url, ai_art_links)
    # create the voiceover audio
    audio = create_voiceover_from_text(story_obj["story"])
    # write the audio to a notion page
    story_text_list = get_story_text_list(story_obj["story"])
    generate_empowering_video(
        audio, story_text_list, ai_art_links
    )


run_journal_to_video(
    "https://www.notion.so/Journal-Entry-One-072721f4d3954a87a8170183f88470a3")
