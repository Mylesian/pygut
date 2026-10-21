import pygame
from pygame._sdl2 import Window
import asyncio
from pygut.base import Screen, Timer

class Application:
    '''Basic application window. Shows an optional start_screen on startup.'''
    def __init__(self, screen_size: tuple[int, int], start_screen: Screen | None = None, fps: int = 30, flags: int = 0, maximize: bool = True, vsync: int = 0, handle_init: bool = True):
        if handle_init:
            pygame.init()
        
        if maximize:
            self.showing = pygame.display.set_mode(screen_size, flags | pygame.RESIZABLE, 0, 0, vsync)
            Window.from_display_module().maximize()
        else:
            self.showing = pygame.display.set_mode(screen_size, flags, 0, 0, vsync)
        
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.screen: Screen | None = start_screen
        self.timers: list[Timer] = []
        
        self.mouse_down = False
        self.mouse_just_down = False
       
    def update(self, dt: float, **kwargs):
        '''Called once per frame. By default updates all of the entities in self.screen as well as count down all of its timers.
           mouse_buttons, m1_just_down, and keys_pressed are passed through kwargs. Override in a subclass to add extra functionality.'''
        if not self.screen is None:
            self.screen.update(dt=dt)
        
        for t in self.timers:
            t.countdown(dt)
    
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
            
            if type(self.screen.bg) is pygame.color.Color:
                self.showing.fill(self.screen.bg, self.screen.get_rect(center=(self.showing.get_width() / 2,
                                                                                self.showing.get_height() / 2)))
            elif type(self.screen.bg) is pygame.Surface:
                self.showing.blit(self.screen.bg, (self.showing.get_width() / 2 - self.screen.get_width(),
                                                    self.showing.get_height() / 2 - self.screen.get_height()))
            
            self.update(dt, mouse_buttons=mouse_buttons, m1_just_down=self.mouse_just_down, keys_pressed=pygame.key.get_pressed(),
                            game_elements=self.screen.game_elements, ui_elements=self.screen.ui_elements)
            updated = self.screen.elements.draw(self.screen)
            pygame.display.update(updated)
        else:
            self.showing.fill((0, 0, 0))
            pygame.display.flip()

    def run(self):
        '''Runs the game loop. Framerate is set to whatever was specified on object creation. Calls pygame.quit() when the loop ends.'''
        while self.running:
            dt = 1 / self.fps
            self._step(dt)
        
            self.clock.tick(self.fps)
            
        pygame.quit()
        
class WebApplication(Application):
    '''async_run() function is asynchronously defined. Call from asyncio.run() to run a web build of the game.'''
    def __init__(self, screen_size: tuple[int, int], start_screen: Screen | None = None, fps: int = 30, flags: int = 0, vsync: int = 0, handle_init: bool = True):
        super().__init__(screen_size, start_screen, fps, flags, False, vsync, handle_init)
        
    async def async_run(self):
        while self.running:
            dt = 1 / self.fps
            self._step(dt)
        
            self.clock.tick(self.fps)
            await asyncio.sleep(0)
            
        pygame.quit()