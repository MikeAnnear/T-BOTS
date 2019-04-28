import pygame, sys, pygame.mixer
from pygame.locals import *
import bluetooth as bt
from time import sleep
pygame.font.init()
#sansfont = pygame.font.Font('sans.ttf', 60)
basicfont = pygame.font.SysFont(None, 30)


#Look for all Bluetooth devices
#the computer knows about.

#Create an array with all the MAC
#addresses of the detected devices

oldkps, oldkp, oldtrim, oldgyro = str(0),str(0),str(0), str(0)

def parse():
    global oldkps
    global oldkp
    global oldtrim
    global oldgyro
    try:
        data = sock.recv(256).decode(encoding='utf-8')
        data = data.split('\x02')
        ministring = data[0]
        splitstr = ministring.split(',')
        oldkps, oldkp, oldtrim, oldgyro = splitstr[0], splitstr[1], splitstr[2], splitstr[3]
        return oldkps, oldkp, oldtrim, oldgyro
    except:
        return oldkps, oldkp, oldtrim, oldgyro

search = True
if search == True:
    print('Searching for devices...')
    print("")
    nearby_devices = bt.discover_devices()
    #Run through all the devices found and list their name
    num = 0
    
    for i in nearby_devices:
	    num+=1
	    print(num , ": " , bt.lookup_name( i ))
    print('Select your device by entering its coresponding number...')
    selection = input("> ") - 1
    print('You have selected - '+bt.lookup_name(nearby_devices[selection]))

    bd_addr = nearby_devices[selection]
else:
    bd_addr = '98:D3:32:11:4C:CF'
    print('connecting...')
error = 1
port = 1
while error:
    try:
        sock = bt.BluetoothSocket( bt.RFCOMM )
        sock.connect((bd_addr,1))
        sock.settimeout(5)
        error = 0
        print('connected to '+bd_addr)
    except:
        print('Trying again...')
        sock.close()
        error = 1
        sleep(2)
def send(sendstr):
    try:
        sock.send(sendstr.encode(encoding='utf-8'))
    except:
        sock.close()
        pygame.display.quit()
        sys.exit()


pygame.init()
clock = pygame.time.Clock()
size = width, height = 800, 500
screen=pygame.display.set_mode(size)

############   Load art work    #####################
joytop = pygame.image.load('images/joytopglow.png')
joybase = pygame.image.load('images/joybase.png')
minus = pygame.image.load('images/minus.png')
plus = pygame.image.load('images/plus.png')
pluslight = pygame.image.load('images/pluslight.png')
minuslight = pygame.image.load('images/minuslight.png')
gTrim = pygame.image.load('images/Trim.png')
gTrimlight = pygame.image.load('images/Trimlight.png')
button1,button2,button3,button4,button5,button6,button7 = 0,0,0,0,0,0,0
clock.tick()
data = []
x,y = 0,0
colour = (0,0,0)
textcolour = (255,255, 255)
mx,my = 0,0
mxnew, mynew = 250, 250


while True: # Continuous Pygame loop
    
    kps, kp, trim, gyrodata = parse()
    kpstext = basicfont.render('KPS '+kps, True, textcolour)
    kptext = basicfont.render('KP ' +kp, True, textcolour)
    trimtext = basicfont.render('TRIM '+trim, True, textcolour)
    mx,my = pygame.mouse.get_pos()
    p2x = mx
    p2y = my
    #print('x '+str(mx)+' y ' +str(my))
    if mx > 480 or mx < 20 or my > 480 or my < 20:
        mx,my = 250,250

    jx = int(((mx-250)*0.43)+200)
    jy = int(((250-my)*0.43)+200)
    if mxnew != mx or mynew != my:
        sendstring = chr(0X02)+str(jx)+str(jy)+chr(0X03)
        send(sendstring)          
        mxnew = mx
        mynew = my
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            kps, kp, trim, gyrodata = parse()
            if p2x > 0 and p2x < 500 and p2y > 0 and p2y < 500:
                mx, my = 250,250

            if p2x > 680 and p2x < 706 and p2y > 100 and p2y < 123:
                buttonstring = chr(0X02)+'200200B'+chr(0X03)
                send(buttonstring)
                button1 = 1
            if p2x > 680 and p2x < 706 and p2y > 130 and p2y < 153:
                buttonstring2 = chr(0X02)+'200200A'+chr(0X03)
                send(buttonstring2)
                button2 = 1

            if p2x > 680 and p2x < 706 and p2y > 230 and p2y < 253:
                buttonstring3 = chr(0X02)+'200200D'+chr(0X03)
                send(buttonstring3)
                button3 = 1
            if p2x > 680 and p2x < 706 and p2y > 260 and p2y < 283:
                buttonstring4 = chr(0X02)+'200200C'+chr(0X03)
                send(buttonstring4)
                button4 = 1

            if p2x > 580 and p2x < 706 and p2y > 360 and p2y < 383:
                buttonstring5 = chr(0X02)+'200200F'+chr(0X03)
                send(buttonstring5)
                button5 = 1
            if p2x > 680 and p2x < 706 and p2y > 390 and p2y < 413:
                buttonstring6 = chr(0X02)+'200200E'+chr(0X03)
                send(buttonstring6)
                button6 = 1
            if p2x > 680 and p2x < 706 and p2y > 430 and p2y < 460:
                buttonstring7 = chr(0X02)+'200200T'+chr(0X03)
                send(buttonstring7)
                button7 = 1

        elif event.type == MOUSEBUTTONUP:
            button1 = 0
            button2 = 0
            button3 = 0
            button4 = 0
            button5 = 0
            button6 = 0
            button7 = 0

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            sock.close()
            print('Your now disconnected.')
            pygame.display.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            sock.close()
            pygame.display.quit()
            print('Your now disconnected.')
            sys.exit()
    
        screen.fill(colour)
        screen.blit(joybase,(250-230,250-230))
        screen.blit(joytop,(mx-75,my-75))
        screen.blit(plus,(680,100))
        screen.blit(minus,(680,130))
        screen.blit(plus,(680,230))
        screen.blit(minus,(680,260))
        screen.blit(plus,(680,360))
        screen.blit(minus,(680,390))
        screen.blit(gTrim,(680,440))


        if button1:
            screen.blit(pluslight,(680-3,100-3))
        if button2:
            screen.blit(minuslight,(680-3,130-3))
        if button3:
            screen.blit(pluslight,(680-3,230-3))
        if button4:
            screen.blit(minuslight,(680-3,260-3))
        if button5:
            screen.blit(pluslight,(680-3,360-3))
        if button6:
            screen.blit(minuslight,(680-3,390-3))
        if button7:
            screen.blit(gTrimlight,(680-2,440-2))
        screen.blit(kpstext,(560,115))
        screen.blit(kptext,(560,245))
        screen.blit(trimtext,(560,375))
        screen.blit(joytop,(mx-75,my-75))
    pygame.display.flip()



