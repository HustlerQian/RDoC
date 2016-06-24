#=-= coding=utf-8 =-=
import libxml2,re,os

pattern_Half_format=u': '



def parseXML(XMLPath) :
    doc = libxml2.parseFile(XMLPath)
    for text in doc.xpathEval('//RDoC/TEXT') :
        return text.content
    doc.freeDoc()

def CleanText(content):
    content_list=content.split(u'\n')
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
            #处理上一行value进入下一行 LIKE 29Sex: Female
            #如果前两个字符首字母非大写，则出问题
            #if not re.search(u'[A-Z]',line[0:2]):
                
            #    print line.split(u':')[0]
            #处理句中-分割符 LIKE Subject: Patient Initial Visit Note -Identifying Information Date of Service: 
            if re.search('[^\w]+-[A-Z]',line):
                print line,u'\n'
                line=line.split(u'-')
                line1=line[0]
                line2=line[1]
                #处理成2行，‘-’前为一行
                NewText[Newline_no]={'Text':line1,'Rawline_no':line_no}
                Newline_no+=1
                NewText[Newline_no]={'Text':'-'+line2,'Rawline_no':line_no}
            else:
                NewText[Newline_no]={'Text':line,'Rawline_no':line_no}
            
            
            
            #判断是否为半结构化数据
            #暂时该功能不用
            #if re.search(pattern_Half_format,line):
            #    NewText[Newline_no]={'Text':line,'Rawline_no':line_no}
            

    return NewText
        
def writeNewText(NewText):
    out_write=open(out_path,'w')
    for line_no in sorted(NewText.keys()):
        out_write.write('%s\n'%(NewText[line_no]['Text'].encode('utf-8')))
        
    out_write.close()

    
    
if __name__=='__main__':
    #test for one xml
    open_path='..\\split_1to4\\Tj_Train\\0007_gs.xml'
    out_path='..\\result\\Tj_Train\\0007_gs.txt'
    content = parseXML(open_path)
    NewText=CleanText(content)
    
    #写入新文件
    writeNewText(NewText)
    
    #for root,dirs,filelists in os.walks:
    
    print 1

