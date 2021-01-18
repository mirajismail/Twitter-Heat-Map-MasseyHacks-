import ssl
from pygame import *
import os
from pymongo import MongoClient

# Setting MongoDB
password = os.getenv("mongoPass")
client = MongoClient("mongodb+srv://Armaan:" + password + "@cluster-1-dnqxb.mongodb.net/test?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
db = client.Twitter
hashtagCollection = db.Hashtags
# Getting coordinates
coordinateDict = hashtagCollection.find_one({})

coordinates = []
coordinates2 = []
coordinates3 = []

num = 1
while True:
    try:
        line = coordinateDict[str(num)]
        firstBracket = line.find('[')
        lastBracket = line.find(']')
        coordinates.append(line[firstBracket+1:lastBracket])
        num += 1
    except:
        break

for coord in coordinates:
    coordinates2.append(list(map(float,coord.split(", "))))

for coord in coordinates2:
    coordinates3.append((2*(coord[0]+180),2*(-1*(coord[1])+90)))


os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centering the screen
init()  # Starting up pygame
size = width, height = 720, 360
screen = display.set_mode(size)
map = transform.scale(image.load("map.png"),(720,360))
logo = transform.scale(image.load("logo.png"),(20,20))
running = True


while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
    screen.blit(map,(0,0))
    for coord in coordinates3:
        screen.blit(logo,(int(coord[0]-20),int(coord[1])))
        
    display.flip()
