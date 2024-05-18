# Discord Bot "Shirube"
## Overview
Shirube(廸無 導, Shirube Michinashi)は学生をサポートする様々な機能を持ったDiscord Botです。時間割表示機能、ChatGPTによる会話機能、Google検索機能、Wikipedia検索機能、その他雑多な機能があります。
## Requirement
```
- Linux (WSL2, Raspbian 10)
- Python 3.8.10
- discord.py
- habachen
- openai
- bs4
```
## Preparation
Run these commands
```bash
mv shirubed.service /lib/systemd/system/
$ sudo systemctl list-unit-files --type=service | grep shirubed
systemctl enable shirubed
systemctl daemon-reload
```