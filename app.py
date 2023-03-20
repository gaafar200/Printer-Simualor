from flask import Flask, render_template, request, redirect, session,url_for
import Printer
import time
app = Flask(__name__)
printer = Printer.Printer.getInstance()
@app.get('/')
def index():
    return render_template("main.html")
@app.post("/print")
def print():
    text = request.form['text']
    key =  printer.print(text)
    redircted_url = "/status/" + str(key) 
    return redirect(redircted_url)
@app.get("/test")
def test():
    return printer.getAllPrintOperation()
@app.get("/status/<string:key>")
def status(key):
    return printer.getPrintStatus(key)
        
if __name__ == "__main__":
    app.run(debug=True)