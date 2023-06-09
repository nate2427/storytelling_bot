from notion_client import Client
import os
import requests
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

    # Retrieve the blocks for the Page
    results = notion.blocks.children.list(
        block_id=page_id,
        page_size=100
    )

    # get all the children of the page
    str_result = ""
    for result in results["results"]:
        block_type = result["type"]
        if block_type != "image" and block_type != "child_page":
            rich_text_list = result[block_type]["rich_text"]
            if len(rich_text_list) > 0:
                block_text = rich_text_list[0]["text"]["content"]
                str_result += f"{block_text}\n"

    # Return the titles of the journal entries as a list of strings
    return str_result


def write_to_notion_page(content, url, name="Voiceover Script", title="Script", extra_space=False):
    if extra_space == False:
        content = content.split("\n\n")
    # get page id
    page_id = extract_page_id(url)
    children = []
    children.append({
        "object": "block",
        "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": title}}]
                }
    })
    for parag in content:
        children.append({"object": "block", "type": "paragraph", "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": parag}}]}})
        if extra_space == True:
            children.append({"object": "block", "type": "paragraph", "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": "\n\n"}}]}})

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
        "children": children
    }
    story_page = notion.pages.create(
        properties=new_page["properties"], children=new_page["children"], parent=new_page["parent"])
    return story_page["url"]


def add_images_to_story(url, images):
    print("Writing images to notion document...\n")
    # get page id
    page_id = extract_page_id(url)
    # Retrieve the blocks for the Page
    results = notion.blocks.children.list(
        block_id=page_id,
        page_size=100
    )
    image_index = 0

    # loop through all the children of the page and adds an image to blocks that are paragraphs with just \n\n
    for i, result in enumerate(results["results"]):
        if i == len(results["results"]) - 1:
            break

        next_block_type = results["results"][i+1]["type"]
        if next_block_type == "paragraph":
            rich_text_list = results["results"][i +
                                                1][next_block_type]["rich_text"]
            if len(rich_text_list) > 0:
                block_text = rich_text_list[0]["text"]["content"]
                if block_text == "\n\n":
                    # append an image block to the current block
                    image_block = {
                        "external": {
                            "url": images[image_index]
                        }
                    }
                    image_index += 1
                    # append the image block to the current block using the current block's id
                    append_image_block(
                        results["results"][i]["id"], image_block)
    print("Images added to story successfully...\n")


def remove_images_from_story(url):
    # get page id
    page_id = extract_page_id(url)
    # Retrieve the blocks for the Page
    results = notion.blocks.children.list(
        block_id=page_id,
        page_size=100
    )
    # loop thru and find blocks that are images and remove them
    for result in results["results"]:
        print(result, "\n\n")
        if result["type"] == "image":
            print("image block")
            # append newlines block to the current block
            append_newlines_block(result["id"])
            # remove the image
            remove_block_from_page(block_id=result["id"])


def remove_block_from_page(block_id):
    url = f'https://api.notion.com/v1/blocks/{block_id}'
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
    }
    response = requests.delete(url, headers=headers)


def append_newlines_block(block_id):
    url = f'https://api.notion.com/v1/blocks/{block_id}/children'
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {notion_token}"
    }
    data = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "\n\n"
                            }
                        }
                    ]
                }
            }
        ]
    }
    response = requests.patch(url, headers=headers, json=data)


def append_image_block(block_id, image_url):
    url = f'https://api.notion.com/v1/blocks/{block_id}/children'
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {notion_token}"
    }
    data = {
        "children": [
            {
                "object": "block",
                "type": "image",
                "image": image_url
            }
        ]
    }
    response = requests.patch(url, headers=headers, json=data)


# does not work
def write_audio_to_notion_page(audio_url, url, title="Voiceover"):
    # get page id
    page_id = extract_page_id(url)
    children = [
        {
            "object": "block",
            "type": "file",
            "file": {
                    "external": {
                        "url": audio_url
                    }
            }
        }

    ]
    new_page = {
        "parent": {"page_id": page_id},
        "properties": {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        "children": children
    }

    story_page = notion.pages.create(
        properties=new_page["properties"], children=new_page["children"], parent=new_page["parent"])
    return story_page["url"]


# url = "https://www.notion.so/Midjourney-Prompts-d0df06abc23849039212d7f1ffeed1df"
# images = ['https://replicate.delivery/pbxt/BUdvsOjVF1ZXBp8LF417fBDL1agZMzetHuvgzhK1FbIcpr4QA/out-0.png', 'https://replicate.delivery/pbxt/g87rnjJ1usoyM5HgKmt9kzj16HWLMDd1PvGyi7lHMMLX6KOE/out-0.png', 'https://replicate.delivery/pbxt/G3VAGBtuchamIlnZHVDz5vNOSVQohbgjfxh9zJKemf6BTXxhA/out-0.png',
#           'https://replicate.delivery/pbxt/Ez4NIEeNYITcVKFSpALT0F135y0JTfuEWAI4PvTbbvanpr4QA/out-0.png', 'https://replicate.delivery/pbxt/JSlClZmqehRTda4X8fq5GHtULSkjU27aevCRIlLhZ68BTXxhA/out-0.png', 'https://replicate.delivery/pbxt/OgVbQyicJv7iOdg0WEeJvxUfyRo2385xcdHxkvQ1Bt8kpr4QA/out-0.png', 'https://replicate.delivery/pbxt/CjYxtIYtIZIcEZyrUKR9feVwnl5IBceL1YZye8c1e3UmMdFHC/out-0.png']
# add_images_to_story(url, images)
