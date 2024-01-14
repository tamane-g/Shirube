"""
年,組,時間は内部的には実際の数値から-1した数値で扱う
時間割変更の実装
・"0":{"date": yyyyMMdd, "before": [hour_0, hour_1], "day": day, "after": [hour_2, hour3]}
・yyyyMMddなら、hour_0, hour_1をday曜日のhour_2, hour_3にする
・yyyyMMddが現在より過去なら削除する
"""
import json
import datetime

year_name  = ["1年", "2年", "3年", "4年", "5年", "専攻科1年", "専攻科2年"]
class_name = ["1組", "2組", "3組", "4組", "5組", "留学生"]
day_name   = ["月","火","水","木","金","土","日"]

# 学年,組,曜日,時間
mem_list = [0,0,0,0]

# 授業名
mem_str  = ""

# inputの返り値の仮変数
buf_str  = ""

# sc_dictに時間割データをロード
with open("schedule.json", 'r') as f:
    sc_dict = json.load(f)


def check_change(in_list, date, year, cls_):
    with open("scd_change.json", 'r') as f:
        cg_dict = json.load(f)

    out_list = in_list
    now = int(datetime.datetime.now().strftime('%Y%m%d'))
    ymd = int(date.strftime('%Y%m%d'))
    print("now = " + str(now))
    print("ymd = " + str(ymd))

    keys = list(cg_dict.keys())
    for key in keys:
        cg = cg_dict[key]
        print("cg[\"date\"] = " + str(cg["date"]))
        if(int(cg["date"]) == ymd):
            for i in range(len(cg["before"])):
                print(str(date))
                print(sc_dict[str(year)][str(cls_)][str(cg["day"])][str(cg["after"][i])] + "=>" + out_list[cg["before"][i]])
                out_list[cg["before"][i]] = sc_dict[str(year)][str(cls_)][str(cg["day"])][str(cg["after"][i])]
        
        elif(int(cg["date"]) < now):
            print(str(date))
            print("delete " + str(cg_dict[key]["date"]))
            del cg_dict[key]
            
    with open("scd_change.json", 'w') as f:
        json.dump(cg_dict, f, indent=2)
    
    return out_list


def read_day(date, year, cls_, day):
    rtn_list = list()
    
    for hour in range(8):
        rtn_list.append(sc_dict[str(year)][str(cls_)][str(day)][str(hour)])
    rtn_list = check_change(rtn_list, date, year, cls_)

    return rtn_list
        

def read(year, cls_, day, hour):
    return str(sc_dict[str(year)][str(cls_)][str(day)][str(hour)])