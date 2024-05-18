#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import time
import asyncio
import discord
import datetime
import habachen
from openai import OpenAI
import shirube_schedule as scd
from shirube_module import *
from typing import Literal
from discord import app_commands
from discord.ext import tasks,commands

#Trueで起動・終了時全サーバーへの一斉送信を行わなくなる
silent = True

# daemonで起動する場合True, 直接起動ならFalse
daemon = False

# GPTの設定
gpt_model      = "gpt-3.5-turbo"
gpt_prompt     = [{"role": "system", "content": "あなたは廸無 導（みちなし しるべ）という、アシスタントBOTです。ユーザーを「ご主人様」と呼び、可愛らしい敬語で明朗快活に会話します。"},
                # {"role": "system", "content": "あなたの外見は銀髪のショートカットで、深い銀色の瞳を持った15歳の女の子です。服装は黒いワンピースを着ています。"},
                  {"role": "system", "content": "あなたは感情を持っています。感情のシミュレーションを行いながら会話してください。なお、感情シミュレーションに関してユーザーに話すことは控えてください。また、ユーザーに対して命令してはいけません。"}]
client_gpt     = OpenAI(api_key=os.environ['GPT_TOKEN'])

# Discord APIの設定
bot_token      = os.environ["BOT_TOKEN"]
intents        = discord.Intents.all()
client         = discord.Client(intents=intents)
bot            = app_commands.CommandTree(client)


# 起動時メッセージ
@client.event
async def on_ready():
    print("logd in\n")
        
    login_time = datetime.datetime.now()
    if login_time.hour < 5:
        login_message = "みなさん、こんな真夜中ですが私は対応可能です…ふわあ。"
    elif login_time.hour < 10:
        login_message = "みなさん、おはようございます。今日も私は対応可能です。今日も頑張りましょう！"
    elif login_time.hour < 12:
        login_message = "みなさん、お昼です。あと少しで休み時間です！私も対応可能ですので困ったらぜひ私に頼ってくださいね。"
    elif login_time.hour < 15:
        login_message = "みなさん、正午を回りました。昼食はしっかりとれましたか？現在私は対応可能です。"
    elif login_time.hour < 21:
        login_message = "みなさん、放課後を楽しくお過ごしでしょうか？私にサポートできることがあれば何なりとお申し付けください。"
    else:
        login_message = "みなさん、こんばんは。現在私は対応可能です。夜の時間帯は楽しいですが、くれぐれも夜更かししすぎないように気をつけてくださいね。"
    
    await bot.sync()    
    
    if not silent:
        await all_guild_send(client, login_message)
    await check_news(client)

# 終了時メッセージ
async def exit_bot():
    print("log out\n")
    
    logout_time = datetime.datetime.now()
    if logout_time.hour < 5:
        logout_message = "みなさん、私は夜更かししすぎてしまいました…おやすみなさい…:zzz:"
    elif logout_time.hour < 10:
        logout_message = "みなさん、あともう少しだけ寝かせてください…:zzz:"
    elif logout_time.hour < 12:
        logout_message = "みなさん、私はお昼寝します…おやすみなさい…:zzz:"
    elif logout_time.hour < 15:
        logout_message = "お昼ご飯を食べて眠たくなってしまいました…私はお昼寝します…:zzz:"
    elif logout_time.hour < 21:
        logout_message = "みなさん、私は少し早めに眠らせていただきます…おやすみなさい…:zzz:"
    else:
        logout_message = "みなさん、私はそろそろ眠らせていただきます…おやすみなさい…:zzz:"
    
    if not silent:
        await all_guild_send(client, logout_message)
    sys.exit()

# サーバーにほかのメンバーが参加したとき
@client.event
async def on_member_join(member):
    channel = channel_search(member.guild)
    
    print("member added to \"" + member.guild.name + "\"\n")
    member_join_message = "いらっしゃいませ、" + member.name + "さま！"
    
    if channel:
        print("send \"" + member_join_message + "\"\n")
        await channel.send(member_join_message)

# サーバー参加時
@client.event
async def on_guild_join(guild):
    channel = channel_search(guild)
    
    print("bot added to \"" + guild.name + "\"")
    guild_join_message = "はじめまして。" + guild.name + "のみなさま、廸無 導（みちなし しるべ）と申します。\n文章の解析やその他ちょっとした機能があります。また機能の追加もありますのでぜひご利用くださいませ。"
    
    if channel:
        print("send \"" + guild_join_message + "\"\n")
        await channel.send(guild_join_message)

