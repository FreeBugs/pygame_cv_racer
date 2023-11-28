# PyGame ComputerVision racer

I have written this as an example of how to control a computer game using machine vision
and as a demo for my [pygame_gesture_kit](https://github.com/FreeBugs/pygame_gesture_kit)
package. This is, and probably will forever be, works in progress, so feel free to submit
something or make suggestions by creating an issue.

## How to
* Clone the repo:
```shell
git clone https://github.com/FreeBugs/pygame_cv_racer.git
```

* Install required packages:
```shell
python -m pip install -r requirements.txt
```

* Run the `main.py`
```shell
python main.py
```

* You probably have to give the python executable access to your camera and
restart the program afterwards.
* If the program is able to detect your hands, it will display a vector graphic of
the detected positions on screen - proper lighting will help.
* Use an imaginary steering wheel to switch lanes.
