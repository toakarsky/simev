# SimEv
very very very simple evolution simulator written in Python

# About
This is my pet project. Bored by my day-to-day office work as a programmer I'd like to finally create something that can enable me to express some sort of creativity. Thus I decided to create this small simulation of small creatures called Dains who compete for food between themself on their tiny 2D world of Adharas.

# How to run it
For now there isn't much there so to run you just have to install pygame(and Python v>=3.7)
```
pip install -r requirements.txt
```

Then just run it with
```
python ./simev.py
```

You can pause the world with ```SPACEBASE``` and while paused It shows some information about hovered object.

# Let's say this is a design description part of README
## Window
## Adharas
Class responsible for keeping track and updating everything in the world of Adharas.
### NaturalClock
NaturalClock is the class responsible for keeping track of current time on the Adharas. One day should take 16 ticks and night(procreation) should take 1 tick. 1 tick should be about 0.5s or 30frames for 60fps.
## Dian
Class representing a single creature living in the world of Adharas. A Dian.

# Attributions
Window icon by [flaticon](https://www.flaticon.com)

Font is [Cascadia Code](https://github.com/microsoft/cascadia-code) by Microsoft