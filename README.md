![uasos logo](https://media.githubusercontent.com/media/Marcels-2-Neurons/uasos-project/main/UASOS/imgs/UASOS%20Banner.png)


*A project on behalf of Fédération de recherche ONERA - ISAE SUPAERO - ENAC ([FONISEN](https://hal.science/FONISEN))*

UASOS Project - UAS Operator Simulator
=============

**Authors**: *[Pr. Raphaëlle N. ROY](https://pagespro.isae-supaero.fr/raphaelle-n-roy-211/) (ISAE CNE), [Pr. Anke BROCK](https://people.bordeaux.inria.fr/abrock/) (ENAC LII),* 

*[Marcel Francis HINSS](https://www.linkedin.com/in/marcel-francis-hinss-9097a5140/) (ISAE CNE), [PHAN Nhat Tien](https://www.linkedin.com/in/phanhatien/) (ENAC LII), [Vincenzo Maria VITALE](https://www.linkedin.com/in/enzomvitale/) (ISAE CNE)*

---
## TOC
- [Scope of the project](#scope-of-the-project)
- [Minimum and Recommended Requirements](#minimum-and-recommended-requirements)
    + [Recommended Requirements](#recommended-requirements)
    + [Minimum Requirements](#minimum-requirements)
    + [You have another Flight Stick?](#you-have-another-flight-stick)
- [Python Modules used](#python-modules-used)
- [Setup](#setup)
- [Usage](#usage)
  * [UASOS](#uasos)
    + [List of Hotkeys](#list-of-hotkeys)
  * [Need personalized scripts? Use scriptgen4HPC](#need-personalized-scripts-use-scriptgen4hpc)
    + [Prerequirements: If you use an Home PC](#prerequirements-if-you-use-an-home-pc)
    + [Prerequirements: If you use an HPC Node](#prerequirements-if-you-use-an-hpc-node)
    + [Parameters to change and run](#parameters-to-change-and-run)
- [FAQ](#faq)
- [License](#license)

---
## Scope of the project

The project aims to reproduce functionally some of the tasks available on a UAS Ground Station and study the Test Subject mental fatigue subjected to this experiment.

The Repository includes:
* *UASOS*: the Experiment
* *scriptgen4HPC*: utility for generating new experimental scripts

---
## Minimum and Recommended Requirements
#### Recommended Requirements

We guarantee the full functionality of UASOS under the following requirements:

* CPU: Intel Core i7-8700 @3.20GHz
* GPU: NVidia Quadro P620 - 2GB GDDR5 - OpenGL 4.5
* RAM: 8 GB
* Storage: At least 2 GB
* 2 Identical Monitors - Resolution: 1920x1080 px
* A keyboard, Trackball for best experience
* Flight Stick: Logitech Extreme 3D Pro
* Any sensor compatible with LSL can be used

#### Minimum Requirements

* CPU: at least a Quad-Core CPU
* GPU: at least 1GB GDDR4 - >OpenGL 2.0 for PsychoPy compatibility 
* RAM: at least 6 GB
* Storage: At least 512 MB
* 2 Monitors - Resolution should be equal between the screens
* A keyboard, a pointing device and Flight Stick (See You have another Flight Stick? section)
* Any sensor compatible with LSL can be used

#### You have another Flight Stick?
UASOS uses for listening the Flight Stick the library [PySticks](https://github.com/simondlevy/PySticks) from [Pr. Simon D. LEVY](https://simondlevy.academic.wlu.edu/) of Computer Science Department, Washington and Lee University. (*Thank you Simon*, Devs. Note)

Following PySticks Release Notes, the compatible controllers are:

* PS3 controller
* PS4 controller
* Xbox 360 controller
* Logitech Extreme 3D Pro joystick
* Spektrum transmitter with WS1000 wireless simulator dongle
* FrSky Taranis TX9 RC transmitter with mini USB cable

The support for Controller Xbox One (Elite Series 2) has been added.

If you want to add a new controller, you can use the *joyreporter.py* given with PySticks repo by Pr. Simon D. LEVY:
1. Run on python console `joyreporter.py` available in `./UASOS/utilities/joyreporter`
2. Identify
   * The Name of the device (ex. `Controller (Xbox One For Windows)`)
   * the Axis that you want to use as Roll Axis (you can identify it by checking the console: it changes between [-1,+1], it will be the only one that UASOS will use)
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
* Pyro4 4.82 (.exes availables in `./UASOS/utilities/pyro4`)
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

Then, clone our repo from GitHub **USING ONLY Github Desktop App or Git from Command Line ([see details in FAQ](#faq))**, 

set on your IDE (we used PyCharm Community Edition) the interpreter targeted to PsychoPy install dir 

and enjoy the experiment by running `main.py` on UASOS folder.

---
## Usage
### UASOS
For a Demo, you can simply start UASOS experiment directly and follow the experience.
Have fun! 😉

#### List of Hotkeys
- Escape: Force Close of the Experiment
- S: advance through Tutorial slides and phases / if during experimental phase it commands the Pause

**NOTE: At the RESTING STATE slide, please press S to advance.** 

### Need personalized scripts? Use scriptgen4HPC
---
**scriptgen4HPC** can work both on a house PC and on HPC Node.

#### Prerequirements: If you use an Home PC
---
In order to avoid stutters when using your PC, maintain one logical core available for essential processes:

Modify in `main.py` at `line 26`: `num_threads = mp.cpu_count() - 1`

#### Prerequirements: If you use an HPC Node
---
No modifications necessary, just go to [Parameters to change](#parameters-to-change)

Remember to build your own Slurm file to organize your simulation.

#### Parameters to change and run
---
From `line 37` to `line 46`
```python
max_size_dset = 1000  # indicative, pc needs to do a round number of scripts
max_time = 167  # Max time allowable to run in hours, useful to cut before HPC cuts the allocation time
# Related to the script_dset.csv gen
phase_gen = 'MAIN'  # choose between 'MAIN', 'SRC_TRAIN', 'NAVI_TRAIN'
exp_time_main = 2*60*min2ms # Modify just the first integer if you want to modify the hours
exp_time_train = 3*min2ms # Modify just the first integer if you want to modify the minutes
it_time = 7000 # Mean iteration time in ms
jitter = 1000 # Jitter range in ms [-jitter,+jitter]
treshold = 0.03  # Default < 0.03 for convergence in 2hrs 7 (+/-1) sec [DO NOT GO < 0.02]
treshold_train = 0.5  # Stay large, it's just training [DO NOT GO < 0.15]
```
And then you are ready to run.

You will obtain your new scripts on `./scriptgen4HPC/final`.

Based on the `phase_gen` parameter you have chosen, the final csv file will have the proper name for substitute the current dataset.

Overwrite them on `./UASOS/scripts` and remember to update with the parameters you have chosen in `settings.py` from `line 23` to `line 28`.

---
## FAQ
1. When I launch UASOS, some errors shows up saying that some files are missing/unreadable. What I need to do?

   All the `.png` and `.mat` files are uploaded on this repository using the GLF (Git Large File) system.

   Several user noticed that downloading the repository directly as `.zip` from this page retrieves a corrupted copy of UASOS due to Github large filesize limitation.

   Please, **Clone this repository using the Github Desktop or Git from Command Line, BUT DO NOT DOWNLOAD DIRECTLY THE REPOSITORY!**

   We are deeply sorry for this inconvenience!

3. When I launch UASOS, after the first Window the execution crashes. The Command Outlet says: "Please, install pyro4==4.82 through pip", but I already have it. What I need to do?

   It falls down 2 potential cases:

   * **The interpreter does not have the Pyro4 executables in `./Scripts` folder**: just copy and paste the content within `./UASOS/utilities/pyro4` to your interpreter folder `<Interpreter>/Scripts`.
   
   * **The intepreter you set up for UASOS is not the declared one in the `PATH` environment variable**: use the interpreter declared in your `PATH` environment variable or declare your current interpreter in the environment variable `PATH`.

   Performing one of these 2 should resolve most of the issues.

4. When I launch UASOS, after the first Window the execution crashes. The Command Outlet express `[WinError10061]`. What I need to do?

   Unfortunately, this error happens when the interpreter tries to launch pyro4 NameServer without success.

   Try to set your interpreter as the one declared within the environment variable `PATH` and reinstall Pyro4.

5. When I launch UASOS, I rapidly have a crash slightly after the Language selection or when I ask to restart from the ID folder:

   That may occur during the Navigation Task Window is not fully charged. We are sorry for that and we are still working on finding the best solution to avoid this funny behavior.

   Our suggestion is to wait a little more (about 7 sec) from the opening of all instances before entering any data.

   Generally, the complete startup of the program takes up to 20 sec before starting entering your data.

---
## License
>You can check out the full license [here](https://anonymous.4open.science/r/uasos-project/LICENSE)

This project is licensed under the terms of the **MIT** license.
