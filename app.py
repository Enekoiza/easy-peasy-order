from flask import Flask, render_template, request, jsonify, redirect, url_for
import pyaudio
import wave
from google.cloud import speech
import os
import io
import DBConnection

app = Flask(__name__)

@app.route("/")
def home():
    search = request.args.get('search')
    return render_template('index.html', micro=search)

@app.route("/generate")
def generate():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 4
    filename = "/Users/enekoiza/Desktop/easy-peasy/test2.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'w')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/enekoiza/Desktop/easy-peasy/Credentials.json'


    # Creates google client
    client = speech.SpeechClient()

    # Full path of the audio file, Replace with your file name
    file_name = os.path.join(os.path.dirname(__file__),"test2.wav")

    #Loads the audio file into memory
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=1,
        language_code="en-gb",
        speech_contexts = [{"phrases" : ["birra moretti", "heineken", "thatchers gold"]}]
        
    )

    # Sends the request to google to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})

    print(response.results)
# ("Transcript: {}".format(result.alternatives[0].transcript))

    # Reads the response
    for result in response.results:
        return redirect(url_for('home', search = result.alternatives[0].transcript))
    

@app.route("/ajaxlivesearch", methods=["POST", "GET"])
def ajaxlivesearch():
    conn = DBConnection.databaseConnection()
    cursor = conn.cursor()
    if request.method == 'POST':
        if 'query' in request.form:
            search_word = request.form['query']
            print(search_word)
            query = "SELECT * FROM PRODUCT WHERE PRODUCT_NAME LIKE '%{}%' OR RELATED_WORDS LIKE '%{}%'".format(search_word, search_word)
            cursor.execute(query)
            product = cursor.fetchall()
            return jsonify({'htmlresponse': render_template('response.html', product=product)})
        else:
            query = 'SELECT * FROM PRODUCT'
            cursor.execute(query)
            product = cursor.fetchall()
            return jsonify({'htmlresponse': render_template('response.html', product=product)})
    return jsonify('success')
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9000)