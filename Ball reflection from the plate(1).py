import pygame
import math
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

#Function to draw dotted line
def draw_dotted_line(screen, color, start_pos, end_pos, dot_spacing):
    # Calculate the direction and length of the line
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    length = pygame.math.Vector2(dx, dy).length()

    # Calculate the number of dots needed
    num_dots = int(length / dot_spacing)

    # Calculate the spacing between each dot
    dot_spacing_x = dx / num_dots
    dot_spacing_y = dy / num_dots

    # Draw the dotted line
    for i in range(num_dots):
        dot_pos = (int(start_pos[0] + i * dot_spacing_x), int(start_pos[1] + i * dot_spacing_y))
        pygame.draw.circle(screen, color, dot_pos, 2)

# Set up the screen
screen_width = 1000
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Angle Line")

# Add text to the screen
font1 = pygame.font.Font(None, 60) # Set up the font
font2 = pygame.font.Font(None, 35) # Set up the font
text1= font1.render("Reflection of the ball from the metal Plate", True, (255, 255, 255)) # Create the text surface
text_rect = text1.get_rect(center=(450, 200)) # Position the text in the center

#------------------------------------------
# Set the color of the lines and dots
color = (255, 255, 120)

# Set the starting and ending points of the first line
start_pos1 = (50, 100)
end_pos1 = (590, 50)

# Set the starting and ending points of the second line
start_pos2 = (50, 100)
end_pos2 = (590, 300)

# Set the starting and ending points of the third line
start_pos3 = (50, 100)
end_pos3 = (590, 500)

# Set the distance between the dots
dot_spacing = 10
#-----------------------------------------------
# Set the reflecting plate properties
L_plate = 500
L_norm=200# normal line length
# Calculate the start and end points of the line
xL0 = 500  # Start from the left side of the screen
yL0= 700  #Start from the top of the screen
angle_degrees = 25 # Angle in degrees!!!!

angle_radians = math.radians(angle_degrees)  # Convert angle to radians
xL1= xL0 + int(math.cos(angle_radians) * L_plate)
yL1 = yL0 - int(math.sin(angle_radians) * L_plate)

# Set ball properties
ball_radius = 10
ball_color = (255, 120, 120)  # Red
ball_x = 50  # Left side of the screen
ball_y = 600
ball_speed_x =0.5
ball_speed_y = 0# Speed of the ball in pixels per frame

# Reflected direction of the ball
reflect_direction=Vector2(5*math.cos(2*angle_radians),-5*math.sin(2*angle_radians))
print('reflect_direction=',reflect_direction)

q=0
r=1
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Clear the screen
    screen.fill('blue')

    text2= font2.render('degrees', True, (255, 255, 255))
    screen.blit(text2, (900, 560))
   
    # Draw the line
    pygame.draw.line(screen, 'black', (xL0, yL0), (xL1, yL1), 20)

    #Draw the normal line
    if q==0:
        deltax=-(ball_y-yL0+ball_radius)/math.tan(angle_radians)
    deltay=deltax*math.tan(angle_radians)
    pygame.draw.line(screen,'white',(xL0+deltax,yL0-deltay-ball_radius),\
        (xL0+deltax+ball_radius-L_norm*math.sin(angle_radians),\
        yL0-deltay-L_norm*math.cos(angle_radians)),4)
    start_pos1=(xL0+deltax,yL0-deltay-ball_radius)
    end_pos1=(xL0+deltax+ball_radius-L_norm*math.sin(angle_radians),\
        yL0-deltay-L_norm*math.cos(angle_radians))

    # Draw the ball
    pygame.draw.circle(screen, 'yellow', (ball_x, ball_y), ball_radius)

    # Calculate the position vector of the ball
    ball_pos = pygame.Vector2(ball_x, ball_y)

    # Check for collision between the ball and the line
    collision_x=round(xL0-(ball_y-yL0+ball_radius)/math.tan(angle_radians))#??????????????????????
    if abs(ball_x-collision_x)<5:
        ball_speed_x = 0.1*reflect_direction.x
        ball_speed_y = 0.1*reflect_direction.y
        #print("Collision detected!")
        q=q+1
        if q==1:
            collision_x1=collision_x
    
    #Draw reference horizontal line
    draw_dotted_line(screen, color, (100,600), (950, 600), dot_spacing)

    #Draw Reflect Line
    reflect_direction=Vector2(5*math.cos(2*angle_radians),-5*math.sin(2*angle_radians))
    start_pos2=(xL0+deltax,yL0-deltay-ball_radius)
    end_pos2=(xL0+deltax+60*reflect_direction[0],yL0-deltay-ball_radius+60*reflect_direction[1])
    draw_dotted_line(screen, color, start_pos2, end_pos2, dot_spacing)
    
    if ball_x - ball_radius  < 0 or ball_x + ball_radius  > 1000:
        ball_x = 50  # Left side of the screen
        ball_y = 600
        ball_speed_x =0.5
        ball_speed_y = 0# Speed of the ball in pixels per frame
        angle_degrees =angle_degrees+5*r
        
        if angle_degrees >=65:
            r=-1
        if angle_degrees <=25:
            r=1
        angle_radians = math.radians(angle_degrees)  # Convert angle to radians
        xL1= xL0 + int(math.cos(angle_radians) * L_plate)
        yL1 = yL0 - int(math.sin(angle_radians) * L_plate)
        q=0

    if ball_y - ball_radius  < 0 or ball_y + ball_radius > 900:
        ball_x = 50  # Left side of the screen
        ball_y = 600
        ball_speed_x =0.5
        ball_speed_y = 0# Speed of the ball in pixels per frame
        angle_degrees =angle_degrees+5*r
        if angle_degrees >=65:
            r=-1
        if angle_degrees <=25:
            r=1
        angle_radians = math.radians(angle_degrees)  # Convert angle to radians
        xL1= xL0 + int(math.cos(angle_radians) * L_plate)
        yL1 = yL0 - int(math.sin(angle_radians) * L_plate)
        q=0
    screen.blit(text1, text_rect) # Draw the text on the screen
    
    angle_on_screen = font2.render(str(angle_degrees), True, (255, 255, 255))
    screen.blit(angle_on_screen, (860, 560))

# Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
