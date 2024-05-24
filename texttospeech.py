"""Synthesizes speech from the input string of text."""
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
# Note: the voice can also be specified by name.
# Names of voices can be retrieved with client.list_voices().
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Studio-M",
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    speaking_rate=1.5
)

def generateSpeech(text):
    input_text = texttospeech.SynthesisInput(ssml=text)
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    return response.audio_content