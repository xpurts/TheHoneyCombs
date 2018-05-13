#!/usr/bin/env python

#################################################################
# Google Cloud Speech API  application using the streaming API. #
#                                                               #
# Example usage:                                                #
#    python transcribe_streaming_mic.py                         #
#################################################################

# [START import_libraries]
from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from settings import RATE, CHUNK, sttClient, sttStreamingConfig

import pyaudio
from six.moves import queue
# [END import_libraries]




class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        # The API currently only supports 1-channel (mono) audio
        # The audio stream is being run asynchronously to fill the buffer object.
        # This is necessary so that the input device's buffer doesn't
        # overflow while the calling thread makes network requests.
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        # Continuously collect data from the audio stream, into the buffer.
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]


def listen_print_loop(responses):
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Store the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Store interim results, but with a carriage return at the end of the
        # line.
        #
        # If the previous result was longer than this one, we need to store
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            #sys.stdout.write(transcript + overwrite_chars + '\r')
            #sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.

            # if re.search(r'\b(how are you)\b', transcript, re.I):
            #     print('Exiting..')
            #     break

            num_chars_printed = 0

            return transcript + overwrite_chars


def processCurrentRequest():
    #todo: move to settings

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = sttClient.streaming_recognize(sttStreamingConfig, requests)

        # Now, put the transcription responses to use.
        return listen_print_loop(responses)
