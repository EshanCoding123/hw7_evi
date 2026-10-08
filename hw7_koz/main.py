from cmu_graphics import *
import requests
import os
import random
import math
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("TICKER_API_KEY")

PAGE = rgb(244, 247, 241)
INK = rgb(24, 43, 38)
MUTED = rgb(100, 119, 108)
GREEN = rgb(20, 121, 92)
MINT = rgb(218, 238, 226)
LIME = rgb(213, 235, 120)
CORAL = rgb(201, 83, 67)
WHITE = rgb(255, 255, 252)
RULE = rgb(219, 228, 218)

#start screen code
def onAppStart(app):
    app.background="black"
    app.money=10000
    app.time=480
    app.stepsPerSecond=1 
    app.date=0
    app.paused=False
    app.gameOver=False
    app.apiError=False
    app.scroll=0
    app.portfolioScroll=0
    #dictionary with key->ticker and current stock value adjusted per step
    app.stocks=None
    app.possessions=dict()
    
    #import requests

    #url = "https://api.tickerbot.io/v2/tickers/AAPL"
    #headers = { "Authorization": f"Bearer {api_key}" }

    #r = requests.get(url, headers=headers)
    #r.raise_for_status()
    #print(r.json())
    resetValues(app)
    
def resetValues(app):
    app.background="black"
    app.money=10000
    app.time=480
    app.stepsPerSecond=1 
    app.date=0
    app.paused=False
    app.gameOver=False
    app.apiError=False
    app.stocks=None
    app.scroll=0
    app.portfolioScroll=0
    app.possessions=dict()

def start_redrawAll(app):
    drawRect(0, 0, 400, 400, fill=PAGE)
    drawRect(0, 0, 400, 155, fill=INK)
    drawLabel("POCKET / STOCKS", 24, 24, align='left', fill=LIME,
              font='monospace', bold=True, size=11)
    drawLabel("PocketStocks", 24, 57, align='left', fill=WHITE,
              font='monospace', bold=True, size=26)
    drawLabel("One Week to Buy and Sell.", 24, 83, align='left', fill=MINT,
              font='monospace', size=13)
    drawLabel("BUY LOW", 24, 126, align='left', fill=WHITE,
              font='monospace', bold=True, size=10)
    drawLabel("SELL HIGH", 105, 126, align='left', fill=LIME,
              font='monospace', bold=True, size=10)
    chartPoints = [(260, 108), (282, 94), (304, 101), (326, 72),
                   (348, 82), (374, 50)]
    for index in range(len(chartPoints) - 1):
        drawLine(*chartPoints[index], *chartPoints[index + 1],
                 fill=LIME, lineWidth=3)
    for x, y in chartPoints:
        drawCircle(x, y, 3, fill=WHITE)

    drawLabel("Start with $10,000", 200, 169, fill=INK,
              font='monospace', bold=True, size=14)
    drawRect(100, 190, 200, 70, fill=GREEN)
    drawRect(100, 190, 200, 70, fill=None, border=INK, borderWidth=2)
    drawLabel("START TRADING", 200, 225, align='center', fill=WHITE,
              font='monospace', bold=True, size=16)
    drawLabel("Build a portfolio and achieve your dreams.", 200, 291,
              align='center', fill=MUTED, font='monospace', size=11)
    drawLine(24, 330, 376, 330, fill=RULE, lineWidth=1)
    drawLabel("7 DAYS", 24, 351, align='left', fill=GREEN,
              font='monospace', bold=True, size=12)
    drawLabel("REAL LIFE TICKER PRICES - SIMULATED VOLATILITY", 376, 351,
              align='right', fill=MUTED, font='monospace', size=9)
    
    #here i just added the rectangle and label inside and use onmousepress to simulate it as a button to start the game
def start_onMousePress(app,mouseX,mouseY):
    if((mouseX>=100 and mouseX<=300) and (mouseY>=190 and mouseY<=260)):
        setActiveScreen("game") #begin game

#add information section with information regarding time increments?

