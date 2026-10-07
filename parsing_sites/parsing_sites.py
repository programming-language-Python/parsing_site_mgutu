import requests
from bs4 import BeautifulSoup as BS
import re

site = requests.get('https://mgutm.ru/sveden/struct/#title')
html = BS(site.content, 'html.parser')
items = html.select("tbody > tr")

for el in items:
    title = el.select('tr > td:first-child')
    link = el.select('tr > td:last-child > a')

    try:
        title_text = title[0].text
        link_href = link[0].get('href')
        
        https = "https://mgutm.ru"
        if link_href.find(https):
            link_href = https + link_href
            print('error', link_href)
        print('success', link_href)

        site2 = requests.get(link_href)
        site2_html = BS(site2.content, 'html.parser')
        site2_select = site2_html.select("main > .container")
        site2_container = site2_select[0]
    except IndexError:
        pass

    reg = re.compile('[^а-яА-Я ]')
    title_text_reg = reg.sub('', title_text).strip()
    html_str = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title_text_reg}</title>
</head>
<style>
    .wrapper {{
        max-width: 1225px;
        margin: 0 auto;
        padding-top: 15px;
        padding-bottom: 15px;
        padding-left: 25px;
        padding-right: 25px;
        background: yellow;
    }}
</style>
<body>

<div class="wrapper">
  {site2_container}
</div>
</body>
</html>
    """
    name_file = title_text_reg + ".html"
    dir_file = "./sites/" + name_file
    with open(dir_file, 'w',  encoding="utf-8") as html_file:
        html_file.write(html_str)
