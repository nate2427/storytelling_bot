from notion_client import Client
import os
from dotenv import load_dotenv
load_dotenv()

notion_token = os.getenv('NOTION_API_KEY')
# this will be input to the function, will change once i build an app around it. this is for testing
journal_notion_page = "https://www.notion.so/Journal-Entry-One-072721f4d3954a87a8170183f88470a3"


def connect_to_notion(api_key, url):
    notion = Client(auth=api_key)

    # parse the url to get the page id by splitting the string at - and grabbing the last value
    page_id = url.split("-")[-1]

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
        if block_type != "image":
            rich_text_list = result[block_type]["rich_text"]
            block_text = rich_text_list[0]["text"]["content"]
            str_result += f"{block_text}\n"

    # Return the titles of the journal entries as a list of strings
    return str_result


print(connect_to_notion(notion_token,
                        journal_notion_page))
