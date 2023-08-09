from flask import Flask
import requests
from lxml import etree


app = Flask(__name__)
root_url = 'https://news.hqu.edu.cn/hdyw.htm'
url = 'https://news.hqu.edu.cn/'


@app.route("/")
def root():

    return '''
       <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>hdxw</title>
    </head>
    <body>
        <a href="./hdxw">这是华大新闻的站点</a>
    </body>
    </html> 
    '''


@app.route("/hdxw")
def main():
    web = get_web(root_url)
    titles = get_title(web)
    outcome = save(titles)
    return outcome


def get_web(url_):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'

        }
    response = requests.get(url=url_, headers=headers)
    response.encoding = response.apparent_encoding

    page_text = response.text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//div[@class="Newslist"]//li')
    return li_list


def get_title(source):

    outcome = []
    for li in source:
        title = li.xpath('./a/text()')[0]
        # title_content = etree.tostring(title, pretty_print=True, encoding='utf-8', method='html').decode('UTF-8')
        outcome.append(title)
        link = url + li.xpath('./a/@href')[0]
        outcome.append(link)
    return outcome


def save(source):
    page = '''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>hdxw</title>
        <p>%s</p>
        <ul>%s</ul>
    </head>
     </html>
    '''
    ul = '''
    <li>
    <a href="%s">按标题顺序</a>
    </li>
    '''
    ul_ = ""
    p = '''
    <li>%s</li>
    '''
    p_ = ""
    for num in (0, str(len(source))):

        link = source[1::2]
        title = source[::2]
        for t in title:
            p_ += p % t
        for li in link:
            ul_ += ul % li

    return page % (p_, ul_)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")






