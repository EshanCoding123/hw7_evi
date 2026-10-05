from cmu_graphics import *
import requests
 

#start screen code
def onAppStart(app):
    app.background="black"
    
    # import requests

    # url = "https://api.tickerbot.io/v2/tickers/AAPL"
    # headers = { "Authorization": "Bearer tb_live_pP36XqCUJKMQVot6IaLyrH5oGWtdiTVQYnpwIqtAWaQ" }

    # r = requests.get(url, headers=headers)
    # r.raise_for_status()
    # print(r.json())
def start_redrawAll(app):
    drawLabel('Welcome to PocketStocks!', 200,50, font='monospace',fill='green', 
              align='center', bold=True, size=13)
    drawLabel("You will be given $10,000 to start, ",200,65,font='monospace',fill='green',align='center',bold=True,size=13)
    drawLabel(" and the freedom to invest in ANY stock.",200,80,font='monospace',fill='green',align='center',bold=True,size=13)
    drawLabel(" Will you survive? or go bankrupt?.",200,95,font='monospace',fill='green',align='center',bold=True,size=13)
    drawLabel(" The choice is yours.",200,110,fill='green',font='monospace',align='center',bold=True,size=13)
    
    drawRect(100, 180, 200, 80, fill='green')
    drawLabel("Press this button to",200, 210, align='center', font='monospace', bold=True,size=13)
    drawLabel("begin the game!", 200, 225, align='center', font='monospace',bold=True,size=13)
    # drawRect()
    # drawLabel()
    
    #here i just added the rectangle and label inside and use onmousepress to simulate it as a button to start the game
def start_onMousePress(app,mouseX,mouseY):
    if((mouseX>=100 and mouseX<=300) and (mouseY>=180 and mouseY<=260)):
        setActiveScreen("game") #begin game

        
#game code
def game_redrawAll(app):
    drawLabel("hello world",200,50,fill='green',align='center',bold=True,size=13)


#onStep() for calling live stock ticker API results
#def 
#add input feature for user
def main():
    runAppWithScreens(initialScreen='start')
    
main()