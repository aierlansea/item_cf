from __future__  import  division
import sys
sys.path.append("../util")
import util.reader as reader
import math
import operator

def base_contribute_score():
    return 1
def cal_item_sim(user_click):
    co_appear={}
    item_user_click_time={}
    for user,itemlist in user_click.items():
        for index_i in range(0,len(itemlist)):
            itemid_i=itemlist[index_i]
            item_user_click_time.setdefault(itemid_i,0)
            item_user_click_time[itemid_i]+=1
            for index_j in range(index_i+1,len(itemlist)):
                itemid_j=itemlist[index_j]
                co_appear.setdefault(itemid_i,{})
                co_appear[itemid_i].setdefault(itemid_j,0)
                co_appear[itemid_i][itemid_j]+=base_contribute_score()

                co_appear.setdefault(itemid_j,{})
                co_appear[itemid_j].setdefault(itemid_i,0)
                co_appear[itemid_j][itemid_i]+=base_contribute_score()
    item_sim_score={}
    item_sim_score_sorted={}
    for itemid_i,relate_item in co_appear.items():
        for itemid_j,co_time in relate_item.items():
            sim_score=co_time/math.sqrt(item_user_click_time[itemid_i]*item_user_click_time[itemid_j])
            item_sim_score.setdefault(itemid_i,{})
            item_sim_score[itemid_i].setdefault(itemid_j,0)
            item_sim_score[itemid_i][itemid_j]=sim_score
    for itemid in item_sim_score:
        item_sim_score_sorted[itemid]=sorted(item_sim_score[itemid].iteritems(),key=\
                                        operator.itemgetter(1),reverse=True)

    return item_sim_score_sorted
def cal_recom_result(sim_info,user_click):
    recom_info={}
    topk=5
    recent_click_num=3
    for user in user_click:
        click_list=user_click[user]
        recom_info.setdefault(user,{})
        for itemid in click_list[:recent_click_num]:
            if itemid not in sim_info:
                continue
            for itemzuhe in sim_info[itemid][:topk]:
                itemsimid=itemzuhe[0]
                itemsimscore=itemzuhe[1]
                recom_info[user][itemsimid]=itemsimscore
    return recom_info





def main_flow():
    user_click=reader.get_user_click("../data/ratings.txt")
    sim_info=cal_item_sim(user_click)
    recom_result=cal_recom_result(sim_info,user_click)
    print (recom_result['1'])

if __name__=="__main__":
    main_flow()