from elevenlabs.api import Voices, Voice, VoiceSettings
from elevenlabs import set_api_key, save, generate
import os
from dotenv import load_dotenv
load_dotenv()
set_api_key(os.getenv('XI_API_KEY'))


def create_voiceover_from_text(script, voice_name="clone/Nate Baker - Clear"):
    # generate an audio object
    voice = Voice(voice_id='f4WyhCVmdkKp3QoMbjdW', name='Nate Baker - Clear',
                  category='cloned', settings=VoiceSettings(stability=0.65, similarity_boost=0.65))
    audio = generate(
        text=script,
        voice=voice,
        model="eleven_monolingual_v1"
    )
    filename = "./temp.mp3"
    # save the audio
    save(audio, filename)
    return filename


def get_all_voices():
    voices = Voices.from_api()

    return (voices)
