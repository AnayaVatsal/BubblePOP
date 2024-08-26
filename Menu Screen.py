import pygame

# initializing pygame window
pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Menu")

# images for button
play_img = pygame.image.load('play.png').convert_alpha()
quit_img = pygame.image.load('quit.png').convert_alpha()


class Button:  # button class to design buttons
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False

    def draw(self):  # draw buttons on window
        action = False
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):  # if mouse collides with the button
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:  # if the button is clicked
                self.click = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:  # reset condition
                self.click = False

        window.blit(self.image, (self.rect.x, self.rect.y))
        return action


# mapping buttons
play_button = Button(129, 20, play_img, 0.5)
quit_button = Button(129, 250, quit_img, 0.5)


# game loop
run = True
while run:
    window.fill((240, 200, 250))

    if play_button.draw():  # open the file with the game code
        code_file = open('Game Code.py', 'r')
        game = code_file.read()
        exec(game)

    if quit_button.draw():  # quit game condition
        run = False

    for event in pygame.event.get():  # event handler
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()  # updates after every loop
pygame.quit()