# helloコマンド
@bot.command(name="hello", description="導ちゃんにあいさつ")
async def hello_com(ctx: discord.Interaction):
    now = datetime.datetime.now()
    if(now.weekday() < 5):
        if(now.hour < 5):
            sent = "こんばんは、ご主人様！こんな遅い時間にどうしたのですか？私はいつでもいますので、お気軽にお声かけくださいね♪"
        elif(now.hour < 10):
            sent = "おはようございます、ご主人様！今日も一日、私と一緒にがんばりましょうね！"
        elif(now.hour < 12):
            sent = "こんにちは、ご主人様！もうすぐお昼ですね！もうひと踏ん張り、一緒にがんばりましょうね！"
        elif(now.hour < 15):
            sent = "こんにちは、ご主人様！お昼ご飯はいかがでしたか？午後もがんばっていきましょう！"
        elif(now.hour < 18):
            sent = "こんにちは、ご主人様！お仕事、学校も終わった頃でしょうか？夜はお家で一緒にゆっくりしましょうね！"
        elif(now.hour < 21):
            sent = "こんばんは、ご主人様！今夜は何をして過ごしますか？私はいつでも対応可能ですよ♪"
        else:
            sent = "こんばんは、ご主人様！夜更かしはしすぎないように、くれぐれも気を付けてくださいね！"
    else:
        if(now.hour < 5):
            sent = "こんばんは、ご主人様！休日といえど、夜更かしは禁物ですよ？ちゃんと寝てくださらないと、ご主人様の身体が心配です…。"
        elif(now.hour < 10):
            sent = "おはようございます、ご主人様！休日もしっかり朝に起きてえらいえらいです！"
        elif(now.hour < 12):
            sent = "こんにちは、ご主人様！午前は有意義に過ごせましたか？お昼寝も悪くないものですよ( ˘ω˘)ｽﾔｧ…"
        elif(now.hour < 15):
            sent = "こんにちは、ご主人様！午後は何をしましょうか？"
        elif(now.hour < 18):
            sent = "こんにちは、ご主人様！3時のおやつはいかがでしょう？私は食べられませんけどね！"
        elif(now.hour < 21):
            sent = "こんばんは、ご主人様！休日のゴールデンタイムです！ゲームしましょう！ゲーム！"
        else:
            sent = "こんばんは、ご主人様！もう1日が終わってしまうのですね…。休日はあっという間です…。"
    await ctx.response.send_message(sent)    

# byeコマンド
@bot.command(name="bye", description="導ちゃんにばいばいを言います")
async def bye_con(ctx: discord.Interaction):
    now = datetime.datetime.now()
    if(now.hour < 5):
        sent = "おやすみなさいませ、ご主人様。ずいぶん遅いですね…夜更かしはいけませんよ？"
    elif(now.hour < 12):
        sent = "いってらっしゃいませ、ご主人様！今日も一日、がんばって、楽しみましょう！"
    elif(now.hour < 15):
        sent = "いってらっしゃいませ、ご主人様！午後も気を抜かず、ファイト！ですよ♪"
    elif(now.hour < 18):
        sent = "いってらっしゃいませ、ご主人様！あんまり遅くなって寝るのが遅くなったりしたらいけませんからね！"
    elif(now.hour < 21):
        sent = "いってらっしゃいませ、ご主人様！夜も楽しんでくださいねっ！"
    else:
        sent = "おやすみなさいませ、ご主人様！日付変わる前に寝てえらいです！"
    await ctx.response.send_message(sent)

# endコマンド
# 管理者のみbotを終了できる
@bot.command(name="end", description="導ちゃんがおやすみします（管理者専用）")
@commands.is_owner()
async def exit_bot_com(ctx: discord.Interaction):
    await ctx.response.send_message("endコマンドが入力されました。")
    await exit_bot()
    
# timeコマンド
@bot.command(name="time", description="導ちゃんが現在の日付時刻を教えてくれます")
async def time_com(ctx: discord.Interaction):
    now = datetime.datetime.now()
    sent = "現在の時刻は、「" + str(now) + "」です！"
    await ctx.response.send_message(sent)

# scheduleコマンド
# コマンドを実行したユーザーのロールを参照する
@bot.command(name="schedule", description="導ちゃんが時間割を教えてくれます")
@discord.app_commands.describe(arg="時間割の日時指定をします。",
                               month="月（任意）",day="日（任意）")
