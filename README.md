![uasos logo](https://raw.githubusercontent.com/Descent098/ezcv/master/.github/logo.png)


*A project on behalf of Fédération de recherche ONERA - ISAE SUPAERO - ENAC ([FONISEN](https://hal.science/FONISEN))*

UASOS Project - UAS Operator Simulator
=============

**Authors**: *[Pr. Raphaëlle N. ROY](https://pagespro.isae-supaero.fr/raphaelle-n-roy-211/) (ISAE CNE), [Pr. Anke BROCK](https://people.bordeaux.inria.fr/abrock/) (ENAC LII),* 

*[Marcel Francis HINSS](https://www.linkedin.com/in/marcel-francis-hinss-9097a5140/) (ISAE CNE), [PHAN Nhat Tien](https://www.linkedin.com/in/phanhatien/) (ENAC LII), [Vincenzo Maria VITALE](https://www.linkedin.com/in/enzomvitale/) (ISAE CNE)*

---
## TOC
- [UASOS Project - UAS Operator Simulator](#uasos-project---uas-operator-simulator)
  * [Scope of the project](#scope-of-the-project)
  * [Minimum and Recommended Requirements](#minimum-and-recommended-requirements)
      - [Recommended Flight Stick](#recommended-flight-stick)
  * [Python Modules used](#python-modules-used)
  * [Setup](#setup)
  * [Usage](#usage)
    + [UASOS](#uasos)
    + [Need personalized scripts? Use scriptgen4HPC](#need-personalized-scripts-use-scriptgen4hpc)
  * [FAQ](#faq)
  * [License](#license)

---
## Scope of the project

The project aims to reproduce functionally some of the tasks available on a UAS Ground Station and study the Test Subject mental fatigue subjected to this experiment.

The Repository includes:
* *UASOS*: the Experiment
* *scriptgen4HPC*: utility for generating new experimental scripts

---
## Minimum and Recommended Requirements
**Recommended Requirements**
We guarantee the full functionality of UASOS under the following requirements:

* CPU: Intel Core i7-8700 @3.20GHz
* GPU: NVidia Quadro P620 - 2GB GDDR5 - OpenGL 4.5
* RAM: 8 GB
* Storage: At least 2 GB
* 2 Identical Monitors - Resolution: 1920x1080 px
* A keyboard, Trackball for best experience
* Flight Stick: Logitech Extreme 3D Pro

**Minimum Requirements**

* CPU: at least a Quad-Core CPU
* GPU: at least 1GB GDDR4 - >OpenGL 2.0 for PsychoPy compatibility 
* RAM: at least 6 GB
* Storage: At least 512 MB
* 2 Monitors - Resolution: 1920x1080 px
* A keyboard, a pointing device and Flight Stick (See Recommended Flight Stick section)

#### Recommended Flight Stick
UASOS uses for listening the Flight Stick the library [PySticks](https://github.com/simondlevy/PySticks) from [Pr. Simon D. LEVY](https://simondlevy.academic.wlu.edu/) of Computer Science Department, Washington and Lee University (*Thank you Simon*, Devs. Note).

Following PySticks Release Notes, the compatible controllers are:

* PS3 controller
* PS4 controller
* Xbox 360 controller
* Logitech Extreme 3D Pro joystick
* Spektrum transmitter with WS1000 wireless simulator dongle
* FrSky Taranis TX9 RC transmitter with mini USB cable

I personally added the support for Controller Xbox One (Elite Series 2).

If you want to add a new controller, you can use the *joyreporter.py* given with PySticks repo by Pr. Simon D. LEVY:
1. Run on python console `joyreporter.py` available in `./UASOS/utilities/joyreporter`
2. Identify
   * The Name of the device (ex. `Controller (Xbox One For Windows)`)
   * the Axis that you want to use as Roll Axis (the only one that UASOS will use)
4. Update at `line 148` with a new line your controller as:
  `'<CONTROLLER_NAME>': _Xbox360((-1, <AXIS_ID_ROLL>, -3, 0), 0)`

**WARNING**: Different PCs may have different names for the same controller, but the axes are always the same.

In case you decide to run UASOS with same Controller but on different PC, just find the control name with the procedure you have up here.

---
## Python Modules used
This project runs under Python 3.8.10, as requirement for PsychoPy 2023.2.2.

At the startup, **UASOS** will check the presence of the following modules:

* lxml 4.9.3
* numpy 1.21.4
* opencv_contrib_python 4.8.0.74
* opencv_python 4.8.0.74
* Pillow 10.0.0
* psutil 5.8.0
* pygame 2.1.0
* pyglet 1.4.11
* pylsl 1.15.0
* PyQt5 5.15.9
* PyQt5_sip 12.12.2
* Pyro4 4.82 (obtained from `./UASOS/utilities/pyro4`)
* pytictoc 1.5.3
* scipy 1.7.2
* screeninfo 0.8.1
* serpent 1.41

Meanwhile **scriptgen4HPC** requires only:

* numpy 1.21.4

---
## Setup
**Before cloning our repo from GitHub**: please install PsychoPy >2023.2.2 from PsychoPy Project site ([here](https://www.psychopy.org/download.html))
and **install it for all users**.

Then, clone our repo from GitHub, set on your IDE (we used PyCharm Community Edition) the interpreter targeted to PsychoPy install dir 

and enjoy the experiment by running `main.py` on UASOS folder.

---
## Usage
### UASOS
For a Demo, you can simply start UASOS experiment directly and follow the experience.
Have fun! 😉

### Need personalized scripts? Use scriptgen4HPC
**scriptgen4HPC** 

---
## FAQ

---
## License
>You can check out the full license [here](https://github.com/Marcels-2-Neurons/Reaper/blob/main/LICENSE)

This project is licensed under the terms of the **MIT** license.
