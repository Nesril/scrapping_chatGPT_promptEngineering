from openai import OpenAI
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from urllib.request import urlopen
import html2text

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

def GetTop1GoogleResults(user_input):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    query = user_input

    n_pages = 11  
    results = []
    counter = 0
    for page in range(1, n_pages):
        url = "http://www.google.com/search?q=" + \
            query + "&start=" + str((page - 1) * 10)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            counter = counter + 1
            title = h.a.h3.text
            link = h.a.get('href')
            rank = counter
            results.append({'title': h.a.h3.text, 'url': link,
                            'domain': urlparse(link).netloc, 'rank': rank})
    driver.quit() 
    return results[0]['url']

def SearchTheWeb(query):
    print("Searching the web...")
    url = GetTop1GoogleResults(query)
    print("URL Found: " + url)
    print("Opening URL...")
    html = urlopen(url).read()
    print("Pasrsing Content...")
    soup = BeautifulSoup(html, features="html.parser")
    extractedText = soup.get_text()
    print("Extract Text...")
    h = html2text.HTML2Text()
    h.ignore_links = True
    blogPost = h.handle(extractedText)
    print("Generating Summary...")
    postPrompt="""In the following input, I am going to give you a text you
             should summarize for me. I will give you a maximum and a minimum
             amount of words you should use for the text. I am also going
             to give you the text itself after that. The language
             of the text you get should define in which language
             you write the summary. For Example, if the text is German
             the summary should be in German too. This goes for every language.
             While writing the summary I want you to remember the following information:
             When it comes to writing content, two factors are crucial,'perplexity' and 'burstiness'
             ,Perplexity measures the complexity of text. Separately, burstiness compares
             the variations of sentences. Humans tend to write with great burstiness,
             for example, with some longer or complex sentences alongside shorter sentences.
             AI sentences tend to be more uniform. Therefore, when writing the following content
             I am going to ask you to create, I need it to have a good amount of perplexity
             and burstiness. Keep that information in mind while writing. Minimum: 100, Maximum: 500, Text: """ + blogPost
   # print(postPrompt,blogPost)
    return BasicGeneration(postPrompt)


query = input("Enter your search query: ")
print(SearchTheWeb(query))