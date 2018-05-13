from google.cloud import texttospeech
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


#####################################
# Algorithm Surface Matrix Settings #
#####################################
width = 3
height = 3
firstPinNumber = 1

SurfaceMapping = [[0 for x in range(width)] for y in range(height)]
for i in range(width):
    for j in range(height):
        SurfaceMapping[i][j] = firstPinNumber
        firstPinNumber += 1

SurfaceState = [[0 for x in range(width)] for y in range(height)]

gridWidth = "." * width
grid = []

###########################
# Text-to-speech Settings #
###########################

# Example: configureTtsAudioConfig(texttospeech.enums.AudioEncoding.MP3)
def configureTtsAudioConfig(audioConfig):
    return texttospeech.types.AudioConfig(
        audio_encoding=audioConfig)

# Example: configureTtsVoice('ro-RO', texttospeech.enums.SsmlVoiceGender.FEMALE)
def configureTtsVoice(languageCode, ssmlGender):
    return texttospeech.types.VoiceSelectionParams(
        language_code=languageCode,
        ssml_gender=ssmlGender)

# Variables
ttsVoice       = configureTtsVoice('en-US', texttospeech.enums.SsmlVoiceGender.FEMALE)
ttsClient      = texttospeech.TextToSpeechClient()
ttsAudioConfig = configureTtsAudioConfig(texttospeech.enums.AudioEncoding.MP3)


##############################
# Audio recording parameters #
##############################
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


###########################
# Speech-to-text Settings #
###########################
sttLanguageCode = 'en-US'
sttClient = speech.SpeechClient()

sttConfig = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code=sttLanguageCode)
sttStreamingConfig = types.StreamingRecognitionConfig(
    config=sttConfig,
    interim_results=True)
