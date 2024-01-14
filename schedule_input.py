"""
    【時間割入力効率化プログラム】

    ・月火水木金土日はそれぞれ、0123456と表す

    ・学年 → 組 → 曜日 → 時間 → 授業名で入力

    ・無入力の場合は前の入力を引き継ぐ

    ・"end"で終了
"""

import json

year_name  = ["1年", "2年", "3年", "4年", "5年", "専攻科1年", "専攻科2年"]
class_name = ["1組", "2組", "3組", "4組", "5組", "留学生"]
day_name   = ["月","火","水","木","金","土","日"]

order_list = ["　学年：", "　　組：", "　曜日：", "　時間："]

with open("schedule.json", 'r') as f:
    sc_dict = json.load(f)

# 学年,組,曜日,時間
mem_list = [0,0,0,0]
# 授業名
mem_str  = ""

# inputの返り値の仮変数
buf_str  = ""

print()

while True:
    # 学年,組,曜日,時間の入力
    for i in range(4):
        buf_str = input(order_list[i]).strip()
        if buf_str == "end":
            break
        mem_list[i] = int(buf_str) if buf_str else mem_list[i]
    
    if buf_str == "end":
        break
    
    # 授業名の入力
    buf_str = input("授業名：").strip()
    mem_str = None if buf_str == "n" else buf_str if buf_str else mem_str
    
    print("\n" + year_name[mem_list[0]-1] + class_name[mem_list[1]-1] + " " + day_name[mem_list[2]] + "曜日 " + str(mem_list[3]) + "時間目 " + str(sc_dict[str(mem_list[0]-1)][str(mem_list[1]-1)][str(mem_list[2])][str(mem_list[3]-1)]) + "\u0020⇒\u0020\u0020"+ str(mem_str) + "\n")

    sc_dict[str(mem_list[0]-1)][str(mem_list[1]-1)][str(mem_list[2])][str(mem_list[3]-1)] = mem_str
    
print("\n===================================\n")
print(" Input stopped. Saving file now...\n")

with open("schedule.json", 'w') as f:
    json.dump(sc_dict, f, indent=2)
    