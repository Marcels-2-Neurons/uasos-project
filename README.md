
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
    + [Need personalized scripts? Use scriptgen4HPC](#need-personalized-scripts--use-scriptgen4hpc)
  * [FAQ](#faq)
  * [License](#license)

---
## Scope of the project

The project aims to reproduce functionally some of the tasks available on a UAS Ground Station and study the Test Subject mental fatigue subjected to this experiment.

The Repository includes the Experiment *UASOS* and its utility for generating new experimental scripts called *scriptgen4HPC*.

---
## Minimum and Recommended Requirements
**Recommended Requirements**
We guarantee the full functionality of UASOS under the following requirements:

* CPU: Intel Core i7-8700 @3.20GHz
* GPU: NVidia Quadro P620 - 2GB GDDR5 - OpenGL 4.5
* RAM: 8 GB
* Storage: At least 2 GB
* A keyboard, Trackball for best experience
* Flight Stick: Logitech Extreme 3D Pro

**Minimum Requirements**

* CPU: at least a Quad-Core CPU
* GPU: at least 1GB GDDR4 - >OpenGL 2.0 for PsychoPy compatibility 
* RAM: at least 6 GB
* Storage: At least 512 MB
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

If you want to add a new controller, follow the procedure written in [PySticks readme](https://github.com/simondlevy/PySticks)
and update it on *pysticks.py* available in the UASOS folder.

---
## Python Modules used
At the startup, **UASOS** will check the presence of the following modules:

* lxml 4.9.3
* numpy 1.21.4
* opencv_contrib_python 4.8.0.74
* opencv_python 4.8.0.74
* Pillow 10.0.0
* psutil 5.8.0
* psychopy 2023.2.2
* pygame 2.1.0
* pyglet 1.4.11
* pylsl 1.15.0
* PyQt5 5.15.9
* PyQt5_sip 12.12.2
* Pyro4 4.82
* pytictoc 1.5.3
* scipy 1.7.2
* screeninfo 0.8.1
* serpent 1.41
* whichcraft 0.6.1

Meanwhile **scriptgen4HPC** requires only:

* numpy 1.21.4

---
## Setup

---
## Usage
### UASOS

### Need personalized scripts? Use scriptgen4HPC

---
## FAQ

---
## License
>You can check out the full license [here](https://github.com/Marcels-2-Neurons/Reaper/blob/main/LICENSE)

This project is licensed under the terms of the **MIT** license.
