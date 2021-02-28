import math
import markdown
import random
import os
from lxml import etree
import pygame

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

        temp_name = f"{link_target}.md"
        if os.path.isfile(f"{path}/{temp_name}"):
            masterlist[file].append(temp_name)

# for wpis in masterlist:
    # print( wpis )
    # for link in masterlist[wpis]:
        # print( link , end=" ")
    # print("\n---------------------------")

print (masterlist)

# The pygame boilerplate 
WIDTH = 640
HEIGHT = 480
FPS = 30

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Preparing the objects for the circles
margin = 50
total = len(masterlist)
C = 6
dX = (WIDTH - 2*margin) / (C - 1)
dY = (HEIGHT - 2*margin) / math.ceil(total / C)
R = 10

circles = {}
for i,element in enumerate(masterlist):
    print(i)
    x = margin + dX * (i % C)
    y = margin + int(i / C) * dY
    circles[element] = (x,y)


## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VimWikiLingGraph")
clock = pygame.time.Clock()     ## For syncing the FPS



## Game loop
running = True
while running:

    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False
    ########################
    for c in circles:
        if len(masterlist[c]):
            for neigh in masterlist[c]:
                try:
                    pygame.draw.line(screen, (130,130,130), circles[c], circles[neigh], 1)
                except:
                    pass

    for c in circles:
        pygame.draw.circle(screen, (130,30,130), circles[c], R, 0)

    ########################
    ## Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()