#game code
def game_redrawAll(app):
    drawRect(0, 0, 400, 400, fill=PAGE)
    drawRect(0, 0, 400, 86, fill=INK)
    drawLabel("POCKET / STOCKS", 18, 22, align='left', fill=LIME,
              font='monospace', bold=True, size=10)
    drawLabel("MARKET SESSION", 18, 54, align='left', fill=WHITE,
              font='monospace', bold=True, size=17)
    drawRect(294, 15, 90, 55, fill=GREEN)
    drawLabel(f"DAY {app.date + 1} / 7", 339, 34, fill=WHITE,
              font='monospace', bold=True, size=12)
    drawLabel(f"{app.time // 60:02d}:{app.time % 60:02d}", 339, 54,
              fill=MINT, font='monospace', size=11)

    drawRect(16, 103, 368, 76, fill=WHITE)
    drawLabel("AVAILABLE CASH", 31, 124, align='left', fill=MUTED,
              font='monospace', bold=True, size=10)
    drawLabel(f"${app.money:,.2f}", 31, 154, align='left', fill=INK,
              font='monospace', bold=True, size=24)
    drawLabel("P  pause     E  exit", 369, 164, align='right', fill=MUTED,
              font='monospace', size=9)

    drawRect(16, 198, 176, 100, fill=GREEN)
    drawLabel("B", 34, 225, align='left', fill=LIME,
              font='monospace', bold=True, size=23)
    drawLabel("BROWSE", 34, 254, align='left', fill=WHITE,
              font='monospace', bold=True, size=15)
    drawLabel("Find a ticker", 34, 279, align='left', fill=MINT,
              font='monospace', size=10)
    drawRect(208, 198, 176, 100, fill=INK)
    drawLabel("C", 226, 225, align='left', fill=LIME,
              font='monospace', bold=True, size=23)
    drawLabel("PORTFOLIO", 226, 254, align='left', fill=WHITE,
              font='monospace', bold=True, size=15)
    drawLabel("Review positions", 226, 279, align='left', fill=MINT,
              font='monospace', size=10)
    drawLine(16, 323, 384, 323, fill=RULE, lineWidth=1)
    drawLabel("LIVE LOOKUP", 18, 346, align='left', fill=GREEN,
              font='monospace', bold=True, size=10)
    drawLabel("Prices update with simulated market movement.", 18, 367,
              align='left', fill=MUTED, font='monospace', size=10)

    if app.gameOver or app.paused:
        drawRect(46, 151, 308, 104, fill=WHITE, border=GREEN, borderWidth=2)
        if app.gameOver:
            drawLabel("SESSION COMPLETE", 200, 187, fill=CORAL,
                      font='monospace', bold=True, size=17)
            drawLabel("Press E to return to the start screen", 200, 220,
                      fill=INK, font='monospace', size=10)
        else:
            drawLabel("PAUSED", 200, 187, fill=GREEN,
                      font='monospace', bold=True, size=20)
            drawLabel("Press P to resume", 200, 220,
                      fill=INK, font='monospace', size=11)
#user inputs stock ticker symbol
#api pulls stock data -> you should go to a new screen 
def game_onKeyPress(app,key):
    if(key=='p'):
        app.paused = not app.paused
    elif(key=='e'):
        response=app.getTextInput("Are you sure you want to quit? (enter Y/N): ")
        if(response=='Y' or response=='y'):
            resetValues(app)
            setActiveScreen('start')
    elif(key=='b'):
        fetchStocks(app)
        setActiveScreen("results")
    elif(key=='c'):
        setActiveScreen("portfolio")
    
    
def game_onStep(app):
    advanceGame(app)

def advanceGame(app):
    if app.paused or app.gameOver:
        return 
    updateStockPrices(app)
    app.time+=6
    if(app.date==7):
        app.gameOver=True
        return
    elif(app.time>=1200):
        app.time=8
        app.date+=1

def updateStockPrices(app):
    for holding in app.possessions.values():
        change = random.uniform(-0.005, 0.005)
        holding['currentPrice'] = max(0.01, holding['currentPrice'] * (1 + change))
        holding['history'].append(holding['currentPrice'])
        if len(holding['history']) > 40:
            holding['history'].pop(0)

def fetchStocks(app):
    response=app.getTextInput("Which stock would you like to buy? (Ticker will make search easier (ex. AAPL))")
    app.scroll=0
    if not response:
        app.stocks=[]
        return
    try:
        url = "https://api.tickerbot.io/v2/tickers"
        params = {
        "search": f"{response}"
        }
        headers = { "Authorization": f"Bearer {api_key}" }
        r = requests.get(url, params=params,headers=headers)
        r.raise_for_status() #api call to get ticker information
        app.stocks = [ #make sure you know  how to explain this
            {"ticker": s["ticker"], "name": s["name"], "exchange": s.get("exchange") or "N/A"}
            for s in r.json()["results"]
            if s["active"]
        ] #stock values 
    except requests.RequestException:
        app.apiError=True
