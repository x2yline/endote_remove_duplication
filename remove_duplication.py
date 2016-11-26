from Levenshtein import ratio
import re
import os
import datetime
start = datetime.datetime.now()
print start
file_list =os.listdir( os.getcwd())
file1 =''
file2 =''
file3 =''
file4 =''
file5 =''
file6 =''
try:
    for file in file_list:
        if file.strip()[0] == '1':
            file1 = file
        if file.strip()[0] == '2':
            file2 = file
        if file.strip()[0] == '3':
            file3 = file
        if file.strip()[0] == '4':
            file4 = file
        if file.strip()[0] == '5':
            file5 = file
        if file.strip()[0] == '6':
            file6 = file
except:
    pass
removed_file_title = ''
def compare_xml(filex,filey):
    global removed_file_title
    f1= open(filex,'r')
    alltext1 = f1.read().decode('utf-8')
    f1.close()
# print alltext1
    all_list1 = alltext1.split('</record>')
# print all_list1[1],len(all_list1)
    year_list1 = re.findall('<year><style .*?size="100%">(.*?)</style></year>',alltext1)
    print  '\n----------------------------------------------------------------------------------------------------------\n < '+filex + ' > have ' + str(len(year_list1)) + 'items'
    author_list1 = re.findall('<authors>(.*?)</authors>',alltext1)
    # print len(author_list1)
    title_list1 = re.findall('<title><style .*?>(.*?)</style></title>',alltext1)
    # print title_list1[1].lower() == title_list1[0].lower()

    f2 = open(filey,'r')
    alltext2 = f2.read().decode('utf-8')
    f2.close()
    # print alltext2
    all_list2 = alltext2.split('</record>')
    # print all_list2[1],len(all_list2)
    year_list2 = re.findall('<year><style .*?size="100%">(.*?)</style></year>',alltext2)
    print  ' < '+filey + ' > have ' + str(len(year_list2))+ 'items'
    author_list2 = re.findall('<authors>(.*?)</authors>',alltext2)
    # print len(author_list2)
    title_list2 = re.findall('<title><style .*?>(.*?)</style></title>',alltext2)
    # print len(title_list2)

    # duplicated = []
    duplicated21 = []
    # print len(title_list1),len(title_list2)
    for i in range(len(title_list2)):
        for j in range (len(title_list1)):
            a = re.findall('<abstract>.*?size="100%">(.*?)</style></abstract>',all_list2[i] ,re.S)
            b = re.findall('<abstract>.*?size="100%">(.*?)</style></abstract>',all_list1[j],re.S) 
            # print title_list2[i].lower().strip('[]')
            # print title_list1[j].lower().strip('[]')
            # print '\n\n'
            if title_list2[i].lower().strip('[]') == title_list1[j].lower().strip('[]') and year_list2[i].lower() ==year_list1[j].lower():
                # duplicated.append('2-'+str(i+1)+' and 1-'+str(j+1)+'\n')
                duplicated21.append(i+1)
                removed_file_title = title_list1[j].lower().strip('[]') + '\n' + title_list2[i].lower().strip('[]') + '\n\n'
                # print 'found \n\n'
            elif  a and b and year_list2[i].lower() ==year_list1[j].lower():
                    rate = ratio(a[0].strip().lower() ,b[0].strip().lower())
                    if  rate >0.93  and len(a[0])>160:
                        print '\nSimilarity: ' + str(rate)
                        print 'Length: ' + str(len(a[0]))
                        if rate < 0.97:
                            try:
                                print type(title_list2[i])
                                print title_list2[i]
                                print title_list1[j],'\n\n'
                            except:
                                print 'print error'
                        # print 'found ' + str(i)
                        duplicated21.append(i+1)
                        removed_file_title = title_list1[j].lower().strip('[]') + '\n' + title_list2[i].lower().strip('[]') + '\n\n'
    print  '\n******************************************************************************\n'+filey + ' duplicate with '+filex +' for ' + str(len(duplicated21)) + ' items' + '\n******************************************************************************\n\n'
    new_group2list = alltext2.split('<record>')
    new_group2 = new_group2list[0]

    for k in range(len( new_group2list)):
        # print k,duplicated21
        if  k!=0 and k not in duplicated21:
            new_group2=new_group2 + '<record>' + new_group2list[k].split('</records>')[0]
        new_group2 = new_group2 + '</records></xml>'
    f = open('new_'+filey,'w')
    f.write(new_group2.encode('utf-8'))
    f.close()
    print '\n******************************************************************************\n'+'Have generate newfile for ' + filey + '\n******************************************************************************\n\n'

compare_xml(file1,file2)
file2 = 'new_' + file2
#delete file2
if file3:
    compare_xml(file2,file3)
    file3 = 'new_' + file3
    compare_xml(file1,file3)
    file3 =  'new_' +file3
if file4:
    compare_xml(file1,file4)
    file4 = 'new_' + file4
    compare_xml(file2,file4)
    file4 =  'new_' + file4
    compare_xml(file3,file4)
    file4 =   'new_' + file4
print 'All things have been done!!!!!!'
end = datetime.datetime.now()
times = 'Using time: \n\tfrom '+str(start) + 'to' + str(end)
print 'Using time: \n\tfrom '+str(start) + 'to' + str(end)
f = open('timelog.txt','w')
f.write(removed_file_title + '\n\n\n\n' + times )
f.close()


