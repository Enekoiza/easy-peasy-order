from crypt import methods
from functools import lru_cache
from sqlite3 import Cursor
from types import MethodDescriptorType
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, session
from flask_session import Session
from playsound import playsound
import gtts
import mysql.connector
import pyaudio
import wave
from google.cloud import speech
import os
import io



def databaseConnection():
  conn = mysql.connector.connect(user='root', password='argider_12',
                              host='127.0.0.1', port=3306, database='EASYPEASY',
                              auth_plugin='mysql_native_password')

  return conn

def getProductID(productName):
    conn = databaseConnection()
    cursor= conn.cursor()
    query = "SELECT product_id FROM PRODUCT WHERE product_name = %s"
    cursor.execute(query, (productName,))
    result = cursor.fetchone()
    conn.close()
    return result[0]

def getProductName(id):
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT product_name FROM PRODUCT WHERE product_id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    conn.close()
    return result[0]

def getLiveProducts():
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT product_name FROM PRODUCT WHERE live=1"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def getNonLiveProducts():
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT product_name FROM PRODUCT WHERE live=0"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def getLiveLanguages():
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT country FROM LANGUAGE WHERE live=1"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def getNonLiveLanguages():
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT country FROM LANGUAGE WHERE live=0"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def getAllProductsMeasures():
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT product_name, measure FROM PRODUCT"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def home():
    conn = databaseConnection()
    cursor = conn.cursor()
    query1 = "SELECT * FROM LANGUAGE WHERE live=1"
    cursor.execute(query1)
    results = cursor.fetchall()
    search = request.args.get('search')
    confidence = request.args.get('confidence')
    voicequantity = request.args.get('quantityvoice')
    if voicequantity:
        voicequantity = (int(voicequantity))
        return render_template('index.html', quantityvoice=voicequantity, confidence=confidence, results = results)
    return render_template('index.html', voiceResponse=search, confidence=confidence, results = results)

@app.route("/admin")
def admin():
    if session.get('logout'):
        session['login'] = None

    if session.get('login'):        
        products = getLiveProducts()
        no_products = getNonLiveProducts()
        languages = getLiveLanguages()
        no_languages = getNonLiveLanguages()
        product_measures = getAllProductsMeasures()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures)

    return render_template('admin.html')

@app.route('/logout')
def logout():
    session['logout'] = 1
    return redirect(url_for('admin'))

@app.route("/admin_dashboard", methods=['POST', 'GET'])
def dashboard():
    error = 'ERROR'
    username = request.form.get('admin-login')
    password = request.form.get('admin-password')
    conn = databaseConnection()
    cursor = conn.cursor()
    query3 = "SELECT COUNT(*) FROM ADMINLOGIN WHERE username = %s AND password = %s"
    cursor.execute(query3, (username, password,))
    results = cursor.fetchone()
    if results[0] == 1:
        session['login'] = username
        products = getLiveProducts()
        no_products = getNonLiveProducts()
        languages = getLiveLanguages()
        no_languages = getNonLiveLanguages()
        product_measures = getAllProductsMeasures()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures)
    elif session.get('login'):
        products = getLiveProducts()
        no_products = getNonLiveProducts()
        languages = getLiveLanguages()
        no_languages = getNonLiveLanguages()
        product_measures = getAllProductsMeasures()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures)
    else:
        return render_template('admin.html', error=error)

@app.route("/updatinglivedata", methods=['POST', 'GET'])
def update():
    updated_value = request.form.get('live-products')
    print(updated_value)

    products = getLiveProducts()
    no_products = getNonLiveProducts()
    languages = getLiveLanguages()
    no_languages = getNonLiveLanguages()
    product_measures = getAllProductsMeasures()

    if updated_value == None:
        error = 'An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)    

    try:
        conn = databaseConnection()
        cursor = conn.cursor()
        query = "UPDATE PRODUCT SET live=0 WHERE product_name=%s"
        cursor.execute(query,(updated_value,))
        conn.commit()
        conn.close()
        message = 'The product has been succesfully removed from the list.'
        products = getLiveProducts()
        no_products = getNonLiveProducts()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, message=message)

    except:
        error='An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)


    

@app.route("/updatingnolivedata", methods=['POST', 'GET'])
def update1():
    updated_value = request.form.get('non-live-products')
    print(updated_value)
    
    
    products = getLiveProducts()
    no_products = getNonLiveProducts()
    product_measures = getAllProductsMeasures()
    languages = getLiveLanguages()
    no_languages = getNonLiveLanguages()

    if updated_value == None:
        error = 'An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)



    try:
        conn = databaseConnection()
        cursor = conn.cursor()
        query = "UPDATE PRODUCT SET live=1 WHERE product_name=%s"
        cursor.execute(query,(updated_value,))
        conn.commit()
        conn.close()
        message = 'The product has been successfully added to the list.'
        products = getLiveProducts()
        no_products = getNonLiveProducts()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, message=message)

    except:
        error = 'An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)



