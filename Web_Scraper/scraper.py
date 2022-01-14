import requests
from bs4 import BeautifulSoup
import os
import string


def check_status(response):
    if response.status_code == 200:
        return True
    return False


def save_file(page_id, content, news):
    directory = 'Page_{0}'.format(page_id)
    os.mkdir(directory)
    file_name = ''
    for ch in news:
        if ch in string.punctuation:
            continue
        file_name += ch
    file_name += '.txt'
    file_name = file_name.replace(' ', '_')

    try:
        with open(directory + '/' + file_name, 'wb') as fn:
            fn.write(content)
    except IOError:
        print('Error with writing page content')


def get_article(article_url, headers):
    r_article = requests.get(article_url, headers=headers)
    if not check_status(r_article):
        return False
    soup_article = BeautifulSoup(r_article.content, 'html.parser')
    # <div class="c-article-body u-clearfix">
    article_body = soup_article.find('div', {'class': 'c-article-body'})
    article_body = article_body.text.strip().replace('\n', '')

    return article_body


def get_articles(page_id, type_of_article, articles, headers):
    no_of_found = 0
    for article in articles:
        article_type = article.find('span', {'data-test': 'article.type'})
        desc = article.find('a', {'itemprop': 'url', 'data-track-action': 'view article'})
        if article_type.text.strip() == type_of_article:
            url = 'https://www.nature.com' + desc.get('href')
            body = get_article(url, headers)
            if not body:
                print('Cannot get article page')
                continue
            save_file(page_id, str(body).encode('utf-8'), desc.text.strip())
            no_of_found += 1

    if not no_of_found:
        os.mkdir('Page_{0}'.format(page_id))


def process_pages(no_of_pages, type_of_article):
    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={0}'

    for page in range(1, no_of_pages + 1):
        r = requests.get(url.format(page), headers=headers)
        if not check_status(r):
            print(f'Cannot open page: {url.format(page)}')
            continue
        soup = BeautifulSoup(r.content, 'html.parser')
        article_list = soup.find('section', {'id': 'new-article-list'})
        articles = article_list.find_all('article')
        get_articles(page, type_of_article, articles, headers)


while True:
    try:
        pages = int(input('> '))
        a_type = input('> ').strip()
    except ValueError:
        print('Provide number for first input')
    else:
        break

process_pages(pages, a_type)
