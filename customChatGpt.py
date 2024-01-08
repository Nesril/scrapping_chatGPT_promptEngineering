from openai import OpenAI
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


def BasicGeneration(userPrompt):
    completion=client.chat.completions.create(model='gpt-3.5-turbo',
    messages=[{'role':'user','content':userPrompt}])
    return completion.choices[0].message.content

def GetBitCoinPrices(daysOfAnalysis):
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"

    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":f"{daysOfAnalysis}"}

    headers = {
        "X-RapidAPI-Key": os.getenv('BITCOIN_API_KEY'),
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    result=json.loads(response.text)
    #print(result,querystring)
    history=result['data']['history']
    prices=[]
    for change in history:
        prices.append(change['price'])
    return ", ".join(prices)


def generatePrompt(daysOfAnalysis):
       
    chatGptPrompt=f"""You are an expert crypto trader with more than 10 uears of experience, 
    i will provide you with the list of bitcoin prices for last {daysOfAnalysis}
    can you provide me with a technical analysis of bitcoin based on these prices. here is what i want:
    Price Overview,
    Moving Averages,
    Relative Strength Index (RSI),
    Moving Average Convergence Divergence (MACD),
    Advice and Suggestion,
    Do I buy or sell ?,
    please be deatiled as you can explain in away any beginner can understand, and make.
    here is the bitcoin list: {GetBitCoinPrices(daysOfAnalysis)}
    """
    return chatGptPrompt

print("--- Bitcoin Analysis---")
daysOfAnalysis=input('''Enter number of days that you want to see the analysis note that timePeriod must be one of 1h, 3h, 12h, 24h, 7d, 
30d, 3m, 1y, 3y, 5y: ''')
print(BasicGeneration(generatePrompt(daysOfAnalysis)))




