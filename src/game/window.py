import pygame


class Window:
    def __init__(self, fullscreen=True, width=800, height=600, events_handler={}):
        pygame.init()
        self.width = width
        self.height = height
        self.events_handler = events_handler
        self.screen = pygame.display.set_mode(
            (width, height),
            pygame.FULLSCREEN if fullscreen else 0
        )
        self.closed = False

    def poll_events(self):
        for event in pygame.event.get():
            if self.events_handler.get(event.type):
                self.events_handler[event.type](event)
            if event.type == pygame.QUIT:
                pygame.quit()
                self.closed = True

    def update(self):
        if self.closed:
            return
        self.poll_events()
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

    def close(self):
        pygame.quit()
        self.closed = True
