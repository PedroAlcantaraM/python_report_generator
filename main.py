import os
from dotenv import load_dotenv
import pandas as pd
import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import smtplib
from email.message import EmailMessage


actives = ["^BVSP", "BRL=X"]

today = datetime.datetime.now()

last_year = today - datetime.timedelta(days=365)

trading_data = yf.download(actives, last_year, today)

trading_data_close = trading_data["Adj Close"]

trading_data_close.columns = ["Dolar", "IBOVESPA"]

trading_data_close = trading_data_close.dropna()

trading_data_close_monthly = trading_data_close.resample("M").last()

trading_data_close_yearly = trading_data_close.resample("Y").last()

year_trading_return = trading_data_close_yearly.pct_change().dropna()

month_trading_return = trading_data_close_monthly.pct_change().dropna()

day_trading_return = trading_data_close.pct_change().dropna()

dollar_day_trading_return = day_trading_return.iloc[-1, 0]
ibov_day_trading_return = day_trading_return.iloc[-1, 1]

dollar_month_trading_return = month_trading_return.iloc[-1, 0]
ibov_month_trading_return = month_trading_return.iloc[-1, 1]

dollar_year_trading_return = year_trading_return.iloc[-1, 0]
ibov_year_trading_return = year_trading_return.iloc[-1, 1]


def round_data(list):
    rounded_list = [round(data * 100, 2) for data in list]
    return rounded_list


data_list = round_data(
    [
        dollar_day_trading_return,
        ibov_day_trading_return,
        dollar_month_trading_return,
        ibov_month_trading_return,
        dollar_year_trading_return,
        ibov_year_trading_return,
    ]
)

[
    dollar_day_trading_return,
    ibov_day_trading_return,
    dollar_month_trading_return,
    ibov_month_trading_return,
    dollar_year_trading_return,
    ibov_year_trading_return,
] = data_list

plt.style.use("cyberpunk")

trading_data_close.plot(y="IBOVESPA", use_index=True, legend=False)

plt.title("Ibovespa")

plt.savefig("ibovespa.png", dpi=300)

plt.style.use("cyberpunk")

trading_data_close.plot(y="Dolar", use_index=True, legend=False)

plt.title("Dollar")

plt.savefig("dollar.png", dpi=300)

load_dotenv()

password = os.environ.get("PASSWORD")

email = "pedroalcan123@gmail.com"

msg = EmailMessage()

msg["Subject"] = "Enviando relatório com Python"

msg["From"] = email

msg["To"] = "brenno@varos.com.br"

msg.set_content(
    f"""Prezado diretor, segue o relatório diário:

Bolsa:

No ano o Ibovespa está tendo uma rentabilidade de {ibov_year_trading_return}%, 
enquanto no mês a rentabilidade é de {ibov_month_trading_return}%.

No último dia útil, o fechamento do Ibovespa foi de {ibov_day_trading_return}%.

Dólar:

No ano o Dólar está tendo uma rentabilidade de {dollar_year_trading_return}%, 
enquanto no mês a rentabilidade é de {dollar_month_trading_return}%.

No último dia útil, o fechamento do Dólar foi de {dollar_day_trading_return}%.


Abs,

O melhor estagiário do mundo

"""
)

with open("dollar.png", "rb") as content_file:
    content = content_file.read()
    msg.add_attachment(
        content, maintype="application", subtype="png", filename="dollar.png"
    )


with open("ibovespa.png", "rb") as content_file:
    content = content_file.read()
    msg.add_attachment(
        content, maintype="application", subtype="png", filename="ibovespa.png"
    )

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

    smtp.login(email, password)
    smtp.send_message(msg)
