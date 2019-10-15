import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import time
import wave
import speech_sample
#import intent_sample
#import translation_sample

from collections import OrderedDict
import platform

"""
Speech recognition samples for the Microsoft Cognitive Services Speech SDK
"""



try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "7916f4ca06fc48e9a7edf6d3cc7e1dd9", "uksouth"

# Specify the path to an audio file containing speech (mono WAV / PCM with a sampling rate of 16
# kHz).
weatherfilename = "C:\\Users\\Anup.Kabra\\Documents\\Code\\Speechtotext\\cognitive-services-speech-sdk-master\\cognitive-services-speech-sdk-master\\samples\\csharp\\sharedcontent\\console\\whatstheweatherlike.wav"


def speech_recognize_once_from_mic():
    """performs one-shot speech recognition from the default microphone"""
    # <SpeechRecognitionWithMicrophone>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Creates a speech recognizer using microphone as audio input.
    # The default language is "en-us".
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Check the result
    #if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    #    print("Recognized: {}".format(result.text))
    #elif result.reason == speechsdk.ResultReason.NoMatch:
    #    print("No speech could be recognized")
    #elif result.reason == speechsdk.ResultReason.Canceled:
    #    cancellation_details = result.cancellation_details
     #   print("Speech Recognition canceled: {}".format(cancellation_details.reason))
     #   if cancellation_details.reason == speechsdk.CancellationReason.Error:
     #       print("Error details: {}".format(cancellation_details.error_details))
            
    return result
    # </SpeechRecognitionWithMicrophone>


def speech_recognize_once_from_file():
    """performs one-shot speech recognition with input from an audio file"""
    # <SpeechRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)
    # Creates a speech recognizer using a file as audio input.
    # The default language is "en-us".
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    # </SpeechRecognitionWithFile>


def speech_recognize_once_from_file_with_customized_model():
    """performs one-shot speech recognition with input from an audio file, specifying a custom
    model"""
    # <SpeechRecognitionUsingCustomizedModel>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Set the endpoint ID of your customized model
    # Replace with your own CRIS endpoint ID.
    speech_config.endpoint_id = "https://uksouth.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)
    # Creates a speech recognizer using a file as audio input.
    # The default language is "en-us".
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    # </SpeechRecognitionUsingCustomizedModel>


def speech_recognize_once_from_file_with_custom_endpoint_parameters():
    """performs one-shot speech recognition with input from an audio file, specifying an
    endpoint with custom parameters"""
    initial_silence_timeout_ms = 15 * 1e3
    template = "wss://{}.stt.speech.microsoft.com/speech/recognition" \
            "/conversation/cognitiveservices/v1?initialSilenceTimeoutMs={:d}"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,
            endpoint=template.format(service_region, int(initial_silence_timeout_ms)))
    print("Using endpoint", speech_config.get_property(speechsdk.PropertyId.SpeechServiceConnection_Endpoint))
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)
    # Creates a speech recognizer using a file as audio input.
    # The default language is "en-us".
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


def speech_recognize_async_from_file():
    """performs one-shot speech recognition asynchronously with input from an audio file"""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)
    # Creates a speech recognizer using a file as audio input.
    # The default language is "en-us".
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Perform recognition. `recognize_async` does not block until recognition is complete,
    # so other tasks can be performed while recognition is running.
    # However, recognition stops when the first utterance has bee recognized.
    # For long-running recognition, use continuous recognitions instead.
    result_future = speech_recognizer.recognize_once_async()

    print('recognition is running....')
    # Other tasks can be performed here...

    # Retrieve the recognition result. This blocks until recognition is complete.
    result = result_future.get()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


def speech_recognize_continuous_from_file():
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    # </SpeechContinuousRecognitionWithFile>

def speech_recognize_keyword_from_microphone():
    """performs keyword-triggered speech recognition with input microphone"""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an instance of a keyword recognition model. Update this to
    # point to the location of your keyword recognition model.
    model = speechsdk.KeywordRecognitionModel("YourKeywordRecognitionModelFile.table")

    # The phrase your keyword recognition model triggers on.
    keyword = "YourKeyword"

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_keyword_recognition()
        nonlocal done
        done = True

    def recognizing_cb(evt):
        """callback for recognizing event"""
        if evt.result.reason == speechsdk.ResultReason.RecognizingKeyword:
            print('RECOGNIZING KEYWORD: {}'.format(evt))
        elif evt.result.reason == speechsdk.ResultReason.RecognizingSpeech:
            print('RECOGNIZING: {}'.format(evt))

    def recognized_cb(evt):
        """callback for recognized event"""
        if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print('RECOGNIZED KEYWORD: {}'.format(evt))
        elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print('RECOGNIZED: {}'.format(evt))
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print('NOMATCH: {}'.format(evt))

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start keyword recognition
    speech_recognizer.start_keyword_recognition(model)
    print('Say something starting with "{}" followed by whatever you want...'.format(keyword))
    while not done:
        time.sleep(.5)

