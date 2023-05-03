from ai_funcs import create_story
from notion_journals import read_journal_from_notion, write_voiceover_script_to_notion_page


def create_story_from_notion_journal(url) -> str:
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


print(create_story_from_notion_journal(
    "https://www.notion.so/Journal-Entry-One-072721f4d3954a87a8170183f88470a3"))