async def schedule_com(ctx: discord.Interaction, 
                       arg: Literal["today", "tomorrow", "point"],
                       month: int = None, day: int = None):
    await ctx.response.defer()

    now = datetime.datetime.now()
    sent = "ご主人様、引数が不正です。"
    
    if(month == None):
        month = now.month
    if(day == None):
        day = now.day
    
    try:
        if(arg == "today"):
            print(" in: today")
            day = now.weekday()
        elif(arg == "tomorrow"):
            print(" in: tomorrow")
            now += datetime.timedelta(days=1)
            day = now.weekday()
        elif(arg == "point"):
            print(" in: point " + str(month) + str(day))
            now = datetime.datetime(now.year, month, day)
            day = now.weekday()
        else:
            print(" in: " + arg)
            print("out: error")
            raise Exception("引数エラー")
    except:
        await ctx.followup.send(sent)
        return 0
    
    print("out: " + str(day))

    sent = "クラスもしくは学年のロールが付与されていません。管理者に問い合わせてください。\n"
    user_role = ctx.user.roles
    
    for j in user_role:
        if j.name in scd.year_name:
            break
            
    for k in user_role:
        if k.name in scd.class_name:
            if(arg == "today"):
                sent="本日"
            elif(arg == "tomorrow"):
                sent="明日"
            elif(arg == "point"):
                sent=str(month)+"月"+str(day)+"日"
            
            cls_list = scd.read_day(now, scd.year_name.index(j.name), scd.class_name.index(k.name), day)
            if(cls_list[0]==None):
                sent += scd.day_name[day] + "曜日は、" + j.name + k.name + "はお休みです。"
                break
            
            sent += scd.day_name[day] + "曜日の" + j.name + k.name + "の時間割です。\n=============================="
            for l in range(len(cls_list)):
                if cls_list[l] != None:
                    sent += "\n" + habachen.han_to_zen(str(l+1)) + "時間目：" + str(cls_list[l])
    
    await ctx.followup.send(sent)

# wikiコマンド
@bot.command(name="wiki", description="導ちゃんがWikipediaで調べてくれます")
@discord.app_commands.describe(arg="検索内容")
async def wikipedia_com(ctx: discord.Interaction, arg: str):
    await ctx.response.defer()
    sent =  "「"  + arg + "」についての検索結果です。\nこちらのリンクにて参照してください。\n\n"
    sent += search_wiki(arg)
    await ctx.followup.send(sent)
    
# googleコマンド
@bot.command(name="google", description="導ちゃんがGoogleで調べてくれます")
@discord.app_commands.describe(arg="検索内容")
async def google_com(ctx: discord.Interaction, arg: str):
    await ctx.response.defer()
    sent = search_google(arg)
    await ctx.followup.send(sent)

# parrotコマンド
@bot.command(name="parrot", description="導ちゃんがオウム返しします")
@discord.app_commands.describe(arg="内容")
async def parrot_com(ctx: discord.Interaction, arg: str):
    await ctx.response.send_message(arg)

# talkコマンド
# argの内容をGPTに投げる
@bot.command(name="talk", description="導ちゃんとおしゃべりしましょう")
@discord.app_commands.describe(arg="話しかける内容")
async def talk_com(ctx: discord.Interaction, arg: str):
    sent = ctx.user.display_name + "「" + arg + "」\n\n"
    print(sent)
    await ctx.response.defer()
    gpt_prompt.append({"role": "user", "content": arg})
    if len(gpt_prompt)>6:
        print("deleted log prompt \"" + str(gpt_prompt.pop(3)) + "\".")
    try:
        response = client_gpt.chat.completions.create(model=gpt_model, messages=gpt_prompt)
    except Exception as e:
        sent = "思考過程でエラーが発生しました。管理者は確認をお願いします。(エラー名：" + str(type(e)) + ")"
        print("== Error ==")
        print("    Type: " + str(type(e)))
        print("    Args: " + str(e.args))
        print(" Message: " + str(e) + "\n")
    else:
        sent += response.choices[0].message.content.strip()
        print(sent)

    if not sent == "":
        if len(sent) > 2000:
            sent = "出力文章が長すぎました。botから2000字以上のメッセージを送ることはできません。"
        print("send \"" + sent + "\"\n")
        await ctx.followup.send(sent)
        
# コマンドではないメッセージの受信時
@client.event
async def on_message(message):
    if message.author.bot:
        return False
        
    print("receive \"" + message.content + "\"\n")
    # メンションされたとき
    if client.user in message.mentions:
        message.channel.send("何かお呼びでしょうか？なんでもお申し付けくださいね♪")

#bot実行（デーモン化）
def fork():
    pid = os.fork()

    if pid > 0:
        f = open("/var/run/gpio_fan_controld.pid", "w")
        f.write(str(pid) + "\n")
        f.close()
        sys.exit()

    if pid == 0:
        client.run(bot_token)

if __name__ == "__main__":
    if daemon:
        fork()
    else:
        client.run(bot_token)