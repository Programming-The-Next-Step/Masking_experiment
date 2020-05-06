## Goal


**Brief**

I want to create a Python package that makes implementing visual masking studies easy. In a visual masking study, a stimulus ("target") is shown to the participant and another, the "mask" is presented to make the "target" harder to see.

There are several standard techniques of masking stimuli (i.e., of using stimuli to make other stimuli harder to see) and several standard tasks that are implemented with such hard-to-see ("masked") stimuli. After downloading my package, I want people to be able to implement these tasks with simple lines of code (*for a hypothetical example, see the end of this document*).


**Long form / All details**

Specifically, I want it to be able to implement the following functions:

* The three standard masking techniques:  
  + Forward masking (mask before target stimulus)   
  + Backward masking (mask after) 
  + Sandwich masking (mask before and after)
* The following standard masking tasks:
  + Simple localization ("Was the target presented left or right?")
  + Harder localization (left, right, top, bottom, top-left, bottom-left, …)
  + Discrimination task ("Was the target of category A or B?")
  + Detection task ("Was there a target or was there nothing?")
* Blank trials (i.e., trials with no target stimuli, but an empty screen)
* Sensical default values (e.g., presenting target and mask at the middle of the screen, unless otherwise specified)
* Multiple masks (e.g., two backwards masks presented in a row)
* Random masks (i.e., input multiple mask stimuli and at each trial draw one or more of them)
* Foil stimuli (i.e., show non-target stimuli)
* Specify a fixation cross/dot/custom picture
* Random presentation times (e.g., being able to implement a distribution of presentation times, rather than a number)
* Timed responses (e.g., participants have only 2 seconds to respond to the task)


## Implementation

**What to implement first / how to start**

I will first create standard masking experiments on Python (i.e., forward, backward, and sandwich) and then work backwards, distilling which elements are important and need to be accessible/changeable to an end user. Thereby, I plan to determine the necessary Python objects and object properties that my package must include (e.g., what must be attributes of objects of the to-be-build "Mask" class).


**What to cut, if necessary**

My "long form"" section mentions my planned features in order of importance. All features, bar the 3 masking types, blank trials and standard masking tasks can be cut for this package to still fulfill its purpose (i.e., simplifying the creation of standard masking experiments). Of the 4 standard masking tasks, the harder localization task can also be cut (it is the least frequetnly utilized of the 4 tasks).


**What to add, if possible**

I have several ideas for how to improve this package, further, but am not sure whether they are realistic to implement (be it due to time or Python constraints).

*Details* 

* Help function entries (“?XYZ” entries for all functions and function arguments of my code)
* A function for user-friendly entry:
Instead of the user having to write long code, the function asks consecutive (branching) questions in the console and arrives at code necessary for implementing their desired experiment

* A rudimentary patching function (checks whether the current patch number is the highest available on GitHub and if not, asks in the console whether it should patch)
* Support for custom tasks/instructions
* A graphical user interface (determine the sequence of stimuli and masks with mouse drag-and-drop and save/output code for the final choice)
* Saving of rudimentary design figures as picture files outside of Python (e.g., output like https://www.frontiersin.org/files/Articles/25452/fpsyg-03-00129-r3/image_m/fpsyg-03-00129-g005.jpg )
* Loading in of stimuli from the internet (i.e., input the link to a picture to use it as a target/mask)

## Code

**Packages**


I will use Python functions from several PsychoPy (sub-)libraries (specifically, psychopy.visual, .core and .event). I will also need mathematical packages like numpy and random.
 

&nbsp;
 
**Functions and objects to be created**

*Object: Mask*

An object with which one specifies a mask stimulus's properties (e.g., how large it is, how long it is shown for).

&nbsp;

*Object: Target*

An object with which one specifies a target stimulus's properties.

&nbsp;

*Object: Task*

An object to specify details about the task that has to be performed after the masked stimulus is presented (e.g., which task has to be performed, what responses are recorded, whether there is a timelimit, etc.).

&nbsp;

*Function: runMasking*

An omnibus function to feed the above-mentioned objects to. It determines the type of experiment (e.g., backward masking) that is performed.

&nbsp;


*(optional)*
*Function: createTask*

If I have the time to get to this, this function would allow users to program their own tasks (i.e., what is done after the stimulus presentation). These could then be used as input to the *Task* object (which usually runs on default values for the four standard task types). 

&nbsp;

&nbsp;

&nbsp;

`Hypothetical code:`
```
#create two Python objects for the mask stimuli (which are shown in the experiment for 100ms)

m_1 = Mask(size = (720, 360), file = "circle_mask.jpg", duration = 100)  
m_2 = Mask(size = (720, 360), file = "triangle_mask.jpg", duration = 100)


#create a Python object for the target stimulus (shown for 17ms)

t_1 = Target(size = (720, 360), file = "Mole.jpg", duration = 17) 


#create a Python object for the task that participants have to perform

d_1 = Task(type = "Detection", yesKey = "z", noKey = "m", customText = "Press z, if you saw a mole; press m, if you did not see a mole", timeLimit = false)


#run the experiment with one (long) Python function

runMasking(nTrials = 200, maskType = "Forward", target = t_1, mask = (m_1, m_2), randomMasks = true, task = d_1, blank = 0.4)
```

Which would result in 200 trials of a forward-masking experiment with: 

* targets shown for 17ms 
* two different masks (from which one is randomly drawn per trial) shown for 100ms
* blank trials (trials on which nothing is shown instead of the target) in 40% of trials 
* and a detection task at the end of each trial (asking participants, whether or not a target was shown) 