#stock search screen
def results_redrawAll(app):
    drawRect(0, 0, 400, 400, fill=PAGE)
    drawRect(0, 0, 400, 76, fill=INK)
    drawLabel("STOCK FINDER", 18, 25, align='left', fill=WHITE,
              font='monospace', bold=True, size=17)
    drawLabel("T  ticker details / buy      E  back", 18, 53,
              align='left', fill=MINT, font='monospace', size=10)
    if app.apiError:
        drawRect(28, 145, 344, 100, fill=WHITE)
        drawLabel("Could not load stock data", 200, 187, fill=CORAL,
                  font='monospace', bold=True, size=14)
        drawLabel("Check your connection and try again.", 200, 215,
                  fill=MUTED, font='monospace', size=10)
        return
    if(app.stocks==[]):
        setActiveScreen("game")
    for i, s in enumerate(app.stocks):
        y = 94 + i * 34 - app.scroll
        if y < 82 or y > 390:
            continue
        drawLabel(s["ticker"], 20, y, align='left', fill=GREEN,
                  bold=True, font='monospace', size=12)
        drawLabel(s["name"][:31], 100, y, align='left', fill=INK,
                  font='monospace', size=10)
        drawLine(18, y + 15, 382, y + 15, fill=RULE, lineWidth=1)


#know how to explain this part
def results_onKeyPress(app, key):
    maxScroll = max(0, len(app.stocks) * 34 - 300)
    if key == 'down':
        app.scroll = min(maxScroll, app.scroll + 34)
    elif key == 'up':
        app.scroll = max(0, app.scroll - 34)
    elif key=='e':
        setActiveScreen("game")
    elif key=='t':
        buyTicker(app)

def buyTicker(app):
    response=app.getTextInput("Please input the TICKER below for price information")
    if not response:
        return
    try:
        url = f"https://api.tickerbot.io/v2/tickers/{response.strip().upper()}"
        headers = { "Authorization": f"Bearer {api_key}" }
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status() #api call to get ticker information
        d = r.json()["data"] #there is a specific ["data"] key in the json file that has all the actual ticker information (display format of json here to explain)
    except (requests.RequestException, KeyError, ValueError):
        app.showMessage(f"Could not load data for '{response}'.")
        return

    try:
        prompt = (
            f"{d['name']} ({d['ticker']}) - {d['exchange']}\n"
            f"Sector: {d.get('sector')} | {d.get('industry')}\n"
            f"Price: ${d['price']:,.2f} ({d['change_1d_pct']*100:+.2f}% today)\n"
            f"52w range: ${d['low_52w']:,.2f} - ${d['high_52w']:,.2f}\n"
            f"Market cap: ${d['market_cap']:,}\n"
            f"P/E: {d.get('pe_ratio')} | EPS: {d.get('eps')}\n"
            f"RSI(14): {d.get('rsi_14')}\n"
            f"Volume: {d['volume_today']:,} (rel. {d.get('relative_volume')}x)\n\n"
            f"Buy {d['ticker']} at ${d['price']:,.2f}? (Y/N)"
        )
    except TypeError:
        app.showMessage("Please choose a different stock. Some information is not available for this stock.")
        return #I noticed during testing that one of the stocks in an api call returned "null" values, so I used this try-except statement to account for that.
    answer = app.getTextInput(prompt)
    quantity=app.getTextInput("How many shares would you like to buy? (enter number only)")
    if not answer or answer.strip().lower() != 'y':
        return
    quantity=float(quantity)
    if(quantity==0):
        return

    try:
        price = float(d['price'])
        ticker = d['ticker']
    except (KeyError, TypeError, ValueError):
        app.showMessage("This stock does not have a valid price.")
        return
    if not math.isfinite(price) or price <= 0:
        app.showMessage("This stock does not have a valid price.")
        return
    if (app.money) < price*quantity:
        app.showMessage("Sorry. You do not have enough to purchase this!")
        return

    holding = app.possessions.get(ticker)
    if holding is None:
        app.possessions[ticker] = {
            'shares': quantity,
            'costBasis': price*quantity,
            'currentPrice': price,
            'history': [price],
        }
    else:
        holding['shares'] += quantity
        holding['costBasis'] += (price*quantity)
        holding['currentPrice'] = price
        holding['history'].append(price)
        holding['history'] = holding['history'][-40:]
    app.money -= (price*quantity)

def drawHoldingGraph(history, x, y, width, height, color=GREEN):
    if len(history) < 2:
        return
    low = min(history)
    high = max(history)
    valueRange = high - low
    if valueRange == 0:
        valueRange = 1
    points = []
    for index, price in enumerate(history):
        pointX = x + index * width / (len(history) - 1)
        pointY = y + height - (price - low) * height / valueRange
        points.append((pointX, pointY))
    for index in range(len(points) - 1):
        drawLine(*points[index], *points[index + 1], fill=color, lineWidth=2)

