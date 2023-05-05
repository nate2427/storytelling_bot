

str_list = ['Duration: 10 seconds\nMidjourney Prompt: Nate standing in front of a large, historic building, looking up at it with wonder and excitement in his eyes.', 'Duration: 12 seconds\nMidjourney Prompt: Nate sitting at a desk, surrounded by notebooks and pens, furiously scribbling down his ideas for his empowerment videos.', 'Duration: 15 seconds\nMidjourney Prompt: Nate walking through a bustling city, headphones in his ears, nodding his head along to the beat of his favorite song as he brainstorms new ideas for his video project.', 'Duration: 8 seconds\nMidjourney Prompt: Nate standing in front of a mirror, practicing his speeches and perfecting his delivery for his upcoming videos.',
            'Duration: 20 seconds\nMidjourney Prompt: Nate sitting on a park bench, surrounded by a group of diverse people of all ages, races, and backgrounds, listening intently to his words of empowerment and encouragement.', 'Duration: 14 seconds\nMidjourney Prompt: Nate standing on a stage, microphone in hand, delivering a powerful speech to a packed room of people, his voice ringing out clear and strong.', 'Duration: 18 seconds\nMidjourney Prompt: Nate sitting at a desk, surrounded by letters and emails from people around the world who have been inspired and empowered by his videos, a smile of satisfaction on his face.']


def get_duration_list(string_list):
    duration_list = []
    for string in string_list:
        duration = string.split(" ")[1]
        duration_list.append(int(duration))
    return duration_list


def get_midjourney_prompt_list(string_list):
    midjourney_prompt_list = []
    for string in string_list:
        midjourney_prompt = string.split("Midjourney Prompt: ")[1]
        midjourney_prompt_list.append(midjourney_prompt)
    return midjourney_prompt_list
