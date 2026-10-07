import requests
from bs4 import BeautifulSoup as BS


def parsing_managers():
    site = requests.get('https://mgutm.ru/sveden/struct/#title')
    html = BS(site.content, 'html.parser')
    items = html.select("tbody > tr")
    for el in items:
        manager = el.select('tr > td:nth-child(3)')
        link_manager = el.select('tr > td:nth-child(3) > a')
        try:
            fio_manager = manager[0].text
            link_manager = link_manager[0].get('href')
        except IndexError:
            continue
        if fio_manager == "-":
            continue
        site_manager = requests.get(link_manager)
        site_manager_html = BS(site_manager.content, 'html.parser')
        selected_container = site_manager_html.select("main > .container")
        container = selected_container[0]

        html_str = f"""
                    <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>{fio_manager}</title>
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
                  {container}
                </div>
                </body>
                </html>
                    """
        name_file = fio_manager + ".html"
        dir_file = "./template/" + name_file
        with open(dir_file, 'w', encoding="utf-8") as html_file:
            html_file.write(html_str)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parsing_managers()
