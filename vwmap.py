import math
import markdown
import os, sys
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
        masterlist[file] = {'links': [], 'ext': [], 'name':file}

    with open(fullpath, 'r') as current_file:
        md_data = current_file.read().replace('\n',' ')

    # And analysis of the links in the current file
    doc = etree.fromstring(markdown.markdown(md_data))
    for link in doc.xpath('//a'):
        link_target = link.get('href')

        temp_name = f"{link_target}.md"
        if os.path.isfile(f"{path}/{temp_name}"):
            temp_name = temp_name.split("/")[-1]
            # print (temp_name)
            masterlist[file]['links'].append(temp_name)

# print(sys.argv)

target = None
if len(sys.argv) > 1:
    # Single target mode
    target = sys.argv[1].split("/")[-1]
    print(f"Looking for the {target}")
    if target in masterlist:
        print(f"The {target} found in the wiki!")
    else:
        target = None

# The pygame boilerplate 
WIDTH = 1000
HEIGHT = 1000
FPS = 60

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
R = 5

for i,element in enumerate(masterlist):
    x = margin + dX * (i % C)
    y = margin + int(i / C) * dY
    masterlist[element]['pos'] = (x,y)

    # And just using this loop to add the incoming links to list
    for el  in masterlist:
        if element in masterlist[el]['links']:
            masterlist[element]['ext'].append(el)
# For some quick print
for el in masterlist:
    # print(f"{el} from: {len(masterlist[el]['links'])} to: {len(masterlist[el]['ext'])}")
    pass

## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VimWikiLingGraph")
clock = pygame.time.Clock()     ## For syncing the FPS
font = pygame.font.Font(pygame.font.get_default_font(), 15)

## Game loop
running = True
t = 0
dt = 0.05;
while running:
    screen.fill(WHITE)
    t += dt

    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False
    mpos = pygame.mouse.get_pos()
    p1, p2, p3 = pygame.mouse.get_pressed()

    if target is None:
        for c in masterlist:
            if len(masterlist[c]['links']):
                for neigh in masterlist[c]['links']:
                    try:
                        pygame.draw.line(screen, (130,130,130), masterlist[c]['pos'], masterlist[neigh]['pos'], 1)
                    except:
                        pass

        for c in masterlist:
            thisR = (R + len(masterlist[c]['links']) / 2)
            pos = masterlist[c]['pos']
            clr = (130,30,130)

            # checking for the mouse click
            distance = math.sqrt((mpos[0]-pos[0])**2 + (mpos[1]-pos[1])**2)
            if p1 and (distance < thisR+5):
                masterlist[c]['pos'] = mpos
                clr = (130,230,130)

            pygame.draw.circle(screen, clr, pos, thisR, 0)
    else:
        c = target
        clr = (130,30,130)
        if len(masterlist[c]['links']):
            for neigh in masterlist[c]['links']:
                try:
                    pos = masterlist[neigh]['pos']
                    thisR = (R + len(masterlist[neigh]['links']) / 2)
                    pygame.draw.line(screen, (130,130,130), pos, masterlist[c]['pos'], 1)
                    pygame.draw.circle(screen, clr, pos, thisR, 0)
                    text_surface = font.render(masterlist[neigh]['name'], True, (0, 0, 0))
                    screen.blit(text_surface, dest=pos)
                except:
                    pass

        if len(masterlist[c]['ext']):
            for neigh in masterlist[c]['ext']:
                try:
                    pos = masterlist[neigh]['pos']
                    thisR = (R + len(masterlist[neigh]['links']) / 2)
                    pygame.draw.line(screen, (130,130,130), pos, masterlist[c]['pos'], 1)
                    pygame.draw.circle(screen, clr, pos, thisR, 0)
                    text_surface = font.render(masterlist[neigh]['name'], True, (0, 0, 0))
                    screen.blit(text_surface, dest=pos)
                except:
                    pass

        thisR = (R + len(masterlist[c]['links']) / 2)
        pos = masterlist[c]['pos']

        # checking for the mouse click
        distance = math.sqrt((mpos[0]-pos[0])**2 + (mpos[1]-pos[1])**2)
        if p1 and (distance < thisR+5):
            masterlist[c]['pos'] = mpos
            clr = (130,230,130)

        pygame.draw.circle(screen, clr, pos, thisR, 0)
        text_surface = font.render(masterlist[c]['name'], True, (0, 0, 0))
        screen.blit(text_surface, dest=pos)


    ## Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
