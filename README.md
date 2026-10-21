# pygut v3.2.0

## Release notes v3.2.0

- Refactored game loop to save on processing power when no screen is active
- Modified passed arguments to **kwargs in Screen's **kwargs param to also pass the lists of GameElements and UIElements
 - Added public lists of GameElements and UIElements to Screen class' fields