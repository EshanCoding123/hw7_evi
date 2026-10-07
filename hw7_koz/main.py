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
    app.time=0
    app.stepsPerSecond=1 
    app.date=0
    app.paused=False
    app.gameOver=False
    
    #dictionary with key->ticker and current stock value adjusted per step
    app.stockpossessions=dict()
    
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
    app.time=0
    app.stepsPerSecond=1 
    app.date=0
    app.paused=False
    app.gameOver=False

def start_redrawAll(app):
    drawLabel('Welcome to PocketStocks!', 200,50, font='monospace',fill='green', 
              align='center', bold=True, size=13)
    drawLabel("$10,000 to start, and 7 days to reach 100,000 dollars.",200,65,font='monospace',fill='green',align='center',bold=True,size=12)
    drawLabel(" You have the freedom to invest in ANY stock.",200,80,font='monospace',fill='green',align='center',bold=True,size=13)
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
    
    drawLabel(f"Current Money: {app.money}",25,25,fill='green', bold=True, font='monospace',align='left',size=20 )
    drawLabel(f"Current Time (Hrs): {app.time/60} | Day {app.date}",25,50,fill='green', bold=True, font='monospace',align='left',size=12 )
    drawLabel(f"P -> Pause | E -> Exit Game (will lose progress)", 25,75, fill='green',bold=True,font='monospace',align='left',size=12)
   
    drawRect(100, 100, 200, 80, fill='green')
    drawLabel("Press green button to input desired stock ()")
    if(app.gameOver):
        drawLabel("Game Over!",200,50,fill='red',bold=True,font='monospace',align='center',size=30)
        drawLabel("Press E to go back to the main screen.",200,75,fill='red',bold=True,font='monospace',align='center',size=20)
    if(app.paused):
        drawLabel("Game Paused!",200,200,fill='blue',bold=True,font='monospace',align='center',size=30)    

def game_onKeyPress(app,key):
    if(key=='p'):
        app.paused = not app.paused
    elif(key=='e'):
        response=app.getTextInput("Are you sure you want to quit? (enter Y/N): ")
        if(response=='Y' or response=='y'):
            resetValues(app)
            setActiveScreen('start')
        
def game_onStep(app):
    if(app.paused):
        #we are just going to change the visibility of the paused game screen
        return 
    app.time+=6
    if(app.date==7):
        # We are just going to change the visibility of the game over screen
        app.gameOver=True
        return
    elif(app.time>=1440):
        app.time=0
        app.date+=1

    #stock volatility simulator
    
    
        
    #6 minutes per sec -> 12 seconds for 1 hr -> 4.8 min 1 day 
    

#onStep() for calling live stock ticker API results
#def 
#add input feature for user
def main():
    runAppWithScreens(initialScreen='start')
    
main()