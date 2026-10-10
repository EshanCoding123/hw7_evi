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
    app.money=500000
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
    app.money=500000
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
    
    
    #explain graph connections!
    chartPoints = [(260, 108), (282, 94), (304, 101), (326, 72),
                   (348, 82), (374, 50)] #graph on home screen
    for index in range(len(chartPoints) - 1): #-1 so that it can connect to the last point
        drawLine(*chartPoints[index], *chartPoints[index + 1],
                 fill=LIME, lineWidth=3) #connects points of graph on homescreen
    for x, y in chartPoints:
        drawCircle(x, y, 3, fill=WHITE) #draws white circles on each point

    drawLabel("Start with $500,000", 200, 169, fill=INK,
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
    
    #button logic; click is between certain coordinates
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


def game_onKeyPress(app,key):
    if(key=='p'):
        app.paused = not app.paused #unpauses or pauses depending on pause value
    elif(key=='e'):
        response=app.getTextInput("Are you sure you want to quit? (enter Y/N): ")
        if(response=='Y' or response=='y'): #resets all user values; exits game
            resetValues(app) 
            setActiveScreen('start')
    elif(key=='b'): #browse stocks
        fetchStocks(app) 
        setActiveScreen("results")
    elif(key=='c'): #stock portfolio
        setActiveScreen("portfolio")
    
    
def game_onStep(app):
    advanceGame(app) #updates for each second in game screen

def advanceGame(app):
    #updates stock prices while in the game or in the portfolio screen
    if app.paused or app.gameOver:
        return 
    updateStockPrices(app)
    app.time+=6 #increments 6 minutes every second
    if(app.date==7): #if date hits 7, game over
        app.gameOver=True
        return
    elif(app.time>=1200): #if time greater than 1200 minutes (8:00PM time), go to 8am time and add a day
        app.time=8
        app.date+=1

def updateStockPrices(app):
    #volatility engine->randomly updates stock prices
    for holding in app.possessions.values(): #goes through each stock holding in values side of dict (dict={key:value,key:value,...})
        #each holding value is a dictionary itself
        change = random.uniform(-0.005, 0.005) #random float between these floats
        holding['currentPrice'] = max(0.01,holding['currentPrice']*(1+change)) 
        #0.01 acts as a safe guard for if the price is below 0.01 or it is negative. it defaults to 0.01
        holding['history'].append(holding['currentPrice']) #adds current price to history for graph
        if len(holding['history']) > 40:
            holding['history'].pop(0) #keeps track of past stock prices so that a graph can be drawn (in portfolio)
            #pops the oldest price so that history does not overload with data

def fetchStocks(app):
    response=app.getTextInput("Which stock would you like to buy? (Ticker will make search easier (ex. AAPL))")
    app.scroll=0 #starts at top of screen
    if not response:
        app.stocks=[] #no stocks to display
        return #ends fetch if no response
    try:
        url = "https://api.tickerbot.io/v2/tickers"
        params = {
        "search": f"{response}"
        }
        headers = { "Authorization": f"Bearer {api_key}" }
        r = requests.get(url, params=params,headers=headers)
        r.raise_for_status() #api call to get ticker information
        app.stocks = [ #reads json information, adds values to app.stocks for displaying (as dictionaries)
            {"ticker": s["ticker"], "name": s["name"], "exchange": s.get("exchange") or "N/A"}
            for s in r.json()["results"]
            if s["active"] #if the stock is active currently
        ] #stock values 
    except requests.RequestException:
        app.apiError=True #api call error stored when redrawing results screen

#stock results screen post-search
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
        #uses stored apiError data -> actually some stocks had null values so I had to implement this safe guard
        return
    if(app.stocks==[]):
        setActiveScreen("game") #if no results, go back to game screen
    for i, s in enumerate(app.stocks): #enumerate gives following -> i is the index, s is the dictionary with stock info
        y = 94 + i * 34 - app.scroll #calculates Y coordinate for label; i*34 spaces each stock 34 pixels apart. rows start 94 pixels down.
        #subtracts app.scroll from y value; say a row is at 400 it wont be drawn but after one scroll it subtracts 34 so it gets drawn because y=366
        if y < 82 or y > 390:
            #doesn't display rows outside the screen size
            continue
        drawLabel(s["ticker"], 20, y, align='left', fill=GREEN,
                  bold=True, font='monospace', size=12)
        drawLabel(s["name"][:31], 100, y, align='left', fill=INK,
                  font='monospace', size=10)
        drawLine(18, y + 15, 382, y + 15, fill=RULE, lineWidth=1) #lines in between


#know how to explain this part
def results_onKeyPress(app, key):
    maxScroll = max(0, len(app.stocks) * 34 - 300)#
    if key == 'down':
        app.scroll = min(maxScroll, app.scroll + 34) #prevents scrolling beyond max amount of scrolls
        #if this weren't the case, you could keep scrolling past the bottom of the screen
    elif key == 'up':
        app.scroll = max(0, app.scroll - 34) #prevents negative scrolling. that would in fact be quite odd if it was possible.
    elif key=='e':
        setActiveScreen("game") #exit
    elif key=='t':
        buyTicker(app) #buy a stock

def buyTicker(app):
    response=app.getTextInput("Please input the TICKER below for price information")
    if not response:
        return 
    try:
        url = f"https://api.tickerbot.io/v2/tickers/{response.strip().upper()}"
        #response is just the ticker the user inputted
        headers = { "Authorization": f"Bearer {api_key}" }
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status() #api call to get ticker information
        d = r.json()["data"] #there is a specific ["data"] key in the json file that has all the actual ticker information (display format of json here to explain)
    except (requests.RequestException, KeyError, ValueError):
        app.showMessage(f"Could not load data for '{response}'.")
        return

    try:
        prompt = (
            #prompt to user with all ticker info. buy or no?
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
    answer = app.getTextInput(prompt) #asks user
    try:
        quantity=app.getTextInput("How many shares would you like to buy? (enter number only)")
    except ValueError:
        app.showMessage("Please input a float value.") #catches bug for no number
        
    if not answer or answer.strip().lower() != 'y':
        return
    quantity=float(quantity)
    if(quantity==0):
        return #ends process of quantity is 0

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
    #checks for low money, or stock having incomplete information
    
    holding = app.possessions.get(ticker) #possessions stores all user holdings.
    if holding is None:#if nothing is returned, the user does not own any shares of this stock
        app.possessions[ticker] = {
            'shares': quantity,
            'costBasis': price*quantity,
            'currentPrice': price,
            'history': [price],
        }
        #adds data
    else: #otherwise, user already owns stock
        holding['shares'] += quantity
        holding['costBasis'] += (price*quantity) #adds all the money you paid for stokcs in total
        holding['currentPrice'] = price 
        holding['history'].append(price) #adds the price you  bought the stock at to the history
        holding['history'] = holding['history'][-40:] #keeps 40 most recent prices
    app.money -= (price*quantity) #subtract money :(

def drawHoldingGraph(history, x, y, width, height, color=GREEN):
    #history[10,20,15]
    #x=100
    #y=50
    #width=80
    #height=40
    
    #parameter in method: drawHoldingGraph(holding['history'], 190, y + 13, 108, 38, graphColor)
     
    if len(history) < 2:
        return #checker for if theres not enough data points to connect a graph
    low = min(history) #10
    high = max(history) #20
    valueRange = high - low #10
    if valueRange == 0: #if they were all equal, then high-low is 0 so setting to 1 is necessary
        valueRange = 1
    #uses min and max to scale the graph's height
    points = []
    for index, price in enumerate(history): #each price and corresponding index in history of prices
        pointX = x + index * width / (len(history) - 1) #computes x point value, increases as we go through history
        #100+0(80/2) = 100 
        #100+1(80/2) = 140
        #100+2(80/2) = 180
        pointY = y + height - (price - low) * height / valueRange 
        #50
        #50+40 = 90
        #15-10 = 5
        #0.5 
        #290 0 pixels above the bottom of the graph + = 110 
        #180,110
        #computes y point value by bottom of graph
        #finds how far price is above lowest price
        #converts into fraction (ex 0.5) then multiplies that by the height
        points.append((pointX, pointY))
    for index in range(len(points) - 1):
        #drawing lines between the points in the points array
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
        #AAPL ->ticker
        #99 2*72 - 72
        y = 99 + index * 72 - app.portfolioScroll #same scrolling logic, except each column spaced 72 pixels apart
        #2 
        if y + 66 < 93 or y > 400:
            continue #makes sure all possessions are in the screen
        averageCost = holding['costBasis'] / holding['shares']
        currentValue = holding['shares'] * holding['currentPrice'] 
        #currentValue updates with currentPrice, which updates using the volatility engine every time portfolio is redrawn
        profit = currentValue - holding['costBasis'] #profit calculation
        drawRect(14, y, 372, 66, fill=WHITE)
        drawLabel(ticker, 25, y + 17, align='left', fill=INK,
                  bold=True, font='monospace', size=14)
        drawLabel(f"{holding['shares']:g} shares  /  avg ${averageCost:,.2f}",
                  25, y + 43, align='left', fill=MUTED, font='monospace', size=9)
        graphColor = GREEN if profit >= 0 else CORAL
        drawHoldingGraph(holding['history'], 190, y + 13, 108, 38, graphColor) #draws graph with current history,x,y,width,height,and color
        drawLabel(f"${holding['currentPrice']:,.2f}", 370, y + 20,
                  align='right', fill=INK, font='monospace', bold=True, size=11)
        drawLabel(f"P/L {profit:+,.2f}", 370, y + 43, align='right',
                  fill=GREEN if profit >= 0 else CORAL,
                  font='monospace', bold=True, size=9)
        #.2f for rounding

def portfolio_onKeyPress(app, key):
    maxScroll = max(0, len(app.possessions) * 72 - 285)
    #same scrolling logic as before
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
        #lets say you bought 15 shares for 350. if you sold 10, remaining shares is
        #15-10=5. thus the fraction is 5/15 (the number of shares). therefore your cost basis 
        #after selling is 116.67 b/c you spent that much money on the 5 shares you have left.
    app.money += proceeds #adds the proceeds generated from selling n shares of a stock

def portfolio_onStep(app):
    advanceGame(app) 

def main():
    runAppWithScreens(initialScreen='start')
    
main()