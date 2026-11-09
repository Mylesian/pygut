import pygame
from pygut.base import Screen, Timer

class Application:
    '''Basic application window. Shows an optional start_screen on startup.'''
    def __init__(self, screen_size: tuple[int, int], title: str = 'Pygame Window', start_screen: Screen | None = None, fps: int = 60, resizable: bool = True, maximize: bool = False, vsync: int = 0, handle_init: bool = True, handle_bg: bool = True):
        if handle_init:
            pygame.init()
        
        self.win = pygame.Window(title, screen_size, resizable=resizable,maximized=maximize)
        
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.handle_bg = handle_bg
        
        self.screen = start_screen
        self.timers: list[Timer] = []
        
        self.mouse_down = False
        self.mouse_just_down = False
       
    def update(self, **kwargs):
        '''Called once per frame. By default updates all of the entities in self.screen as well as count down all of its timers.
           mouse_buttons, m1_just_down, and keys_pressed are passed through kwargs. Override in a subclass to add extra functionality.'''
        if not self.screen is None:
            self.screen.update(**kwargs)
        
        for t in self.timers:
            t.countdown(kwargs['dt'])
    
    def _step(self, dt: float):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        if not self.screen is None:
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                if self.mouse_down: self.mouse_just_down = False
                else: self.mouse_just_down = True
                
                self.mouse_down = True
            else:
                self.mouse_down = False
                self.mouse_just_down = False
            
            self.update(dt=dt, mouse_buttons=mouse_buttons, m1_just_down=self.mouse_just_down, keys_pressed=pygame.key.get_pressed(),
                            game_elements=self.screen.game_elements, ui_elements=self.screen.ui_elements)
            updated = (self.screen.reg_elements.draw(self.win.get_surface(), self.screen.bg if self.handle_bg else None)
                     + self.screen.dirty_elements.draw(self.win.get_surface(), self.screen.bg if self.handle_bg else None))
            pygame.display.update(updated)
        else:
            self.win.get_surface().fill((0, 0, 0))
            pygame.display.flip()

    def run(self):
        '''Runs the game loop. Framerate is set to whatever was specified on object creation. Calls pygame.quit() when the loop ends.'''
        while self.running:
            dt = 1 / self.fps
            self._step(dt)
        
            self.clock.tick(self.fps)
            
        pygame.quit()