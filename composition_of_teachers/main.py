import os

import requests
from bs4 import BeautifulSoup as BS


def create_teachers_page():
    site = requests.get('https://mgutm.ru/sveden/employees/#title')
    html = BS(site.content, 'html.parser')
    items = html.select(".container.mb80 > .col-xs-12 > .table-responsive")
    for element in items:
        department_selection = element.select('table > caption')
        department = department_selection[0].text

        department_links = element.select('.tableWrap tbody > tr > td:last-child a')
        for department_link in department_links:
            link = department_link.get('href')
            teacher_page = requests.get(link)
            teacher_page_html = BS(teacher_page.content, 'html.parser')

            tag_name_of_the_teacher = teacher_page_html.select('main .section-title')
            name_of_the_teacher = tag_name_of_the_teacher[0].text

            content_main = teacher_page_html.select('main > div')[0]
            template = f"""
                        <?php get_header(); ?>

                            <main class="main-content home-page">
                                {content_main}
                            </main>

                        <?php get_footer(); ?>
                        """
            filename = './templates/' + department + '/' + name_of_the_teacher + '.php'
            if not os.path.exists(os.path.dirname(filename)):
                dir_name = os.path.dirname(filename)
                os.makedirs(dir_name)
            with open(filename, "w", encoding="utf-8") as file:
                file.write(template)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_teachers_page()
