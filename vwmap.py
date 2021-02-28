import markdown
import os
from lxml import etree

# Reading the all files

path ="/home/tymancjo/Nextcloud/mynote/"
#we shall store all the file names in this list
filelist = []
masterlist = {}

for root, dirs, files in os.walk(path):
        for file in files:
        #append the file name to the list
            if ".md" in file:
                filelist.append([file, os.path.join(root,file)])

#print all the file names
for file, fullpath in filelist:
    if file not in masterlist:
        masterlist[file] = []

    with open(fullpath, 'r') as current_file:
        md_data = current_file.read().replace('\n',' ')

    # And analysis of the links in the current file
    doc = etree.fromstring(markdown.markdown(md_data))
    for link in doc.xpath('//a'):
        link_target = link.get('href')

        if os.path.isfile(f"{path}/{link_target}.md"):
            # print (link.text, link_target)
            masterlist[file].append(link_target)

print(len(masterlist))

for wpis in masterlist:
    print( wpis )
    for link in masterlist[wpis]:
        print( link , end=" ")
    print("\n---------------------------")