def speech_recognition_with_pull_stream():
    """gives an example how to use a pull audio stream to recognize speech from a custom audio
    source"""
    class WavFileReaderCallback(speechsdk.audio.PullAudioInputStreamCallback):
        """Example class that implements the Pull Audio Stream interface to recognize speech from
        an audio file"""
        def __init__(self, filename: str):
            super().__init__()
            self._file_h = wave.open(filename, mode=None)

            self.sample_width = self._file_h.getsampwidth()

            assert self._file_h.getnchannels() == 1
            assert self._file_h.getsampwidth() == 2
            assert self._file_h.getframerate() == 16000
            assert self._file_h.getcomptype() == 'NONE'

        def read(self, buffer: memoryview) -> int:
            """read callback function"""
            size = buffer.nbytes
            frames = self._file_h.readframes(size // self.sample_width)

            buffer[:len(frames)] = frames

            return len(frames)

        def close(self):
            """close callback function"""
            self._file_h.close()

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # specify the audio format
    wave_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16,
            channels=1)

    # setup the audio stream
    callback = WavFileReaderCallback(weatherfilename)
    stream = speechsdk.audio.PullAudioInputStream(callback, wave_format)
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    # instantiate the speech recognizer with pull stream input
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)


def speech_recognition_with_push_stream():
    """gives an example how to use a push audio stream to recognize speech from a custom audio
    source"""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # setup the audio stream
    stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    # instantiate the speech recognizer with push stream input
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    # The number of bytes to push per buffer
    n_bytes = 3200
    wav_fh = wave.open(weatherfilename)

    # start continuous speech recognition
    speech_recognizer.start_continuous_recognition()

    # start pushing data until all data has been read from the file
    try:
        while(True):
            frames = wav_fh.readframes(n_bytes // 2)
            print('read {} bytes'.format(len(frames)))
            if not frames:
                break

            stream.write(frames)
            time.sleep(.1)
    finally:
        # stop recognition and clean up
        wav_fh.close()
        stream.close()
        speech_recognizer.stop_continuous_recognition()

############# Use This

eofkey = 'Ctrl-Z' if "Windows" == platform.system() else 'Ctrl-D'

samples = OrderedDict([
    (speech_sample, [
        speech_sample.speech_recognize_once_from_mic,
        speech_sample.speech_recognize_once_from_file,
        speech_sample.speech_recognize_once_from_file_with_customized_model,
        speech_sample.speech_recognize_once_from_file_with_custom_endpoint_parameters,
        speech_sample.speech_recognize_async_from_file,
        speech_sample.speech_recognize_continuous_from_file,
        speech_sample.speech_recognition_with_pull_stream,
        speech_sample.speech_recognition_with_push_stream,
        speech_sample.speech_recognize_keyword_from_microphone,
    ])
])

import pyodbc
server = "demosampletoy.database.windows.net"
database = "Sample_Toy"
username = "toydebug"
password = 'Toy_access'
#driver = "{SQL Server Native Client 10.0}"
driver = "{ODBC Driver 17 for SQL Server}"
x = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
#conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
conn = pyodbc.connect(x)
mycursor = conn.cursor()

def select():
    #print('select sample module, {} to abort'.format(eofkey))
    modules = list(samples.keys())
    #for i, module in enumerate(modules):
    #    print("{}: {}\n\t{}".format(i, module.__name__, module.__doc__.strip()))

    try:
        #num = int(input())
        selected_module = modules[0]
    except EOFError:
        raise
    except Exception as e:
        #print(e)
        return

    #print('select sample function, {} to abort'.format(eofkey))
    #for i, fun in enumerate(samples[selected_module]):
    #    print("{}: {}\n\t{}".format(i, fun.__name__, fun.__doc__))

    try:
        #num = int(input())
        selected_function = samples[selected_module][0]
        
    except EOFError:
        raise
    except Exception as e:
        #print(e)
        return

    #print('You selected: {}'.format(selected_function))
    try:
        y = selected_function()
        final_msg = ""
         # Check the result
        if y.reason == speechsdk.ResultReason.RecognizedSpeech:
            final_msg = y.text
            #print("Recognized: {}".format(y.text))
        elif y.reason == speechsdk.ResultReason.NoMatch:
            final_msg = "No speech could be recognized"
            #print("No speech could be recognized")
        else:
            final_msg = "Some Error Occured"
        print(final_msg)
        
        query = "insert into voice_message (Msg) values ('"+final_msg+ "')"
        
        mycursor.execute(query)
        conn.commit()
    except Exception as e:
        print('Error running sample: {}'.format(e))

dash_app = dash.Dash(__name__)

app = dash_app.server

dash_app.config.suppress_callback_exceptions = True

dash_app.layout = html.Div([
    html.Button('Submit', id='button'),
    html.Div(id='container-button-basic')
])

@dash_app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])

def update_output(n_clicks):
    if n_clicks>0:
        select()
        
        

if __name__ == "__main__":
    dash_app.run_server()