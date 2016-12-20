
file = r'F:\meta\endnote\去重 demo\1.xml'

xml_first = '<?xml version="1.0" encoding="UTF-8" ?><xml><records>'
xml_last = '</records></xml>'

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
    
text = read_file(file)

def get_endnote_list(text):
    '''records_list包括所有的记录
    其格式为：<record>*******
    后面没有</records>
    
    输入为unicode的string
    输出结果为一个列表
    列表包括四个元素，每个原素又是一个列表
    依次为title，year，abstract，author
    
    endnote正则表达式如下'''
    #import re
    #year_list = re.findall('<year>.*?>(.*?)<.*?/year>',text,re.S)
    #title_list = re.findall('<title>.*?>(.*?)<.*?/title>',text,re.S)
    #abstract_list = re.findall('<abstract.*?>(.*?)<.*?/abstract>',text,re.S)
    #author_list = re.findall('<contributors>(.*?)</contributors>',text,re.S)
    records_list = text[text.find('<record>'):text.find('</records>')].split('</record>')[0:-1]
    year_list = []
    title_list = []
    abstract_list = []
    author_list = []
    for i in records_list:
        sys.stdout.write('+'"\b")
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
        try:
            author_list.append(i[i.find('<author><style'):i.find('</style></author>')].split('>')[2])
        except:
            author_list.append('')
    return [title_list,year_list,abstract_list,author_list]

T,Y,Ab,Au = get_endnote_list(text)
