from window import Window


class Game:
    def __init__(self):
        self.window = Window()
        self.running = True

    def run(self):
        while self.running:
            self.window.screen.fill((0, 0, 0))
            
            self.window.update()
        self.window.close()
