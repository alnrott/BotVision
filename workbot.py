from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
import time
from flask import Flask, jsonify, render_template, request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import threading
import base64


app = Flask(__name__ , template_folder='templates')
status = "OFF.."

def browser():
    global driver
    options = webdriver.ChromeOptions()
    # to supress the error messages/logs
    options.add_argument(f'--user-data-dir=C:/Users/alanr/AppData/Local/Google/Chrome/User Data/Profile 6')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver
        
def login_wsp():
    driver.get("https://web.whatsapp.com/")
    print("SE DEBERIA LOGGEAR")
    canvas = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME , ("canvas"))))
    canvas_png = canvas.screenshot_as_png
    with open("QR-code.jpg", "wb") as f:
        f.write(canvas_png)
    

def run_bot():
    global status
    global driver
    # cargamos los datos del navegador
    status = ("El bot está ejecutándose..")
    driver = browser()
    login_wsp()
    
    
    time.sleep(20)
    status = ("El bot está por terminar")

    detenerBOT()


@app.route("/obtenerQR")
def obtenerQR():
    with open("QR-code.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return jsonify({"QR": encoded_string})
    # Devuelve el estado del bot como una respuesta JSON


@app.route("/detenerBOT")
def detenerBOT():
    status = "BOT OFF"
    driver.close()
    return jsonify(status=status)


@app.route("/status")
def get_status():
    # Devuelve el estado del bot como una respuesta JSON
    return jsonify(status=status)

@app.route("/", methods=["GET", "POST"])
def index():
    global status
    if request.method == "POST":
        run_bot()
        return jsonify(status=status)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run()    
