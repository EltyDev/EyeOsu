import pygame


class Window:
    def __init__(self, fullscreen=True, width=800, height=600, events_handler=None):
        if events_handler is None:
            events_handler = {}
        self.width = width if not fullscreen else pygame.display.Info().current_w
        self.height = height if not fullscreen else pygame.display.Info().current_h
        self.events_handler = events_handler
        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        self.closed = False
        pygame.display.set_caption("EyeOsu")

    def poll_events(self):
        if self.closed:
            return
        for event in pygame.event.get():
            if self.events_handler.get(event.type):
                self.events_handler[event.type](event)
            if event.type == pygame.QUIT:
                self.close()

    def render(self, objects):
        if self.closed:
            return
        self.screen.fill((0, 0, 0))
        for obj in objects:
            obj.draw(self.screen)
        pygame.display.flip()

    def close(self):
        if self.closed:
            return
        pygame.quit()
        self.closed = True
