# pygut v4.1.0

## Documentation
Full documentation is coming soon here's an overview for now:
### ```pygut```
- ```Application```: Class to use/subclass that handles startup and event loop.
### ```pygut.base```
- ```Screen```: Class that holds the information about what should be drawn to the screen. Has a LayeredUpdates and LayeredDirty group of ```Element```s to handle different types of objects being drawn to the screen. Set ```Application.screen``` to show on screen.
- ```Element```: Base class that holds an object that is shown on screen. Extends ```pygame.sprite.Sprite``` and so has the fields ```image``` and ```rect``` to handle what is shown on screen and its position. Add a ```Collider``` to handle things like collisions with other ```Element```s. Can have ```action```s that correspond to different keyboard keys being pressed.
- ```Collider```: Base class that defines a hitbox for an ```Element```. Use ```Element.collides()``` to check for collision with another ```Collider```. Module ```pygut.collider``` has a few default ones, subclass this to add project-specific implementation.

## Release notes for v4.1.0

- Switched to pygame-ce for better support and higher python version compatibility. As a result of this a few syntax things changed in ```pygame.Application.__init__()```, though nobody cares because I'm the only person using this as of now.
- Removed ```pygame.WebApplication``` because pygbag (web deployment package) has an arduous process to get a module added to its list of available dependencies, so it is not being worked on. If you're building for web, don't use pygut.