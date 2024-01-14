"""
4次元配列として扱える辞書型変数[学年][組][曜日][時間]を定義
jsonファイルとして出力し、schedule_inputで入力できるようにする
キーはそれぞれ0から始まる自然数によって定義される(1組 → 0)
"""

# coding: utf-8
import json

day_name   = ["月","火","水","木","金","土","日"]

schedule = {}
sp_years = ["専攻科1年","専攻科2年"]

# 1~5学年,1~5組,月~日曜日
for year_num in range(5):
    schedule.setdefault(year_num, {})
    for class_num in range(5):
        schedule[year_num].setdefault(class_num, {})
        for day_num in range(7):
            schedule[year_num][class_num].setdefault(day_num, {})
            for j_num in range(8):
                schedule[year_num][class_num][day_num].setdefault(j_num)

# 専攻科1,2年,月~日曜日
# 専攻科は仕様上全員1組として扱う
for sp_year in range(5,7):
    schedule.setdefault(sp_year, {})
    schedule[sp_year].setdefault(1, {})
    for day_num in range(7):
        schedule[sp_year][1].setdefault(day_num, {})
        for j_num in range(8):
            schedule[sp_year][1][day_num].setdefault(j_num)


"""

特殊コースは組と同列に扱い、
出力時は組別の時間割に加えて表示する。

"""
# 1~5学年,留学生(6組),月~日曜日
for year_num in range(5):
    schedule[year_num].setdefault(5, {})
    for day_num in range(7):
        schedule[year_num][5].setdefault(day_num, {})
        for j_num in range(8):
            schedule[year_num][5][day_num].setdefault(j_num)

# 4~5学年,機能材料(7組),食品・バイオコース(8組),月~日曜日
for year_num in range(3,5):
    for cource in range(6,8):
        schedule[year_num].setdefault(cource, {})
        for day_num in range(7):
            schedule[year_num][cource].setdefault(day_num, {})
            for j_num in range(8):
                schedule[year_num][cource][day_num].setdefault(j_num)

# 4~5学年,フロンティアコース(9組),月~日曜日
for year_num in range(3,5):
    schedule[year_num].setdefault(8, {})
    for day_num in range(7):
        schedule[year_num][8].setdefault(day_num, {})
        for j_num in range(8):
            schedule[year_num][8][day_num].setdefault(j_num)

f = open("schedule.json", 'w')

print(schedule)
json.dump(schedule, f, indent=2)