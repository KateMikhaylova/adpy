import requests
from bs4 import BeautifulSoup
import re
from Homework5 import logger


@logger('scrapper_log')
def check_intersection(texts_list: list, keywords: set) -> bool:
    '''
    Checks if any of keywords present in text from text list
    :param texts_list: list of strings with article texts
    :param keywords: list of words to be searched
    :return: True if any word is found, False if neither word is found
    '''
    texts_string = ' '.join(texts_list)
    split_pattern = r'[а-яёА-ЯЁa-zA-Z-]+'
    tokens = set(re.findall(split_pattern, texts_string))
    if tokens & keywords:
        return True
    else:
        return False


@logger('scrapper_log')
def cook_soup(url: str, headers: dict) -> object:
    '''
    Makes get-request to url and creates bs4.BeautifulSoup object
    :param url: url for get-request
    :param headers: headers for get-request
    :return: soup
    '''
    response = requests.get(url, headers=headers)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    return soup


@logger('scrapper_log')
def get_articles(soup: object, tag: str) -> list:
    '''
    Gets list of articles from bs4.BeautifulSoup object
    :param soup: bs4.BeautifulSoup object
    :param tag: search tag
    :return: list of articles
    '''
    articles = soup.find_all(class_=tag)
    return articles


@logger('scrapper_log')
def check_articles_preview(article: object, possible_tags: list, keywords: set) -> bool:
    '''
    Collects text from all preview blocks and checks whether any words from keywords are present in text or not
    :param article: bs4.BeautifulSoup object
    :param possible_tags: list of possible tags where preview text can be found
    :param keywords: keywords to be found
    :return: True if intersection is found, otherwise False
    '''
    preview_list = []
    for tag in possible_tags:
        preview = article.find_all(class_=tag)
        for element in preview:
            preview_list.append(element.text)
    return check_intersection(preview_list, keywords)


@logger('scrapper_log')
def get_articles_params(article: object, date_tag: str, address_tag: str, title_tag: str) -> list:
    '''
    Gets article parameters: date, title and link
    :param article: bs4.BeautifulSoup object
    :param date_tag: tag where date may be found
    :param address_tag: tag where link may be found
    :param title_tag: tag where title may be found
    :return:
    '''
    date = article.find(class_=date_tag)
    address = article.find(class_=address_tag)
    title = address.find(title_tag)
    url = 'https://habr.com' + address['href']
    return [date.text, title.text, url]


@logger('scrapper_log')
def get_html_tag_text(article: object, html_tag: str, text_list: list) -> None:
    '''
    Gets text from group of same html tag and appends it to list
    :param article: bs4.BeautifulSoup object
    :param html_tag: name of tag
    :param text_list: list to add text
    :return: None, amends incoming list
    '''
    paragraphs = article.find_all(html_tag)
    for paragraph in paragraphs:
        text_list.append(paragraph.text)


@logger('scrapper_log')
def get_article_text(article: object, tags: list, html_tags: list) -> list:
    '''
    Gets  full article text from all possible tags where text can be found and from all html tags chosen by user
    :param article: bs4.BeautifulSoup object
    :param tags: tags with article full text
    :param html_tags: list if tags with parts of text
    :return: list of strings with full article text
    '''
    text_list = []
    for tag in tags:
        article_text = article.find(class_=tag)
        if article_text:
            for html_tag in html_tags:
                get_html_tag_text(article, html_tag, text_list)
    return text_list


if __name__ == "__main__":
    KEYWORDS = {'в', 'и', 'на', 'я'}
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

    soup = cook_soup('https://habr.com/ru/all/', HEADERS)

    articles = get_articles(soup, "tm-articles-list__item")
    for article in articles:
        possible_tags_list = ["article-formatted-body article-formatted-body article-formatted-body_version-2",
                              "article-formatted-body article-formatted-body article-formatted-body_version-1"]
        if check_articles_preview(article, possible_tags_list, KEYWORDS):
            parameters = (get_articles_params(article,
                                              "tm-article-snippet__datetime-published",
                                              "tm-article-snippet__title-link",
                                              'span'))
            print(f'{parameters[0]} - {parameters[1]} - {parameters[2]}')

    # print('--------Дополнительное задание------------')
    #
    # for article in articles:
    #     parameters = (get_articles_params(article,
    #                                       "tm-article-snippet__datetime-published",
    #                                       "tm-article-snippet__title-link",
    #                                       'span'))
    #     article_soup = cook_soup(parameters[2], HEADERS)
    #     possible_tags_list = ["article-formatted-body article-formatted-body article-formatted-body_version-2",
    #                           "article-formatted-body article-formatted-body article-formatted-body_version-1"]
    #     possible_html_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'ul', 'a']
    #     '''От статьи к статье могут быть и другие теги, например, заголовки меньше h5, в некоторых статьях текст
    #     был даже в div, и если для этих статей доставать текст из div, в других доставались елочки внутренностей.
    #     Из-за этого статьи в выборке по preview могут присутствовать, а в дополнительной нет, хотя текст preview
    #     есть в основной статье. Если нужна дополнительная проверка, просто добавьте div в список тегов.'''
    #     article_text = get_article_text(article_soup, possible_tags_list, possible_html_tags)
    #     if check_intersection(article_text, KEYWORDS):
    #         print(f'{parameters[0]} - {parameters[1]} - {parameters[2]}')