@app.route("/createnewproduct", methods=["POST", "GET"])
def create_new():
    product_name = request.form.get('product-name')
    related_words = request.form.get('related-words')
    cost = request.form.get('product-cost')
    measure = request.form.get('measure')
    imageURL = request.form.get('imageURL')


    products = getLiveProducts()
    no_products = getNonLiveProducts()
    languages = getLiveLanguages()
    no_languages = getNonLiveLanguages()
    product_measures = getAllProductsMeasures()


    try:
        conn = databaseConnection()
        cursor = conn.cursor()
        query = "INSERT INTO `PRODUCT` (product_name, related_words, cost, live, measure, imageURL) VALUES (%s, %s , %s, 1, %s, %s);"
        cursor.execute(query,(product_name, related_words, cost, measure, imageURL,))
        conn.commit()
        conn.close()
        message = 'The product has been successfully added to the list of products.'
        products = getLiveProducts()
        product_measures = getAllProductsMeasures()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, message=message)

    except:
        error = "Sorry you can't submit a replicated value"
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, error=error, product_measures=product_measures)

@app.route("/changeproductcost", methods=["POST", "GET"])
def change_cost():
    new_cost = request.form.get('cost-change')
    product_name = request.form.get('product-measure-selection')


    list = product_name.split()

    product_name = list[0]
    measure = list[1]

    products = getLiveProducts()
    no_products = getNonLiveProducts()
    languages = getLiveLanguages()
    no_languages = getNonLiveLanguages()
    product_measures = getAllProductsMeasures()

    try:
        conn = databaseConnection()
        cursor = conn.cursor()
        query = "UPDATE PRODUCT SET cost=%s WHERE product_name=%s AND measure = %s"
        cursor.execute(query, (new_cost, product_name, measure,))
        conn.commit()
        conn.close()
        message = 'The cost has been successfully changed.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, message=message)
    except:
        error = 'An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)

@app.route("/addnewlanguage", methods=["POST", "GET"])
def add_language():
    new_language = request.form.get('non-live-languages')

    products = getLiveProducts()
    no_products = getNonLiveProducts()
    languages = getLiveLanguages()
    no_languages = getNonLiveLanguages()
    product_measures = getAllProductsMeasures()

    try:
        conn = databaseConnection()
        cursor = conn.cursor()
        query = "UPDATE LANGUAGE SET live=1 WHERE country=%s"
        cursor.execute(query, (new_language,))
        conn.commit()
        conn.close()
        message = 'The language code has been succesfully added to the list of available languages.'
        languages = getLiveLanguages()
        no_languages = getNonLiveLanguages()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, message=message)
    except:
        error = 'An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)




@app.route("/removelanguage", methods=["POST", "GET"])
def remove_language():
    removed_language = request.form.get('live-languages')

    products = getLiveProducts()
    no_products = getNonLiveProducts()
    languages = getLiveLanguages()
    no_languages = getNonLiveLanguages()
    product_measures = getAllProductsMeasures()
    try:
        conn = databaseConnection()
        cursor = conn.cursor()
        query = "UPDATE LANGUAGE SET live=0 WHERE country=%s"
        cursor.execute(query, (removed_language,))
        conn.commit()
        conn.close()
        message = 'The language code has been succesfully removed from the list of available languages.'
        languages = getLiveLanguages()
        no_languages = getNonLiveLanguages()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, message=message)
    except:
        error = 'An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)

@app.route("/loading")
def loading():
    return render_template('loading.html')

@app.route("/generate", methods=['POST', 'GET'])
def generate():
    language_code = request.form.get('language-holder')
    print(language_code)

    conn = databaseConnection()
    cursor = conn.cursor()
    query2 = "SELECT * FROM LANGUAGE WHERE country= %s"
    cursor.execute(query2, (language_code,))
    language = cursor.fetchone()
    print(language[1])

    language_code = language[1]




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
        language_code=language_code,
        speech_contexts = [{"phrases" : ["birra moretti", "heineken", "thatchers gold"]}]
        
    )

    # Sends the request to google to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})

    if not response.results:
        return redirect(url_for('home', search = 'ERROR'))

    print(response.results)

    for result in response.results:
        confidence = result.alternatives[0].confidence

    print(confidence)
