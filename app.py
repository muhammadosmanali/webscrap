from flask import Flask, render_template

import requests
from bs4 import BeautifulSoup

from datetime import datetime
from pytz import timezone

#__name__ == __main__
app = Flask(__name__)
URL = 'https://techcrunch.com/'
page = requests.get(URL)  # type of page -- request

# type coverted to BeautifulSoup
# second argument how you want to structure your data
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(class_='river river--homepage')

post_elems = results.select('.post-block')

table = [['Sr No', 'Time Stamp', 'News Title', 'Image Source URL', 'Author']]
i = 1

for post_elem in post_elems:
    header_elem = post_elem.find('header', class_='post-block__header')
    title_elem = header_elem.find('a', class_='post-block__title__link')
    timeStamp_elem = header_elem.find('time')['datetime']
    author_elem = header_elem.find('span')
    image_elem = post_elem.find('img')
    date = datetime.strptime(timeStamp_elem, "%Y-%m-%dT%H:%M:%S%z" )
    row = [i,  date.astimezone(timezone('Asia/Kolkata')).strftime("%I:%M %p" + " IST " + "%B %d, %Y"), title_elem.text.strip(),
           image_elem.get('src'), author_elem.text.strip()]
    table.append(row)
    i = i + 1

@app.route('/')
def index():
    return render_template("index.html", table=table)

if __name__ == '__main__':
    app.run(debug=True)
