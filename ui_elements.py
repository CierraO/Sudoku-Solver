import pygame


class TextComment:
    def __init__(self, x, y, font, color, size):
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.size = size

    def draw(self, window, text):
        text_font = pygame.font.SysFont(self.font, self.size)
        text = text_font.render(text, True, self.color)
        window.blit(text, (self.x, self.y))


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, window):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check if mouse is over button and has clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            # if mouse left key is not pressed down set click to false
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # draws button on the screen
        window.blit(self.image, (self.rect.x, self.rect.y))

        return action


class TextField(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, limiter):
        super().__init__()
        self.color = (0, 0, 0)
        self.limiter = False
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.draw()

    def draw(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)  # renders the initial box
        self.image = pygame.Surface((max(self.width, t_surf.get_width() + 10), t_surf.get_height() + 10),
                                    pygame.SRCALPHA)  # makes it so the box expands with text
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        for event in event_list:
            # if mouse is clicked, make rectangle active
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.active:
                self.active = False

            if self.limiter == False:
                # if key is pressed down while active...
                if event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:  # make key inactive
                        self.active = False
                    elif event.key == pygame.K_BACKSPACE:   # move back one space
                        self.text = self.text[0:-1]
                    elif event.key == pygame.K_DELETE:   # move back one space
                        self.text = self.text[0:-1]
                    else:   # type whatever key is pressed
                        self.text += event.unicode
                self.draw()  # draw the key

            if self.limiter == True:
                # if key is pressed down while active...
                if event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:  # make key inactive
                        self.active = False
                    elif event.key == pygame.K_BACKSPACE:  # move back one space
                        self.text = self.text[0:-1]
                    elif event.key == pygame.K_DELETE:  # move back one space
                        self.text = self.text[0:-1]
                self.draw()  # draw the key



class OptionBox:
    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
                self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1
