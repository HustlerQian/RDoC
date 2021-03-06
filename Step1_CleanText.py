#=-= coding=utf-8 =-=
import libxml2,re,os

pattern_Half_format=u': '




def parseXML(XMLPath) :
    doc = libxml2.parseFile(XMLPath)
    for text in doc.xpathEval('//RDoC/TEXT') :
        return text.content
    doc.freeDoc()

def CleanText(content):
    content_list=content.split('\n')
    #行号
    line_no=0
    #newText
    NewText={}
    Newline_no=0
    for line in content_list:
        line_no+=1
        line = line.strip()
        
        #print line_no,line
        if len(line)!=0:
            Newline_no+=1
            #处理line
            #判断是否分割行
            HASsplitline=0
                
            #    print line.split(u':')[0]
            #对行号有改变
            #处理句中-分割符 LIKE Subject: Patient Initial Visit Note -Identifying Information Date of Service:   
            if re.search('[^\w]+-[A-Z]',line):
                #errorwrite.write(line+'\n')
                #print line,u'\n'
                #已找到的item分割
                item=re.search('[^\w]+-[A-Z]',line).group(0)
                line_split=line.split(item)
                item=item.split('-')
                line1=line_split[0]+item[0]
                line2='-'+item[1]+line_split[1]
                #处理成2行，‘-’前为一行
                NewText[Newline_no]={'Text':line1,'Rawline_no':line_no}
                Newline_no+=1
                NewText[Newline_no]={'Text':'-'+line2,'Rawline_no':line_no}
                HASsplitline=1
            else:
                NewText[Newline_no]={'Text':line,'Rawline_no':line_no}
            

            #可能要另写一个function
            #不会改变行号    
            #处理上一行value进入下一行 LIKE 29Sex: Female     
            #LIKE (5/20/66) TSH-2.85; (6/21/77)-testosterone-WNLPertinent Medical Review of Systems Constitutional:
            #如果大写字母前面出现数字，小写字母或者我们给定的group
            
            #把pattern左右各拓宽一个字符， addedby wyq,2016/6/22
            pattern='.[a-z0-9][A-Z].'
            #NOTICE!!! Addition_group元素不能重复
            #加入一些values是大写的pattern
            #Addition_group '.\."' addedby wyq,2016/6/22
            Addition_group=['WNL','GED','.\."']
            for i in Addition_group:
                pattern+='|.'+i+'[A-Z].'
            match_item=re.findall(pattern,line)
            #改成pattern的group
            out_group=['PhD','EtOH','[0-9]MG','qHS','[0-9][0-9]F']
            if match_item:
                #如果分割行则需要把行数-1
                if HASsplitline==1:
                    Newline_no+=-1
                errorwrite.write(NewText[Newline_no-1]['Text']+'\n')
                errorwrite.write(NewText[Newline_no]['Text']+'\n')
                
                
                #处理NewText字典,排除outgroup的可能
                for item in match_item:
                    errorwrite.write(item+'\n')
                    #split方法
                    HASout=0
                    for pattern_out in out_group:
                        if re.search(pattern_out,item):
                            HASout=1
                    if HASout==0:
                    #if not item in out_group:
                        line2back=NewText[Newline_no]['Text'].split(item)[0]+item[:-2]
                        line2stay=item[-2:]+NewText[Newline_no]['Text'].split(item)[1]
                        NewText[Newline_no-1]['Text']+=' '+line2back
                        NewText[Newline_no]['Text']=line2stay
                        errorwrite.write(line2back+'\n')
                        
                        
                    
                    #index的方法
                    #index=NewText[Newline_no]['Text'].find(item)
                    #item=NewText[Newline_no]['Text'][index-1:index+2]
                    #Additem=NewText[Newline_no]['Text'][index:index+3]
                    ##Addition_group的元素index和最初规则不同
                    #for pattern_AG in Addition_group:
                    #    if re.search(pattern_AG,Additem):
                    #        index+=2
                    #if not item in out_group: 
                    #    errorwrite.write(NewText[Newline_no]['Text'][:index+1]+'\n')
                    #    #返回item到上一行，并删除这一行的
                    #    NewText[Newline_no-1]['Text']+=' '+NewText[Newline_no]['Text'][:index+1]
                    #    NewText[Newline_no]['Text']=NewText[Newline_no]['Text'][index+1:]
                
                #分割错误输出
                errorwrite.write('++++++++++++++\n')
            
            #判断是否为半结构化数据
            #暂时该功能不用
            #if re.search(pattern_Half_format,line):
            #    NewText[Newline_no]={'Text':line,'Rawline_no':line_no}
            

    return NewText
        
def writeNewText(NewText,out_path):
    out_write=open(out_path,'w')
    for line_no in sorted(NewText.keys()):
        out_write.write('%s\n'%(NewText[line_no]['Text']))
        
    out_write.close()

    
    
if __name__=='__main__':
    #test for one xml
    #open_path='..\\split_1to4\\Tj_Train\\0007_gs.xml'
    #out_path='..\\result\\Tj_Train\\0007_gs.txt'
    #content = parseXML(open_path)
    #NewText=CleanText(content)
    
    #写入新文件
    #writeNewText(NewText)
    
    
    #For a dirs
    open_path='..\\split_1to4\\Tj_Train\\'
    out_path='..\\result\\Tj_Train\\'
    #记录error信息
    error_info='.\\error_info.txt'
    errorwrite=open(error_info,'w')
    for root,dirs,filelists in os.walk(open_path):
        for filename in filelists:
            path=os.path.join(root,filename)
            content=parseXML(path)
            NewText=CleanText(content)
            path=os.path.join(out_path,filename[:-3]+'txt')
            writeNewText(NewText,path)
            errorwrite.write(path+'\n')
            #writeNewText(NewText,path)
            errorwrite.write('===============================\n')        
    errorwrite.close()
    

