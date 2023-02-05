#performance benchmark
from engine import game_engine_240123 as engine
import pygame, os, random, time, settings
debug_file = open("debug.txt", "w")
file_dir = os.getcwd()

#create window
w, h = settings.width, settings.height
window = engine.window("Performance Test", w, h, (0, 0, 128))

#variables
run = True
clock = pygame.time.Clock()
performance_mode = settings.performance_mode                #remove alpha transparencies
player_speed = 4                #set the speed of the player
Canvas = engine.Canvas          #get the canvas 
fps_stat = []           #keeps track of the fps
angle = 0           #sets the sprites angle position
no_of_sprites = settings.number_of_sprites          #how many sprites to be loaded in
no_of_text = settings.number_of_texts
direction = True            #true is right, left is false

#lists
display = []
ground = engine.properties_object("bg", f"{file_dir}/textures/ground.png", 0, 0, 3848, 3200, not performance_mode)
display += [ground]

#sprites
display_sprite = []
player = engine.properties_object("player", f"{file_dir}/textures/player.png", w/2, h/2, 64, 64, not performance_mode)
display_sprite += [player]

#foreground
foreground = []
#create sprites that rotate in place
for _ in range(no_of_sprites):
    x = random.randint(0, w-64)
    y = random.randint(0, h-64)
    sprite = engine.properties_object("sprite", f"{file_dir}/textures/player.png", x, y, 64, 64, not performance_mode)
    foreground += [sprite]

#text
text_foreground = []
for _ in range(no_of_text):
    x = random.randint(0, w-64)
    y = random.randint(0, h-64)
    text = engine.properties_text("text", "Hello, World!", "YELLOW", x, y, 30, False)
    text_foreground += [text]

def main():
    global fps_stat, text_foreground
    global angle, direction

    if player.x >= 3848:
        direction = not direction

    if player.x <= 0:
        direction = not direction
    
    if direction:
        if engine.object.right(player, player_speed, w - 64):
            Canvas.offsetX += player_speed
            engine.object.right(player, player_speed, w - 64)
            #move the text and the sprites
            for object in foreground:
                engine.object.right(object, player_speed, w - 64)

            for text in text_foreground:
                engine.object.right(text, player_speed, w - 64)

        if engine.object.down(player, player_speed, h - 64):
            Canvas.offsetY += player_speed
            engine.object.down(player, player_speed, h - 64)
            #move the text and the sprites
            for object in foreground:
                engine.object.down(object, player_speed, w - 64)

            for text in text_foreground:
                engine.object.down(text, player_speed, w - 64)

    else:
        if engine.object.left(player, player_speed, 64):
            Canvas.offsetX -= player_speed
            engine.object.left(player, player_speed, 64)
            #move the text and the sprites
            for object in foreground:
                engine.object.left(object, player_speed, 64)

            for text in text_foreground:
                engine.object.left(text, player_speed, 64)

        if engine.object.up(player, player_speed, 64):
            Canvas.offsetY -= player_speed
            engine.object.up(player, player_speed, 64)
            #move the text and the sprites
            for object in foreground:
                engine.object.up(object, player_speed, 64)

            for text in text_foreground:
                engine.object.up(text, player_speed, 64)

    #set the angle for the sprites
    if player.animationTime <= engine.frames:
        player.animationTime = engine.frames + 60
        for object in foreground:
            engine.object.setAngle(object, angle)
            angle += 90

    #keeps the data of how it performaed 
    if engine.frames > 30:
        fps_stat += [int(clock.get_fps())]
        engine.window.writeDebug_file(debug_file, display, display_sprite, foreground, text_foreground, clock)

    
start = time.time()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False

    main()
    engine.counter.update()
    engine.window.update(window, display, display_sprite, foreground, text_foreground, clock)
    clock.tick()

    #end game when the time passed is 30 seconds or greater
    if time.time() - start >= settings.duration:
        run = False

pygame.quit()
debug_file.close()

summary = open("summary.txt", "w")
average_fps = sum(fps_stat) / len(fps_stat)
print(f"Average FPS: {average_fps}")

#sort the list to find the lowest fps and the maximum fps
fps_stat.sort()
low_fps = fps_stat[0]
high_fps = fps_stat[len(fps_stat) - 1]
print(f"Lowest FPS: {low_fps}       Highest FPS: {high_fps}")

#find the lowest and highest deviation to the average fps
low_fps_devi = 100 - (low_fps / average_fps * 100)
high_fps_devi = (high_fps / average_fps * 100) - 100

if high_fps_devi > low_fps_devi:
    highest_devi = high_fps_devi
    lowest_devi = low_fps_devi
else:
    highest_devi = low_fps_devi
    lowest_devi = high_fps_devi

print(f"Lowest deviation: {int(lowest_devi)}%           Highest deviation: {int(highest_devi)}%")

#write to the file
summary.write(f"Average FPS: {average_fps}\n")
summary.write(f"Lowest FPS: {low_fps}       Highest FPS: {high_fps}\n")
summary.write(f"Lowest deviation: {int(lowest_devi)}%           Highest deviation: {int(highest_devi)}%\n")
summary.close()