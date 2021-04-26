# Computational Geometry
Application of geometry algorithms in simple tkinter driven GUI python3 script. 

Functionalities:
* Creating and removing points, lines and polygons
* Generating random points
* Generating convex hull for created points
* Generating visual representation of 2D (KD) tree for created points
* Finding functional equation for two selected points
* Specifying point location relating to line or polygon
* Rotating line in relation to point 
* Finding coordinates of two lines crossing point 
* Calculating triangle area 
   
### How does it work?
##### Usage
The menu on the left side gives standard functionality, mostly creating stuff. After you add some points to the canvas try to click them, you should see a menu with some options now, try them. Same applies to lines and polygons. **Beware**! If you create only one element of type and try to run method which requires two or more of them you will be forced to `restore scene` since there is no check in code for that kind of situation.  
##### Files
Main and the biggest - in terms of lines of code - is the `GUI.py` script. It contains whole logic of the application, starting with creating canvas and operating on it to calling geometry methods. Second in size and importance is `Operation.py` which holds a class of static methods which manipulate with given parameters, objects. Files `Point.py`, `Line.py` and `Polygon.py` holds classes with geometry objects with a couple of overridden build-in methods to simplify work with them. `KDTree.py` contains implementation of 2D tree with just enough methods to use it properly.
##### Action
GUI creates static sized window and lets user interact with the interface. After the user does any action its firstly calculated, then saved to GUI's variables and then painted on canvas.
There is a lot of methods doing simple one-usage operations such as adding listener to create the point, then actually creating them etc. The most important methods in GUI are `_paint` and `_restore`. First one clears canvas, gets data from variables and puts them back on screen, second one recreates user interface after the action is done. This model of application saves a lot of time with handling states of the buttons, making sure that screen has only right data etc. but may not be the most optimised. 
##### Some technicalities
Most of `Operations` is simple maths stuff so there is not much point to elaborate about them. Two things I consider worth to mention is:
* The convex hull is created using Graham's Scan algorithm - simple presentation available on [Wikipedia](https://en.wikipedia.org/wiki/Graham_scan)
* KD tree is set to be constantly two-dimensional, but it can be easily converted to be flexible, again explanation on [Wikipedia](https://en.wikipedia.org/wiki/K-d_tree#Construction)


@pause1 / Krzysztof Garbarz 26.04.2021 11:28