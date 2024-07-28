import io
import base64
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import yfinance as yf
import threading
import time


class RealTimeUpdater:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
        self.plot_url = None
        self.update_interval = 60  # Güncellemeler arasında geçen süre (saniye)

    def fetch_and_forecast(self):
        while True:
            try:
                # Veriyi indir
                self.data = yf.download(self.symbol, period='1y', interval='1d')
                self.data = self.data[['Close']]

                # Eksik günleri doldur
                self.data = self.data.resample('D').ffill()

                # ARIMA modelini oluştur ve eğit
                model = ARIMA(self.data['Close'], order=(5, 1, 0))
                model_fit = model.fit()

                # Tahmin yap
                forecast = model_fit.forecast(steps=30)
                forecast_index = pd.date_range(start=self.data.index[-1], periods=30, freq='D')

                # Grafiği oluştur
                plt.figure(figsize=(10, 6))
                plt.plot(self.data['Close'], label='Historical Data')
                plt.plot(forecast_index, forecast, label='Forecast', color='red')
                plt.title(f'Stock Price Prediction for {self.symbol}')
                plt.xlabel('Date')
                plt.ylabel('Close Price')
                plt.legend()

                # Grafiği kaydet ve base64 formatında dön
                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                self.plot_url = base64.b64encode(img.getvalue()).decode()
                plt.close()  # Kaynakları serbest bırak
            except Exception as e:
                print(f"Error: {e}")

            time.sleep(self.update_interval)  # Güncellemeler arasında bekle

    def start_update_thread(self):
        update_thread = threading.Thread(target=self.fetch_and_forecast)
        update_thread.daemon = True
        update_thread.start()
