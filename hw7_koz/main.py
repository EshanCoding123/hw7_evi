from cmu_graphics import *
import requests
import os
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
    app.possessions=dict()

def start_redrawAll(app):
    drawLabel('Welcome to PocketStocks!', 200,50, font='monospace',fill='green', 
              align='center', bold=True, size=13)
    drawLabel("$10,000 to start, and 7 days to reach 100,000 dollars.",200,65,font='monospace',fill='green',align='center',bold=True,size=12)
    drawLabel(" You have the freedom to invest in ANY volatile stock.",200,80,font='monospace',fill='green',align='center',bold=True,size=13)
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
    drawLabel(f"Current Money: {app.money}",25,25,fill='green', bold=True, font='monospace',align='left',size=20 )
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

    
def game_onStep(app):
    if(app.paused):
        return 
    app.time+=6
    if(app.date==7):
        app.gameOver=True
        return
    elif(app.time>=1200):
        app.time=0
        app.date+=1

    #stock volatility simulator
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
        d = r.json()["data"]
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
    
    if answer and answer.strip().lower() == 'y':
        app.selectedStock = d
    ticker=d['ticker']
    #dictionary logic
    if(app.money-app.selectedStock['price']<0):
        app.showMessage("Sorry. You do not have enough to purchase this!")
    if(ticker in app.possessions.keys()):
        app.money-=app.selectedStock['price']
        app.possessions[ticker]+=app.selectedStock['price']
    else:
        app.money-=app.selectedStock['price']
        app.possessions[ticker]=app.selectedStock['price']
    print(app.possessions) #tester
    
    

#current portfolio screen

    #this is where you continuously update the stock value
    #6 minutes per sec -> 12 seconds for 1 hr -> 4.8 min 1 day 
    
def main():
    runAppWithScreens(initialScreen='start')
    
main()