# ("Transcript: {}".format(result.alternatives[0].transcript))
    # Reads the response
    for result in response.results:
        return redirect(url_for('home', search = result.alternatives[0].transcript, confidence = confidence))
    

#A view to return the data when the input search changes
@app.route("/ajaxlivesearch", methods=["POST", "GET"])
def ajaxlivesearch():
    conn = databaseConnection()
    cursor = conn.cursor()
    if request.method == 'POST':
        #When the search bar input has a value different to ""
        if 'query' in request.form:
            search_word = request.form['query']
            print(search_word)
            query = "SELECT * FROM PRODUCT WHERE live=1 AND PRODUCT_NAME LIKE '%{}%' OR live=1 AND RELATED_WORDS LIKE '%{}%' OR live=1 AND MEASURE LIKE '%{}%'".format(search_word, search_word, search_word)
            cursor.execute(query)
            product = cursor.fetchall()
            return jsonify({'htmlresponse': render_template('response.html', product=product)})
        #When the search bar input has a value "" which means get all the items alive
        else:
            query = 'SELECT * FROM PRODUCT WHERE live=1'
            cursor.execute(query)
            product = cursor.fetchall()
            print(product)
            return jsonify({'htmlresponse': render_template('response.html', product=product)})
    return jsonify('ERROR')

@app.route("/neworder", methods=["POST", "GET"])
def create_order():
    count = request.form.get('product-count')
    product = []
    productValue = []
    for i in range(0,int(count)):
        productName = "product" + str(i)
        productValueName = "product-value" + str(i)
        productholder = request.form.get(productName)
        productValueHolder = request.form.get(productValueName)
        productValue.append(productValueHolder)
        product.append(productholder)
    
    print(product)


    conn = databaseConnection()
    cursor = conn.cursor()
    checkOrderCount = "SELECT COUNT(*) FROM ORDERS"
    cursor.execute(checkOrderCount)
    noOrder = cursor.fetchone()
    print(noOrder[0])
    nextOrder = int(noOrder[0]) + 1
    print('the next order is: ', nextOrder)
    nextOrderQuery = "INSERT INTO ORDERS (OrderNo) VALUES (%s)"
    cursor.execute(nextOrderQuery, (nextOrder,))
    conn.commit()


    for i in range(0, int(count)):
        query = "INSERT INTO ORDERS_PRODUCTS (OrderNo, Product_id, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query, (nextOrder, getProductID(product[i]), productValue[i],))
    
    conn.commit()


    return redirect(url_for('home'))


@app.route("/order_dashboard", methods=["POST", "GET"])
def order_dashboard():

    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT MAX(OrderNo) FROM ORDERS_PRODUCTS"
    cursor.execute(query)
    maxOrders = cursor.fetchone()
    maxOrders = maxOrders[0]

    if maxOrders == None:
        products = getLiveProducts()
        no_products = getNonLiveProducts()
        languages = getLiveLanguages()
        no_languages = getNonLiveLanguages()
        product_measures = getAllProductsMeasures()

        message = "There are no orders to show"
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, message=message)

    orders = dict()

    orderHolder = [dict() for _ in range(maxOrders)] 

    for i in range(1, int(maxOrders) + 1):
        query = "SELECT product_id, quantity FROM ORDERS_PRODUCTS WHERE OrderNo = %s"
        cursor.execute(query, (i,))
        result = cursor.fetchall()

        listLen = len(result)
        
        


        for y in range (0, int(listLen)):
            key = getProductName(result[y][0])
            value = result[y][1]
            orderHolder[i - 1][key] = value

        orders[i] = orderHolder[i-1]


    return render_template('order_dashboard.html', orders = orders)

@app.route("/welcomemessage", methods=["POST", "GET"])
def welcomemessage():
    return send_from_directory('static/audio', 'welcome.mp3')

@app.route("/selectvoicequantity", methods=["POST", "GET"])
def quantityvoice():


    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 4
    filename = "/Users/enekoiza/Desktop/easy-peasy/test3.wav"

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
    file_name = os.path.join(os.path.dirname(__file__),"test3.wav")

    #Loads the audio file into memory
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=1,
        language_code="en-GB"
    )

    # Sends the request to google to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})
    print(response.results)


    if not response.results:
        return redirect(url_for('home', search = 'ERROR'))


    for result in response.results:
        confidence = result.alternatives[0].confidence

    print(confidence)
# ("Transcript: {}".format(result.alternatives[0].transcript))
    # Reads the response
    print(result.alternatives[0].transcript)
    for result in response.results:
        return redirect(url_for('home', quantityvoice = result.alternatives[0].transcript, confidence = confidence, quantityFlag = 'allow' ))


    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)