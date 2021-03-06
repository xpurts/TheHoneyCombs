#!/usr/bin/env python

################################################
# Google Cloud Text-To-Speech API application .#
#                                              #
# Example usage:                               #
#   python synthesize_text.py --text "hello"   #
################################################

import argparse
from settings import ttsClient, ttsVoice, ttsAudioConfig
from google.cloud import texttospeech
import playsound
import os

outputIndex = 0

# [START tts_synthesize_text]
def synthesize_text(text):
    global outputList
    global outputIndex

    input_text = texttospeech.types.SynthesisInput(text=text)
    
    response = ttsClient.synthesize_speech(input_text, ttsVoice, ttsAudioConfig)

    with open("output"+str(outputIndex)+".mp3", 'wb') as out:
        out.write(response.audio_content)
    
    play_message("output"+str(outputIndex)+".mp3")
# [END tts_synthesize_text]


# [START tts_play_message]
def play_message(message):
    global outputIndex
    playsound.playsound("output"+str(outputIndex)+".mp3")
    try:
        os.remove("output"+str(outputIndex)+".mp3")
    except OSError:
        pass
    outputIndex += 1
# [END tts_play_message]


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         description=__doc__,
#         formatter_class=argparse.RawDescriptionHelpFormatter)
#     group = parser.add_mutually_exclusive_group(required=True)
#     group.add_argument('--text',
#                        help='The text from which to synthesize speech.')

#     args = parser.parse_args()

#     synthesize_text(args.text)
