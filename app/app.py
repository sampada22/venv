import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template,request,make_response,send_file
from io import BytesIO 
app = Flask(__name__)
import sqlite3

def get_Data():
    conn = sqlite3.connect("C:/Users/Sampada Dhakal/venv/app/forecast.db")
    curs = conn.cursor()
    for row in curs.execute("SELECT * FROM TODO"):
        humidity = row[1]
        temp_in_C = row[2]
        temp_in_F = row[3]
        heatIndex_in_C = row[4]
        heatIndex_in_F = row[5]
    conn.close()
    return humidity,temp_in_C,temp_in_F,heatIndex_in_C,heatIndex_in_F

def get_HistoricalData():
    conn = sqlite3.connect("C:/Users/Sampada Dhakal/venv/app/forecast.db")
    curs = conn.cursor()
    curs.execute("SELECT * FROM todo ")
    data = curs.fetchall()
    a_Hum = []
    a_Temp = []
    a_heatIndex = []

    for row in reversed(data):
        a_Hum.append(row[0])
        a_Temp.append(row[1])
        a_heatIndex.append(row[2])
    return a_Hum, a_Temp,a_heatIndex

def max_RowsTable():
    conn = sqlite3.connect("C:/Users/Sampada Dhakal/venv/app/forecast.db")
    curs = conn.cursor()
    for row in curs.execute("SELECT COUNT(temp_in_C) FROM todo"):
        maxNumberRows = row[0]
    return maxNumberRows

global num_Samples 
num_Samples = max_RowsTable()
if (num_Samples > 101):
    num_Samples = 100


@app.route('/')
def profile():
    humidity,temp_in_C,temp_in_F,heatIndex_in_C,heatIndex_in_F = get_Data()
    template_Data = {
        'humidity' : humidity,
        'temp_in_C' :temp_in_C,
        'temp_in_F' : temp_in_F,
        'heatIndex_in_C' : heatIndex_in_C,
        'heatIndex_in_F' : heatIndex_in_F
    }
    return render_template('profile2.html', **template_Data)

@app.route('/plot/hum')
def plot_Hum():
    a_Hum, a_Temp, a_heatIndex = get_HistoricalData()
    ys = a_Hum
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    axis.set_title ("Humidity in %")
    axis.set_xlabel("Samples")
    axis.grid(False)
    xs = range(num_Samples)
    axis.plot(xs,ys)
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = "image/png"
    return response

@app.route('/plot/temp')
def plot_Temp():
    a_Hum, a_Temp, a_heatIndex = get_HistoricalData()
    ys = a_Temp
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    axis.set_title ("Temperature in degree Celsius")
    axis.set_xlabel("Samples")
    axis.grid(False)
    xs = range(num_Samples)
    axis.plot(xs,ys)
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = "image/png"
    return response

@app.route('/plot/heatIndex')
def plot_heatIndex():
    a_Hum, a_Temp, a_heatIndex = get_HistoricalData()
    ys = a_heatIndex
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    axis.set_title ("Heat Index in Farenheit")
    axis.set_xlabel("Samples")
    axis.grid(False)
    xs = range(num_Samples)
    axis.plot(xs,ys)
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = "image/png"
    return response



if __name__ == '__main__':
    app.debug = True
    app.run()
