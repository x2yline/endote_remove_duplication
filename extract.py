
file = r'F:\meta\endnote\去重 demo\3.xml'
#
#xml_first = '<?xml version="1.0" encoding="UTF-8" ?><xml><records>'
#xml_last = '</records></xml>'

def read_file(file):
    '''file为endnote导出的xml文件路径，
    输出为一个unicode格式的string'''
    import chardet
    f = open(file,'r')
    Reads = f.read()
    f.close()
    Encoding = chardet.detect(Reads)
    alltext = Reads.decode(Encoding['encoding'])
    return alltext


def get_endnote_list(text):
    '''record_list包括所有的记录
    其格式为：<record>*******
    后面没有</record>
    
    输入为unicode的string
    输出结果为一个列表
    列表包括四个元素，每个原素又是一个列表
    依次为record,title，year，abstract，author
    
    endnote正则表达式如下'''
    #import re
    #year_list = re.findall('<year>.*?>(.*?)<.*?/year>',text,re.S)
    #title_list = re.findall('<title>.*?>(.*?)<.*?/title>',text,re.S)
    #abstract_list = re.findall('<abstract.*?>(.*?)<.*?/abstract>',text,re.S)
    #author_list = re.findall('<contributors>(.*?)</contributors>',text,re.S)
    record_list = text[text.find('<record>'):text.rfind('</records>')].split('</record>')[0:-1]
    year_list = []
    title_list = []
    abstract_list = []
    #    author_list = []
    for i in record_list:
        sys.stdout.write('#'"\b")
        sys.stdout.flush()
        try:
            year_list.append(i[i.find('<year>'):i.rfind('/year>')].split('>')[2][0:4])
        except:
            year_list.append('')
        try:
            abstract_list.append(i[i.find('<abstract>'):i.rfind('</abstract>')].split('>')[2].split('<')[0])
        except:
            abstract_list.append('')
        try:
            title_list.append(i[i.find('<title>'):i.rfind('</title>')].split('>')[2].split('<')[0])
        except:
            title_list.append('')
            #        try:
            #            author_list.append(i[i.find('<author><style'):i.find('</style></author>')].split('>')[2])
            #        except:
            #            author_list.append('')
    print '\n'
    return [record_list,title_list,year_list,abstract_list]

def remove_duplication(record_list,dup_list):
    '''输入所有记录的列表（record_list）和重复文献的索引列表（dup_list）
    输出新的xml文本'''
    new_list  = []
    new_file = '<?xml version="1.0" encoding="UTF-8" ?><xml><records>'
    print unicode('>')+'新纪录包括：',
    for i in range(len(record_list)):
        if i not in dup_list:
            new_file = new_file + record_list[i] + '</record>'
            new_list.append(i)
            print str(i+1) + ' ',
    new_file = new_file + '</records></xml>'
    return [new_file,new_list]





def self_duplication_removed(file):
    from Levenshtein import ratio
    record_list,title_list,year_list,abstract_list = get_endnote_list(read_file(file))
    self_dup_list = []
    for i in range(len(year_list)):
        sys.stdout.write('#'"\b")
        sys.stdout.flush()
        for j in range(i+1,len(year_list)):
            if title_list[i].lower().strip('[]') == title_list[j].lower().strip('[]') and year_list[i].lower() ==year_list[j].lower():
                self_dup_list.append(j)
                print '\n'
                print '第' + unicode(str(i)) + '篇文献: '+title_list[i] + '\n'
                print '第' + unicode(str(j)) + '篇文献: '+title_list[j] + '\n'
            elif abstract_list[i] and abstract_list[j] and year_list[i].lower() ==year_list[j].lower():
                rate = ratio(abstract_list[i].strip().lower() ,abstract_list[j].strip().lower())
                if  rate >0.93  and len(abstract_list[i])>160:
                    print '\n\n相似度: ' + unicode(str(rate))
                    print '摘要字数: ' + unicode(str(len(abstract_list[i].split(' ')))) + '\n'
                    if rate < 0.97:
                        try:
                            print '第' + unicode(str(i)) + '篇文献: ' + title_list[i],'\n'
                            print '第' + unicode(str(j)) + '篇文献: ' + title_list[j],'\n'
                        except:
                            print 'print error\n'
                    self_dup_list.append(j)
        
    print '\n识别出'+unicode(str(len(self_dup_list)))+'篇重复文献\n'
    new_file,new_list = remove_duplication(record_list,dup_list=self_dup_list)
    record_list_updated = [record_list[i] for i in new_list] 
    title_list_updated = [title_list[i] for i in new_list] 
    year_list_updated = [year_list[i] for i in new_list] 
    abstract_list_updated = [abstract_list[i] for i in new_list] 
    
    return [new_file,record_list_updated,title_list_updated,year_list_updated,abstract_list_updated]



new_file,record_list_updated,title_list_updated,year_list_updated,abstract_list_updated = self_duplication_removed(file)
