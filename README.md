# pygut v4.1.1

## Documentation
Full documentation is coming soon here's an overview for now:
### ```pygut```
- ```Application```: Class to use/subclass that handles startup and event loop.
### ```pygut.base```
- ```Screen```: Class that holds the information about what should be drawn to the screen. Has a LayeredUpdates and LayeredDirty group of ```Element```s to handle different types of objects being drawn to the screen. Set ```Application.screen``` to show on screen.
- ```Element```: Base class that holds an object that is shown on screen. Extends ```pygame.sprite.Sprite``` and so has the fields ```image``` and ```rect``` to handle what is shown on screen and its position. Add a ```Collider``` to handle things like collisions with other ```Element```s. Can have ```action```s that correspond to different keyboard keys being pressed.
- ```Collider```: Base class that defines a hitbox for an ```Element```. Use ```Element.collides()``` to check for collision with another ```Collider```. Module ```pygut.collider``` has a few default ones, subclass this to add project-specific implementation.

## Release notes for v4.1.1

- Hotfix cause I missed a couple references to non-declared objects when updating