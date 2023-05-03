from ai_funcs import create_story, create_midjourney_prompts_from_story, format_midjourney_data_for_notion, get_midjourney_prompts_for_image_creation
from notion_journals import read_journal_from_notion, write_voiceover_script_to_notion_page, add_images_to_story
from ai_image_generator import generate_ai_art
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
    write_voiceover_script_to_notion_page(
        formatted_prompts, url, name="Midjourney Prompts", title="Prompts"
    )
    return formatted_prompts


def run_journal_to_video(url):
    # create the story from the journal
    story_obj = create_story_from_notion_journal(url)
    # create the midjourney prompts for the story
    midjourney_formatted_prompts = create_midjourney_prompts(
        story_obj["story_url"], story_obj["story"])
    # format the midjourney prompts for easy generation
    midjourney_prompts_list = get_midjourney_prompts_for_image_creation(
        midjourney_formatted_prompts)
    # generate ai art
    ai_art_links = generate_ai_art(midjourney_prompts_list)
    # write the ai art to a notion page
    add_images_to_story(story_obj['story_url'], ai_art_links)


run_journal_to_video(
    "https://www.notion.so/Journal-Entry-One-072721f4d3954a87a8170183f88470a3")
