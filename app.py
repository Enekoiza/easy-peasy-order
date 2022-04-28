from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, session
from flask_session import Session
import mysql.connector
import pyaudio
import wave
from google.cloud import speech
import os
import io
import hashlib
import config


def databaseConnection():
    try:
        conn = mysql.connector.connect(user=config.username, password=config.password,
                              host=config.hostname, port=config.port, database='EASYPEASY',
                              auth_plugin='mysql_native_password')
        return conn
    except:
        return render_template('error.html')

  

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

#Function to return the live products
def getLiveProducts():
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT product_name FROM PRODUCT WHERE live=1"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

#Function to return the Non-live products
def getNonLiveProducts():
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT product_name FROM PRODUCT WHERE live=0"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

#Function to return the live languages
def getLiveLanguages():
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT country FROM LANGUAGE WHERE live=1"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

#Function to return the Non-live languages
def getNonLiveLanguages():
    conn = databaseConnection()
    cursor = conn.cursor()
    query = "SELECT country FROM LANGUAGE WHERE live=0"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

#Function to get all the product with their measures
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

#Index view
@app.route("/")
def home():
    conn = databaseConnection()
    #Check for database connection error
    try:
        cursor = conn.cursor()
    except:
        return render_template('error.html')
    query1 = "SELECT * FROM LANGUAGE WHERE live=1"
    cursor.execute(query1)
    results = cursor.fetchall()
    #Get the confidence and word from the speech-to-text conversion
    search = request.args.get('search')
    confidence = request.args.get('confidence')
    #return to index with the information passed through Jinja2
    return render_template('index.html', voiceResponse=search, confidence=confidence, results = results)

#Admin login view where the admin view is returned in case that the login session is not saved.
#Also logouts the session when the view is called by the button logout
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


#Return the admin dashboard if the entered details are correct or there is a session saved
@app.route("/admin_dashboard", methods=['POST', 'GET'])
def dashboard():
    error = 'Credentials needed'

    #There is a session saved
    if session.get('login'):
        products = getLiveProducts()
        no_products = getNonLiveProducts()
        languages = getLiveLanguages()
        no_languages = getNonLiveLanguages()
        product_measures = getAllProductsMeasures()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures)

    username = request.form.get('admin-login')
    password = request.form.get('admin-password')
    if username == None and password == None:
        return render_template('admin.html', error=error)
    hashedPassword = hashlib.sha256(password.encode()).hexdigest()
    conn = databaseConnection()
    try:
        cursor = conn.cursor()
    except:
        return render_template('error.html')
    query3 = "SELECT COUNT(*) FROM ADMINLOGIN WHERE username = %s AND password = %s"
    cursor.execute(query3, (username, hashedPassword,))
    results = cursor.fetchone()
    #The admin exists
    if results[0] == 1:
        session['login'] = username
        products = getLiveProducts()
        no_products = getNonLiveProducts()
        languages = getLiveLanguages()
        no_languages = getNonLiveLanguages()
        product_measures = getAllProductsMeasures()
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures)
    

    #An error happened
    else:
        return render_template('admin.html', error=error)


#Change the live option to 0 to make it invisible to the user
@app.route("/updatinglivedata", methods=['POST', 'GET'])
def update_non_live_data():
    updated_value = request.form.get('live-products')
    print(updated_value)

    products = getLiveProducts()
    no_products = getNonLiveProducts()
    languages = getLiveLanguages()
    no_languages = getNonLiveLanguages()
    product_measures = getAllProductsMeasures()

    #An error ocurred show it to the user
    if updated_value == None:
        error = 'An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)    

    try:
        conn = databaseConnection()
        try:
            cursor = conn.cursor()
        except:
            return render_template('error.html')
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


    
#Change the live option to 1 to make the it visibe to the user
@app.route("/updatingnolivedata", methods=['POST', 'GET'])
def update_live_product():
    updated_value = request.form.get('non-live-products')
    print(updated_value)
    
    
    products = getLiveProducts()
    no_products = getNonLiveProducts()
    product_measures = getAllProductsMeasures()
    languages = getLiveLanguages()
    no_languages = getNonLiveLanguages()
    
    #An error ocurred show it to the user
    if updated_value == None:
        error = 'An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)

    try:
        conn = databaseConnection()
        try:
            cursor = conn.cursor()
        except:
            return render_template('error.html')
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


#Create a new product that has never been in the database
@app.route("/createnewproduct", methods=["POST", "GET"])
def create_new():
    product_name = request.form.get('product-name')
    related_words = request.form.get('related-words')
    cost = request.form.get('product-cost')
    measure = request.form.get('measure')
    imageURL = request.form.get('imageURL')

    cost = round(cost, 2)

    products = getLiveProducts()
    no_products = getNonLiveProducts()
    languages = getLiveLanguages()
    no_languages = getNonLiveLanguages()
    product_measures = getAllProductsMeasures()


    try:
        conn = databaseConnection()
        try:
            cursor = conn.cursor()
        except:
            return render_template('error.html')
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

