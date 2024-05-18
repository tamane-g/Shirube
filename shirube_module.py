import re
import sys
import discord
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

# 全サーバーへのメッセージ送信
async def all_guild_send(client, message):
    for guild in client.guilds:
        channel = channel_search(guild)
        if channel:
            print("send \"" + message + "\" to \"" + guild.name + "\"")
            await channel.send(message)
    print()

# メッセージが送信可能なチャンネルを検索
def channel_search(guild):
    for channel in guild.channels:
        if channel.permissions_for(guild.me).send_messages and type(channel) is discord.TextChannel:
            return channel
    return False

# 高専の最新ニュースを取得
# latest_news.txtにyyyyMMddを格納
async def check_news(client):
    res = requests.get('https://www.tomakomai-ct.ac.jp/news')
    soup = BeautifulSoup(res.text, 'html.parser')
    res = requests.get(soup.find('li', class_='news_item').find('a').get('href'))
    soup = BeautifulSoup(res.text, 'html.parser')
    news_title = soup.find('h1').get_text()
    news_date = soup.find('span', class_='date').get_text().strip()
    news_date_num = int(news_date.replace(".", ""))
    news_texts = soup.find(attrs={'class':['element_grp_text','element_grp_link']}).find_all(['a','p'])
    
    with open("latest_news.txt", "r") as f:
        late_date_num = int(f.read())
    
    if(news_date_num > late_date_num):
        sent  = "苫小牧高専ホームページのお知らせが更新されました。\nURL: https://www.tomakomai-ct.ac.jp/news\n======================================\n"
        sent += news_title + news_date + "\n"
        for text in news_texts:
            sent += text.get_text() + "\n"

        print(str(late_date_num) + " => " + str(news_date_num))
        with open("latest_news.txt", "w") as f:
            f.write(str(news_date_num))

        await all_guild_send(client, sent)

# Googleスクレイピング
def search_google(searchwords):
    if searchwords != None:
        try:
            print("google " + searchwords)
            load_url = "https://www.google.com/search?q=" + searchwords.replace(" ","+").replace("　","+")
            print(load_url)
            html = requests.get(load_url)
            soup = BeautifulSoup(html.content, "html.parser")
            link_title = soup.select(".kCrYT > a")
            result = "了解いたしました。\n以下が「" + searchwords + "」の検索結果上位3サイトです。\n======================================\n"
            length = len(link_title) if len(link_title) < 3 else 3 
            for i in range(length):
                result += link_title[i].find("h3").get_text() + "\n"
                hoge = unquote(link_title[i].get("href").replace("/url?q=",""))
                result += hoge[0:hoge.find("&sa=U")] + "\n\n"
            return result
            
        except Exception as e:
            f = open('bot_error.txt', 'w', encoding='UTF-8')
            f.write("type : " + str(type(e)) + "\n")
            f.write("type : " + str(e.args) + "\n")
            f.write("type : " + str(e) + "\n")
            f.write("source : " + str(soup) + "\n")
            f.close()
            return "申し訳ありません。検索結果を取得できませんでした。（" + str(type(e)) + "）\nエラーの詳しい内容はbot_error.txtを参照してください。"
    else:
        return "検索対象を指定してください。"

# Wikipediaスクレイピング
def search_wiki(searchwords):
    if searchwords != None:
        result = ""
        print("wikipedia " + searchwords)
        result_url = "https://ja.wikipedia.org/w/index.php?search=" + searchwords.replace(" ","+").replace("　","+")
        html = requests.get(result_url)
        soup = BeautifulSoup(html.content, "html.parser")
        if soup.select(".firstHeading")[0].get_text() == "検索結果":
            result += "検索の結果wikipediaにそのような項目はありませんでした。\nwikipedia検索結果上位に該当する項目は以下です。\n======================================\n"
            link_title = soup.select("div.mw-search-result-heading > a")
            length = len(link_title) if len(link_title) < 3 else 3 
            if length == 0:
                result = "wikipediaにそのような項目はありませんでした。\nwikipedia検索においても該当するページはありませんでした。\n検索ワードを変えて試してみてはいかがでしょうか。"
            for i in range(length):
                result += link_title[i].get("title") + "\n"
                print(link_title[i].get("href"))
                result += "https://ja.wikipedia.org" + unquote(link_title[i].get("href")) + "\n\n"
        else:
            result += soup.select(".firstHeading")[0].get_text() + "\n"
            for i in soup.select(".mw-perser-output > p"):
                result += i.get_text()
            result += "\n参照元\n" + result_url.replace("%","%%")
        return result
    else:
        return "検索対象を指定してください。"