def portfolio_redrawAll(app):
    totalValue = sum(holding['shares'] * holding['currentPrice'] for holding in app.possessions.values())
    drawRect(0, 0, 400, 400, fill=PAGE)
    drawRect(0, 0, 400, 70, fill=INK)
    drawLabel("YOUR PORTFOLIO", 18, 23, align='left', fill=WHITE,
              bold=True, font='monospace', size=17)
    drawLabel(f"CASH  ${app.money:,.2f}", 18, 50, align='left',
              fill=LIME, font='monospace', bold=True, size=11)
    drawLabel(f"INVESTED  ${totalValue:,.2f}", 382, 50, align='right',
              fill=MINT, font='monospace', bold=True, size=11)
    drawLabel("E back     S sell     UP / DOWN scroll", 200, 84,
              fill=MUTED, font='monospace', size=9)

    if not app.possessions:
        drawRect(24, 145, 352, 112, fill=WHITE)
        drawLabel("No positions yet", 200, 190, fill=INK,
                  font='monospace', bold=True, size=16)
        drawLabel("Browse stocks to make your first trade.", 200, 220,
                  fill=MUTED, font='monospace', size=10)
        return

    for index, (ticker, holding) in enumerate(app.possessions.items()):
        y = 99 + index * 72 - app.portfolioScroll
        if y + 66 < 93 or y > 400:
            continue
        averageCost = holding['costBasis'] / holding['shares']
        currentValue = holding['shares'] * holding['currentPrice']
        profit = currentValue - holding['costBasis']
        drawRect(14, y, 372, 66, fill=WHITE)
        drawLabel(ticker, 25, y + 17, align='left', fill=INK,
                  bold=True, font='monospace', size=14)
        drawLabel(f"{holding['shares']:g} shares  /  avg ${averageCost:,.2f}",
                  25, y + 43, align='left', fill=MUTED, font='monospace', size=9)
        graphColor = GREEN if profit >= 0 else CORAL
        drawHoldingGraph(holding['history'], 190, y + 13, 108, 38, graphColor)
        drawLabel(f"${holding['currentPrice']:,.2f}", 370, y + 20,
                  align='right', fill=INK, font='monospace', bold=True, size=11)
        drawLabel(f"P/L {profit:+,.2f}", 370, y + 43, align='right',
                  fill=GREEN if profit >= 0 else CORAL,
                  font='monospace', bold=True, size=9)

def portfolio_onKeyPress(app, key):
    maxScroll = max(0, len(app.possessions) * 72 - 285)
    if key == 'down':
        app.portfolioScroll = min(maxScroll, app.portfolioScroll + 72)
    elif key == 'up':
        app.portfolioScroll = max(0, app.portfolioScroll - 72)
    elif key == 'e':
        setActiveScreen('game')
    elif key == 's':
        sellStock(app)


#make sure you understand how this works
def sellStock(app):
    if not app.possessions:
        app.showMessage("You do not own any stocks to sell.")
        return

    response = app.getTextInput("Enter the ticker symbol you would like to sell:")
    if not response or not response.strip():
        return
    ticker = response.strip().upper() #entering ticker symbol
    holding = app.possessions.get(ticker) #corresponding holding for the inputted ticker that the user inputs
    if holding is None:
        app.showMessage(f"You do not own {ticker}.") 
        return

    quantityResponse = app.getTextInput(
        f"How many shares of {ticker} would you like to sell? "
        f"You own {holding['shares']:g}."
    ) #response box for user to input their shares
    
    if not quantityResponse:
        return #if no response
    
    #try/except to ensure that user inputs a valid number
    try:
        quantity = float(quantityResponse)
    except (TypeError, ValueError):
        app.showMessage("Enter a valid number of shares.")
        return
    
    if not math.isfinite(quantity) or quantity <= 0:
        app.showMessage("Enter a positive number of shares.")
        return #positive number of shares
    if quantity > holding['shares']:
        app.showMessage(f"You only own {holding['shares']:g} shares of {ticker}.")
        return #catches whether a quantity is greater than the existing shares in the holding for the ticker

    proceeds = quantity * holding['currentPrice'] 
    remainingShares = holding['shares'] - quantity #updates current shares
    if remainingShares == 0:
        del app.possessions[ticker]
    else:
        remainingFraction = remainingShares / holding['shares'] #explain this
        holding['shares'] = remainingShares #updates shares
        holding['costBasis'] *= remainingFraction
    app.money += proceeds #adds the proceeds generated from selling n shares of a stock

def portfolio_onStep(app):
    advanceGame(app)

def main():
    runAppWithScreens(initialScreen='start')
    
main()