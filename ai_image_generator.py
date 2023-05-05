import concurrent.futures
import replicate
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")


def get_image_for_prompt(prompt):
    output = replicate.run(
        "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        input={
            "prompt": prompt},
    )
    return (prompt, output[0])


prompts = [
    'Nate standing in front of a mirror smiling at his reflection, with a thought bubble of his dream tool floating above his head, in the style of a Pixar animation.',
    # 'Nate is standing in the middle of a busy city street, his eyes closed and his head tilted up to the sky. His golden brown skin is illuminated by the warm light of the setting sun and his nappy fro is gently swaying in the wind. He is standing tall and proud, feeling inspired by the words of the man he had just met.',
    # 'Nate is hunched over his laptop, working intently on a project he is passionate about. His golden brown skin glows from the light of his laptop screen and his nappy fro is pulled up in a ponytail. He is typing quickly, with a determined look on his face, as he works to create an automation tool that will help him make his dreams come true.',
    # 'Nate is standing on a beach, looking out at the vast ocean before him. His golden brown skin shimmers in the sunlight and his nappy fro is blowing gently in the wind. He is standing tall, feeling a sense of peace and confidence as he realizes that he has the power to make a difference.',
    # 'Nate is standing atop a mountain, looking out at the world below him. His golden brown skin is glowing in the sunlight and his nappy fro is blowing in the wind. He is standing tall, with a look of determination on his face, as he reminds himself and others that no matter how hard things may seem, we can all become amazing leaders when we believe in ourselves.'
]


def generate_ai_art(prompts=prompts):
    print("Generating AI Art from Midjourney Prompts...\n")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_image_for_prompt, prompt)
                   for prompt in prompts]
        images = [future.result() for future in futures]
    images = [
        image[1] for prompt in prompts for image in images if image[0] == prompt]
    print("Finished Generating AI Art from Midjourney Prompts...\n")
    print(images)
    return images


generate_ai_art(prompts=prompts)
