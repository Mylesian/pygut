# pygut v4.2.0

## Documentation
Full documentation is coming soon here's an overview for now:
### ```pygut```
- ```Application```: Class to use/subclass that handles startup and event loop.
### ```pygut.base```
- ```Screen```: Class that holds the information about what should be drawn to the screen. Has a LayeredUpdates and LayeredDirty group of ```Element```s to handle different types of objects being drawn to the screen. Set ```Application.screen``` to show on screen.
- ```Element```: Base class that holds an object that is shown on screen. Extends ```pygame.sprite.Sprite``` and so has the fields ```image``` and ```rect``` to handle what is shown on screen and its position. Add a ```Collider``` to handle things like collisions with other ```Element```s. Can have ```action```s that correspond to different keyboard keys being pressed.
- ```Collider```: Base class that defines a hitbox for an ```Element```. Use ```Element.collides()``` to check for collision with another ```Collider```. Module ```pygut.collider``` has a default one (```RectCollider``` for rectangular ```Element```s), subclass this to add project-specific implementation. More subclasses to come in future updates (especially when pygame finishes their ```geometry``` module or I figure out better implementation for collision checking).

## Release notes for v4.2.0

- A hell of a lot of rewriting/updating ```action``` code but the important thing is that it works decently well now.
- Deleted a random return statement that appears to have no use. Hopefully nothing breaks.
- Realized my collision logic was completely wrong and so I am now in the process of rewriting it. CircleCollider is gone because it did not work and I don't know how to write it with the new architecture yet.
- Removed dependents and replaced them with methods to be called when a timer finishes counting down because why did I have them in the first place even.
- Changed ```Timer``` to not update when they've finished already (to prevent them from calling their finish method every frame).
- Added option for a ```Timer``` to call a method when ```Timer.reset()``` is called.
- Did a bit of refactoring of classes like ```Element``` and ```Collider``` to allow you to instantiate (or subclass, etc) them directly from calling ```pygut```
- Fixed ```Screen``` objects incorrectly trying to add an argument as a sprite.
- Fixed ```UIElements``` incorrectly setting their layer.
- Various other small bugfixes and changes that I can't remember now/are unimportant to mention.