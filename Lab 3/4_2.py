#Work Cited: 
#iStock:Hand Sign Illustration Set Vector stock illustration, https://www.istockphoto.com/vector/hand-sign-illustration-set-vector-gm1217338878-355301059
import pygame
import paho.mqtt.client as mqtt

from pygame.locals import (
    K_r,
    K_p,
    K_s ,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

B_Size = 90
DEFAULT_IMAGE_SIZE = (B_Size, B_Size)
def button(img, x, y):
    button = pygame.image.load(img)
    button = pygame.transform.scale(button, DEFAULT_IMAGE_SIZE)
    button = button.convert()
    buttonR = button.get_rect(topleft=(x, y))
    return button, buttonR

def text(f_size, str, x, y):
    font = pygame.font.Font('freesansbold.ttf', f_size)
    txt = font.render(str, True, white)
    txtR = txt.get_rect()
    txtR.center = (x,y)
    return txt, txtR

def on_connect(client, userdata, flags, rc):
    client.subscribe("p2_logi", 1) #add subscription for each player added, format: p#_s where # is the player number and s is the sever name

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

p2_O = " "
def on_message(client, userdata, message):
    global p2_O
    if(message.topic == "p2_logi"):
        p2_O = message.payload.decode()

if __name__ == "__main__":
    pygame.init()
    #parameters
    Scores = [0,0] #Scores[0] = player 1's score and so on
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    r_w = SCREEN_WIDTH//2 - 300
    r_h = SCREEN_WIDTH//2
    p_w = SCREEN_WIDTH//2 - 200
    p_h = SCREEN_WIDTH//2
    s_w = SCREEN_WIDTH//2 - 100
    s_h = SCREEN_WIDTH//2 
    A_w = SCREEN_WIDTH//2 + 100
    A_h = SCREEN_WIDTH//2 
    white = (255,255,255)
    black = (0,0,0)
    color_light = (170,170,170) 
    color_dark = (100,100,100)
    game_count = 0
    current_game = 0
    #screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Rock, Paper, Scissors')
    title, titleRect = text(32, 'Rock, Paper, Scissors!', SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250)
    Inst, InstR = text(32, "Instructions:", 170,120)
    Inst1,InstR1 = text(32, "Click on the image or", 250, 160)
    Inst2,InstR2 = text(32, "Enter the number", 220, 200)
    N1, N1R =  text(32, "r", r_w+40, r_h+120)
    N2, N2R =  text(32, "p", p_w+40, p_h+120)
    N3, N3R = text(32, "s", s_w+40, s_h+120)
    r, p, s= "Rock","Paper","Scissors"
    Operations = [r, p, s]

    #images
    rock, rockR = button("rock.jpg", r_w, r_h)
    scis, scisR = button("scis.jpg", s_w, s_h)
    paper, paperR = button("paper.jpg", p_w, p_h)

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message


    client.connect_async("mqtt.eclipseprojects.io")

    client.loop_start()
    running = True
    while(running):
        User_O = " "
        selecting= True
        while selecting and running:
            screen.fill((135, 206, 250))
            screen.blit(title,  titleRect)
            screen.blit(Inst, InstR)
            screen.blit(Inst1, InstR1)
            screen.blit(Inst2, InstR2)
            screen.blit(N1, N1R)
            screen.blit(N2, N2R)
            screen.blit(N3, N3R)
            mouse = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if(event.key == K_ESCAPE):
                        running = False
                    elif(event.key == K_r):
                        User_O = r
                        selecting = False
                    elif event.key == K_p:
                        User_O = p
                        selecting = False
                    elif event.key == K_s:
                        User_O = s
                        selecting = False
                elif event.type == QUIT:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    if r_w <= mouse[0] <= r_w + B_Size and r_h <= mouse[1] <= r_h +B_Size: 
                        User_O = r
                        selecting = False
                    elif p_w <= mouse[0] <= p_w + B_Size and p_h <= mouse[1] <= p_h +B_Size: 
                        User_O = p
                        selecting = False
                    elif s_w <= mouse[0] <= s_w + B_Size and s_h <= mouse[1] <= s_h +B_Size: 
                        User_O = s
                        selecting = False

            pygame.draw.rect(screen, black, (50,100,500,260), 2)
            screen.blit(rock, rockR)
            screen.blit(paper, paperR)
            screen.blit(scis, scisR)
            pygame.display.flip()
        
        client.publish("p1_logi", User_O,1) 

        wait, waitR = text(32, "Waiting for the input from player 2", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) 
        while(p2_O == " " and running):
            screen.fill((135, 206, 250))
            screen.blit(wait,waitR)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
            pygame.display.flip()

        if(p2_O == User_O):
            result, resultR = text(64, "Result: Tie", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) 
        else:
            if((User_O == r and p2_O  == s) or (User_O == p and p2_O  == r) or (User_O == s and p2_O  == p)):
                result, resultR = text(64, "Result: Player1 Win", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                Scores[0] = Scores[0] + 1
            else:
                result, resultR = text(64, "Result: Player2 Win", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                Scores[1] = Scores[1] + 1

        again = False
        ag, agR = text(32, "Again?", A_w+75, A_h+40)
        S, SR = text(32, "Scores", SCREEN_WIDTH//2 - 240, A_h+25)
        p1_s, p1_sR = text(32, "Player1: " + str(Scores[0]), SCREEN_WIDTH//2 - 220, A_h +75)
        p2_s, p2_sR  = text(32,"Player2: " + str(Scores[1]), SCREEN_WIDTH//2 - 220, A_h + 125)
        p1O, p1OR = text(32, "Player1 used: " + User_O, A_w+100, A_h + 120)
        p2O, p2OR   = text(32,"Player2 used: " + p2_O, A_w+100, A_h + 180) 
        p2_O = " " 
        while(running and (not again)):
            screen.fill((135, 206, 250))
            screen.blit(result,  resultR)
            screen.blit(S,  SR)
            screen.blit(p2_s,  p2_sR)
            screen.blit(p1_s,  p1_sR)
            screen.blit(p1O,   p1OR)
            screen.blit(p2O,  p2OR)
            screen.blit(ag,  agR)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    if A_w <= mouse[0] <= A_w + 150 and A_h <= mouse[1] <= A_h +80: 
                        again = True

            pygame.draw.rect(screen, black, ( SCREEN_WIDTH//2 - 300,A_h,250,180), 2)
            pygame.draw.rect(screen, black, (A_w,A_h,150,80), 2)
            pygame.display.flip()     
    client.loop_stop()
    client.disconnect() 
    pygame.quit()
    