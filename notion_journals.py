from notion_client import Client
import os
from dotenv import load_dotenv
load_dotenv()

notion_token = os.getenv('NOTION_API_KEY')
# this will be input to the function, will change once i build an app around it. this is for testing
journal_notion_page = "https://www.notion.so/Journal-Entry-One-072721f4d3954a87a8170183f88470a3"

notion = Client(auth=notion_token)


def extract_page_id(url):
    return url.split("-")[-1]


def read_journal_from_notion(url):
    # parse the url to get the page id by splitting the string at - and grabbing the last value
    page_id = extract_page_id(url)

    print("Connecting to notion...")
    print(f"Page id: {page_id}")

    # Retrieve the blocks for the Page
    # db = notion.pages.retrieve(page_id=page_id)
    results = notion.blocks.children.list(
        block_id=page_id,
        page_size=100
    )

    # get all the children of the page
    # Print the block type and text for each block
    str_result = ""
    for result in results["results"]:
        block_type = result["type"]
        if block_type != "image" and block_type != "child_page":
            print(result)
            rich_text_list = result[block_type]["rich_text"]
            if len(rich_text_list) > 0:
                block_text = rich_text_list[0]["text"]["content"]
                str_result += f"{block_text}\n"

    # Return the titles of the journal entries as a list of strings
    return str_result


def write_voiceover_script_to_notion_page(content, url, name="Voiceover Script"):
    print(content)
    print(name)
    # get page id
    page_id = extract_page_id(url)

    # Create a new page in the database
    new_page = {
        "parent": {"page_id": page_id},
        "properties": {
            "title": [
                {
                    "text": {
                        "content": name
                    }
                }
            ]
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Script Title"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content,
                            }
                        }
                    ]
                }
            },
        ]
    }
    story_page = notion.pages.create(
        properties=new_page["properties"], children=new_page["children"], parent=new_page["parent"])
    return story_page["url"]


# write_voiceover_script_to_notion_page(
#     "This is a test voiceover script", journal_notion_page)