#Change the cost of a product that is in the database
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
        
        try:
            cursor = conn.cursor()
        except:
            return render_template('error.html')
        query = "UPDATE PRODUCT SET cost=%s WHERE product_name=%s AND measure = %s"
        cursor.execute(query, (new_cost, product_name, measure,))
        conn.commit()
        conn.close()
        message = 'The cost has been successfully changed.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, message=message)
    except:
        error = 'An error ocurred, if it persists contact the administrator.'
        return render_template('admin-dashboard.html', products = products, no_products=no_products, languages = languages, no_languages=no_languages, product_measures=product_measures, error=error)

#Make a language available for the user to choose
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
        try:
            cursor = conn.cursor()
        except:
            return render_template('error.html')
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



#Make a language unavailable for the user to choose
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
        try:
            cursor = conn.cursor()
        except:
            return render_template('error.html')
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

#View to redirect the system to loading.html
@app.route("/loading")
def loading():
    return render_template('loading.html')


#View that will record the audio from microphone and generate a transcript or an error
@app.route("/generate", methods=['POST', 'GET'])
def generate():
    #Get the language that the user has selected
    language_code = request.form.get('language-holder')

    conn = databaseConnection()
    try:
        cursor = conn.cursor()
    except:
        return render_template('error.html')
    query2 = "SELECT * FROM LANGUAGE WHERE country= %s"
    cursor.execute(query2, (language_code,))
    language = cursor.fetchone()


    language_code = language[1]

    #Record in chunks of 1024 samples
    chunk = 1024  
    #16 bits per sample
    sample_format = pyaudio.paInt16
    #Number of audio streams at once
    channels = 1
    #Record at 44100 samples per second
    fs = 44100
    #Record for 4 seconds  
    seconds = 4
    #Filename to save the audio input
    filename = "/Users/enekoiza/Desktop/easy-peasy/solution.wav"

    #Create an interface to PortAudio  
    p = pyaudio.PyAudio()

    #Create a stream and populate with the given values
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    # Initialize array to store frames
    frames = [] 

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()


    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'w')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    #Import into the operating system the Google Speech-to-text credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/enekoiza/Desktop/easy-peasy/Credentials.json'


    #Creates google client
    client = speech.SpeechClient()

    #Full path of the audio file, Replace with your file name
    file_name = os.path.join(os.path.dirname(__file__),"solution.wav")

    #Loads the audio file into memory
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    #Configuration for the convertion
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=1,
        language_code=language_code
    )

    #Sends the request to google to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})

    #There is no response return an error for the user to know
    if not response.results:
        return redirect(url_for('home', search = 'ERROR'))


    #Extract the confidence from the result
    for result in response.results:
        confidence = result.alternatives[0].confidence


    # Create a home redirection with the final data: transcript and confidence 
    for result in response.results:
        return redirect(url_for('home', search = result.alternatives[0].transcript, confidence = confidence))
    

#A view to return the data when the input search changes
@app.route("/ajaxlivesearch", methods=["POST", "GET"])
def ajaxlivesearch():
    conn = databaseConnection()
    try:
        cursor = conn.cursor()
    except:
        return render_template('error.html')
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
            return jsonify({'htmlresponse': render_template('response.html', product=product)})
    return jsonify('ERROR')


#View to generate a new order and insert the items from the paid basket into the database
@app.route("/neworder", methods=["POST", "GET"])
def create_order():
    #Get the count of products
    count = request.form.get('product-count')
    product = []
    productValue = []
    #Generate the product ids and request the information stored
    for i in range(0,int(count)):
        productName = "product" + str(i)
        productValueName = "product-value" + str(i)
        productholder = request.form.get(productName)
        productValueHolder = request.form.get(productValueName)
        productValue.append(productValueHolder)
        product.append(productholder)
    


    #Check for errors in database connection
    conn = databaseConnection()
    try:
        cursor = conn.cursor()
    except:
        return render_template('error.html')
    #Check the last order and generate a new one
    checkOrderCount = "SELECT COUNT(*) FROM ORDERS"
    cursor.execute(checkOrderCount)
    noOrder = cursor.fetchone()
    print(noOrder[0])
    nextOrder = int(noOrder[0]) + 1
    print('the next order is: ', nextOrder)
    nextOrderQuery = "INSERT INTO ORDERS (OrderNo) VALUES (%s)"
    cursor.execute(nextOrderQuery, (nextOrder,))
    conn.commit()

    #Insert the records into the table generated for the many to many relationship
    for i in range(0, int(count)):
        query = "INSERT INTO ORDERS_PRODUCTS (OrderNo, Product_id, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query, (nextOrder, getProductID(product[i]), productValue[i],))
    conn.commit()
    #Redirect to the home so the user can order again
    return redirect(url_for('home'))


@app.route("/order_dashboard", methods=["POST", "GET"])
def order_dashboard():

    error = "Credentials needed"

    if not session.get('login'):
        return render_template('admin.html', error=error)

    conn = databaseConnection()
    try:
        cursor = conn.cursor()
    except:
        return render_template('error.html')
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



    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)