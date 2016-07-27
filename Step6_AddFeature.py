#=-= coding=utf-8 =-=
import json,os

def Add_item(load_matrix,add_matrix,item_list,value_list=None):
    for filename in load_matrix:
        #可能add_matrix key不同
        if not add_matrix.has_key(filename):
            filename_add=filename[:4]
        else:
            filename_add=filename
        #item_list对应的value 比如current这个item里，既有value也有descripition
        if value_list!=None:
            for item in item_list:
                index=item_list.index(item)
                value=value_list[index]
                load_matrix[filename][item]=add_matrix[filename_add][item][value]
        #没有多个value的
        else:
            for item in item_list:
                load_matrix[filename][item]=add_matrix[filename_add][item]
    return load_matrix


if __name__=='__main__':
    #读入的原始matrix
    load_matrix=json.load(open('..\\result\\train2\\file_item_mat_filtered.json','r'))
    New_Matrix={}
    #加入Axis5
    add_matrix=json.load(open('..\\result\\Axis5.json','r'))
    item_list=['Current']
    value_list=['value']
    New_Matrix=Add_item(load_matrix,add_matrix,item_list,value_list)
    #加入sentiment
    add_matrix=json.load(open('..\\result\\goldInfo_1to4+sentiment.json','r'))
    item_list=['sentiment_node']
    New_Matrix=Add_item(load_matrix,add_matrix,item_list)
    #输出的新matrix
    json.dump(New_Matrix,open('..\\result\\train2\\file_item_mat_Addfeature.json','w'),indent=4)