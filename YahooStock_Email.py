# Using the yfinance library
from yfinance import Share
import smtplib

tickers = ['^GSPC', '^DJI', '^IXIC', 'UBS']

global Prices
Prices = []

global Change
Change = []

global today
today = date.today()

for ticker in tickers:
    last_price = yf.Ticker(ticker).fast_info.last_price        # Getting the last price
    Prices.append(last_price)  
    previous_price = yf.Ticker(ticker).fast_info.previous_close     # Getting previous market close
    change = round(100*(last_price - previous_price)/previous_price, 2) # Calculating % change and rounding to 2 d.p.
    Change.append(change)

# Function to send Emails
def send_mail(port, password, sender, recipients):
    context = ssl.create_default_context()    # Create a secure SSL context

    try:
        server = smtplib.SMTP('smtp.gmail.com',port=port)
        server.ehlo()
        server.starttls(context=context) # Secure the connection
        server.ehlo()
        server.login(sender, password)
        subject = 'BQG Daily Stock Price Update'
        body = '''Hello ,
                Today's data is from {0}
                Today's S&P 500 stock price is: {1} ({2}%)$
                Today's Dow Jones Industrial Average stock price is: {3} ({4}%)$
                Today's NASDAQ Composite stock price is: {5} ({6}%)$
                Today's UBS stock price is: {7} ({8}%)$ '''.format(today, Prices[0], Change[0], Prices[1], Change[1], Prices[2],  Change[2], Prices[3],  Change[3])
        msg = f"Subject: {subject}\n\n{body}"     
        
        server.sendmail(sender, recipients, msg)
        return "Email sent successfully."

    except smtplib.SMTPException as e:
       return f"Failed to send email: {e}"
    finally:
        server.quit() 


send_mail(port,'password', 'sender', ['recipient1'])
