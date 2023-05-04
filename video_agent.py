from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.editor import *


images = ['https://replicate.delivery/pbxt/VfXfRyrgZLqXi02REDAdwcpqq4oQ4aZebXadKz2ZxfD9uohDB/out-0.png', 'https://replicate.delivery/pbxt/Zf9vbeoupticJENTF17e97tfXnvn2uVM2fAyuBRk25cceiGOE/out-0.png', 'https://replicate.delivery/pbxt/LjjHJOY9p5qNPJQIhpYOce5mIAqFfP5xvTK648gePOTqX0whA/out-0.png',
          'https://replicate.delivery/pbxt/AppGYdNsDW7EA5XF41ryLriRw1GvKGklsf37ejL7R2y3La4QA/out-0.png', 'https://replicate.delivery/pbxt/CMYweKxCo4SkLKzG9eVddj1fmQgW7nDBItK3orHZGjZpX0whA/out-0.png', 'https://replicate.delivery/pbxt/DsMh6UbDzfy9B6XNZo0GnsHllZOfs9pPTQe7Vyf5eSjBfiGOE/out-0.png', 'https://replicate.delivery/pbxt/4hK0gBDDUXo4CFmaurrinimkyCoUjiksEazlQnweviU4FNcIA/out-0.png']


def generate_empowering_video(audio_filename, images_urls):
    # Load the audio and image clips
    audio = AudioFileClip(audio_filename)
    duration_per_image = audio.duration / len(images_urls)
    clips = []

    for image_url in images_urls:
        # Load the image and add a Ken Burns zoom effect
        image = ImageClip(image_url)
        zoom_factor = 1.2
        zoom_duration = duration_per_image * 0.9
        zoomed_image = image.resize(lambda t: 1 + (zoom_factor - 1) * t)
        zoomed_image = CompositeVideoClip([zoomed_image], size=image.size)
        zoomed_image = zoomed_image.set_start(0).set_end(zoom_duration)
        zoomed_image = zoomed_image.set_position('center')
        zoomed_image = zoomed_image.set_duration(duration_per_image)

        # Add the zoomed image clip to the list of clips
        clips.append(zoomed_image)

    # Concatenate the clips and set the audio
    final_clip = concatenate_videoclips(clips).set_audio(audio)
    final_clip.fps = 24

    # Write the final clip to a file
    final_clip.write_videofile("output.mp4")


# def generate_empowering_video(audio_filename, images_urls):
#     # Load the audio and image clips
#     audio = AudioFileClip(audio_filename)
#     duration_per_image = audio.duration / len(images_urls)
#     clips = [ImageClip(image_url).set_duration(duration_per_image)
#              for image_url in images_urls]

#     # Concatenate the clips and set the audio
#     final_clip = concatenate_videoclips(clips).set_audio(audio)
#     final_clip.fps = 24
#     # Write the final clip to a file
#     final_clip.write_videofile("output.mp4")

generate_empowering_video("temp.mp3", images)
