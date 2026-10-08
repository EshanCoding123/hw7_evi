from cmu_graphics import *
import requests
import os
import random
import math
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("TICKER_API_KEY")

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
    drawLabel('Welcome to PocketStocks!', 200,50, font='monospace',fill='green', 
              align='center', bold=True, size=13)
    drawLabel("$10,000 to start, and 7 days to make lots of money.",200,65,font='monospace',fill='green',align='center',bold=True,size=12)
    drawLabel(" You have the freedom to invest in ANY volatile stock.",200,80,font='monospace',fill='green',align='center',bold=True,size=12)
    drawLabel(" Will you survive? or go bankrupt?.",200,95,font='monospace',fill='green',align='center',bold=True,size=13)
    drawLabel(" The choice is yours.",200,110,fill='green',font='monospace',align='center',bold=True,size=13)
    
    drawRect(100, 180, 200, 80, fill='green')
    drawLabel("Press this button to",200, 210, align='center', font='monospace', bold=True,size=13)
    drawLabel("begin the game!", 200, 225, align='center', font='monospace',bold=True,size=13)
    
    #here i just added the rectangle and label inside and use onmousepress to simulate it as a button to start the game
def start_onMousePress(app,mouseX,mouseY):
    if((mouseX>=100 and mouseX<=300) and (mouseY>=180 and mouseY<=260)):
        setActiveScreen("game") #begin game

#add information section with information regarding time increments?

#game code
def game_redrawAll(app):
    drawRect(50, 100, 300, 80, fill='green')
    drawRect(50, 200, 300, 80, fill='green')
    drawLabel(f"Current Money: ${app.money:.2f}",25,25,fill='green', bold=True, font='monospace',align='left',size=20 )
    drawLabel(f"Current Time (Hrs): {app.time/60} | Day {app.date}",25,50,fill='green', bold=True, font='monospace',align='left',size=12 )
    drawLabel(f"P -> Pause | E -> Exit Game (will lose progress)", 25,75, fill='green',bold=True,font='monospace',align='left',size=12)
    
    drawLabel("Press B to browse stocks!",200,140,fill='black',bold=True,font='monospace',align='center',size=15)
    #(only a ticker symbol will be accepted -> ex. AAPL or NVDA)
    drawLabel("Press C to display current stock portfolio!",200,240,fill='black',bold=True,font='monospace',align='center',size=11)
    drawLabel("Note: stocks are real market price the moment you open them;",200,300,fill='green',bold=True,font='monospace',align='center',size=10)
    #afterwards volatility is simulated
    drawLabel("Afterwards, volatility is simulated.",200,315,fill='green',bold=True,font='monospace',align='center',size=12)
    if(app.gameOver):
        drawLabel("Game Over!",200,50,fill='red',bold=True,font='monospace',align='center',size=30)
        drawLabel("Press E to go back to the main screen.",200,75,fill='red',bold=True,font='monospace',align='center',size=20)
    if(app.paused):
        drawLabel("Game Paused!",200,200,fill='blue',bold=True,font='monospace',align='center',size=30)    
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
    if app.apiError:
        drawLabel("Could not load stock data", 200, 200, fill='red', font='monospace')
        return
    if(app.stocks==[]):
        setActiveScreen("game")
    for i, s in enumerate(app.stocks):
        y = 70 + i * 25 - app.scroll
        drawLabel(s["ticker"], 20, y, align='left', fill='green', bold=True, font='monospace')
        drawLabel(s["name"][:28], 90, y, align='left', fill='green', font='monospace', size=11)
    # header drawn last so scrolled rows are hidden behind it
    drawRect(0, 0, 400, 55, fill='black')
    drawLabel("Results (Up/Down to scroll)", 200, 30, fill='green', bold=True, font='monospace', size=16)
    drawLabel("Press T to input a ticker and see price info", 200, 40, fill='green',align='center', bold=True, font='monospace', size=11)
    drawLabel("Press E to exit to game", 200, 50, fill='green',align='center', bold=True, font='monospace', size=11)


#know how to explain this part
def results_onKeyPress(app, key):
    maxScroll = max(0, len(app.stocks) * 25 - 320)
    if key == 'down':
        app.scroll = min(maxScroll, app.scroll + 25)
    elif key == 'up':
        app.scroll = max(0, app.scroll - 25)
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

def drawHoldingGraph(history, x, y, width, height):
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
        drawLine(*points[index], *points[index + 1], fill='green', lineWidth=2)

def portfolio_redrawAll(app):
    totalValue = sum(holding['shares'] * holding['currentPrice'] for holding in app.possessions.values())
    drawLabel("Portfolio", 200, 22, fill='green', bold=True, font='monospace', size=18)
    drawLabel(f"Cash: ${app.money:,.2f}   Holdings: ${totalValue:,.2f}", 200, 44, fill='green', font='monospace', size=11)
    drawLabel("E: back   S: sell   Up/Down: scroll", 200, 59, fill='green',font='monospace', size=10)

    if not app.possessions:
        drawLabel("No stocks owned yet", 200, 200, fill='green',
                  font='monospace', size=16)
        return

    for index, (ticker, holding) in enumerate(app.possessions.items()):
        y = 75 + index * 64 - app.portfolioScroll
        if y + 58 < 70 or y > 400:
            continue
        averageCost = holding['costBasis'] / holding['shares']
        currentValue = holding['shares'] * holding['currentPrice']
        profit = currentValue - holding['costBasis']
        drawLabel(f"{ticker}  x{holding['shares']}", 15, y + 12,
                  align='left', fill='green', bold=True, font='monospace', size=13)
        drawLabel(f"${holding['currentPrice']:,.2f}  avg ${averageCost:,.2f}",
                  15, y + 31, align='left', fill='green', font='monospace', size=10)
        drawLabel(f"P/L ${profit:+,.2f}", 15, y + 48, align='left',
                  fill='green' if profit >= 0 else 'red', font='monospace', size=10)
        drawHoldingGraph(holding['history'], 205, y + 8, 175, 42)
        drawLine(12, y + 61, 388, y + 61, fill='darkGreen')

def portfolio_onKeyPress(app, key):
    maxScroll = max(0, len(app.possessions) * 64 - 320)
    if key == 'down':
        app.portfolioScroll = min(maxScroll, app.portfolioScroll + 64)
    elif key == 'up':
        app.portfolioScroll = max(0, app.portfolioScroll - 64)
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