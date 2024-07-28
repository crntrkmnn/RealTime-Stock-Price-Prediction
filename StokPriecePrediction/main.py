from flask import Flask, render_template
from realtime_updater import RealTimeUpdater

app = Flask(__name__)
updater = RealTimeUpdater('AAPL')  # Örnek olarak Apple'ın hisse senedi sembolü
updater.start_update_thread()  # Gerçek zamanlı güncellemeleri başlat

@app.route('/')
def index():
    return render_template('index.html', plot_url=updater.plot_url)

if __name__ == '__main__':
    app.run(debug=True)
