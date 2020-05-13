"""
@author: Dominik
"""

#Version 1.1
#Goal: Create masking experiment to distill necessary elements from
#Goal for Version 1.2: Bug fixing / have it running

#Import modules
from psychopy.visual import Window, ImageStim, TextStim
from psychopy.core import wait
from psychopy.event import getKeys, clearEvents, waitKeys         #key inputs
from random import shuffle


'''Constants''' #variables that the end user does not interact with

DISPSIZE = (1280, 720)
grey= (0, 0, 0)         #define color pigment values for grey
win = Window(size = DISPSIZE, units = 'pix', fullscr = False, color = grey) #create window object
example_mask = ImageStim(win, 'round_mask.png') #initialize default/example pictures for mask
example_blank = ImageStim(win, 'blank.png') #blank screen
example_target = ImageStim(win, 'target.png') #target stimulus
example_foil =  ImageStim(win, 'foil.png') #and foil stimulus
log = open('exam_log.txt', 'w') #initialize the data log
welcome_txt = TextStim(win, text="", pos = (200, -250), height = 60) #initializing the welcome text placeholder
detec_instructions = TextStim(win, text="", pos = (200, -250), height = 60) #initialize placeholder for instruction text of the detection task
local_instructions = TextStim(win, text="", pos = (200, -250), height = 60) # ...of the localization task
disc_instructions = TextStim(win, text="", pos = (200, -250), height = 60) # ...of the discrimination task
fix = TextStim(win, text = "+", pos = (0, 0), height = 60) #fixation cross
center = (0, 0) #coordinates for the picture locations
left = (-250, 0)
right = (250, 0)
N_types = [] #to-be appended list of trial types (different numbers indicating different types of trials)

#other placeholders (filled later, depending on which tasks are chosen)
detec_txt = '' #Note to reviewer: If you know elegant ways of simultaneously creating different objects with the same initial values/properties, let me know
local_txt = ''
disc_txt = ''
disc_txt2 = ''
disc_txt3 = ''





'''input''' #variables whose values the end user will be able to enter, when this as a function

#Exposure details (i.e., details about the masking and target)
fixation_cross = True  #Should we show a fixation cross
mask_forw = False     #Will there be a forward mask?
mask_backw = False    # ...a backward mask?
mask_sandw = True     #...sandwich masking (i.e., both forward and backward mask)
mask_forw_durat = 0.1   #For how long is the forward mask shown? (in seconds)
mask_backw_durat = 0.1  #...the backward mask shown?
target_durat = 0.075       #the target stimulus shown?

#Task details
task_detec = False    #Should there be a detection task?
task_local = False    #localization task?
task_disc  = False    #discrimination task?
N_trials = 10         #how many stimulus trials?,              to be implemented: must be an integer
N_blanks = 10         #how many blank trials?,                 to be implemented: must be an integer
disc_cat_A = 'woman'  #name of category A in the discrimination task
disc_cat_B = 'man'    #name of category B in the discrimination task

#Task buttons
button_quit = 'q'              #button to press to quit experiment
button_detec_pres = 'z'        #button to press during detection task, if stimulus is present
button_detec_abs = 'm'         #button to press during detection task, if stimulus is absent / trial is a blank trial
button_local_left = 'left'    #button to press in localization task, if stimulus was shown left (default value: left arrow key)
button_local_right = 'right'  #button to press in localization task, if stimulus was shown right (default value: right arrow key)
button_disc_A = 'a'     #button to press in discrimination task, if stimulus is from category A
button_disc_B = 'l'     #button to press in discrimination task, if stimulus is from category B
button_welcome_quit = 'space' #button to quit the welcome screen with (default value: space)





'''Implementation (this part would be invisible to the end user)'''

log.write('trial_number\ttrial_type\t') #the trial number will be logged, no matter which task(s) (if any) is/are chosen

#the welcoming message and log is appended based on which tasks are chosen (if any)
if task_detec == True:
	detec_txt = 'Pay attention to whether or not a picture is shown. \n\ ' #this part would be added to the welcome message
	log.write('button_detection\t') #add elements to the first row of the log (i.e., of the header row), because this task takes place
if task_local == True:
	local_txt = 'Pay attention to whether the picture is shown left or right. \n\ '
	log.write('button_localization\t')
if task_disc == True:
	disc_txt = 'Pay attention to whether the picture is a'
	disc_txt2 = 'or a'
	disc_txt3 = '.'
	log.write('button_discrimination\t')

log.write('\n') #after all elements are added to the header row of the log, it goes to the next row (ready to note participants' responses)


#If no tasks are chosen, these "task_" objects will remain as initialized: ''
#Then, the welcome message will be appended with nothing (i.e., the content of empty objects).

welcome_txt.setText(f'Welcome to the experiment! \n\
					In this experiment, you will be shown pictures. \n\ \n\
					{detec_txt} {disc_cat_A} {disc_txt2} {disc_cat_B} {disc_txt3} \n\
					Once the experiment starts, you can between trials by pressing the {button_quit} button.\n\ \n\
					Procede to the experiment by pressing the {button_welcome_quit} button. Enjoy!')

# ^ in the third row, all appendices will be entered


'''Adjust task instructions, based on the selected buttons'''
detec_instructions.setText(f'Press {button_detec_pres}, if a picture was shown and {button_detec_abs} if no picture was shown.')
local_instructions.setText(f'Press {button_local_left}, if the picture was shown to the left and {button_local_right}, if the picture was shown to the right.')
disc_instructions.setText(f'Press {button_disc_A}, if the picture showed a(n) {disc_cat_A} and press {button_disc_A}, if the picture showed a(n) {disc_cat_B}.')

'''Sandwich masking (if selected)'''
if mask_sandw == True:            #Since sandwich masking means that forward + backwards masks are used
	mask_forw = True #so we set the values up this way
	mask_backw = True #in the final version, the input will instead be the choice of 3 default values: "forward, backward, sandwich"
	#so unlike in the current version, where sandwich is redundant, these T/F variables will only exist behind the scenes

'''Preparation for localization and discrimination task'''
complexity = 0 #So that each condition has an equal number of trials
#I need to find out whether we need 2 different trial types (left vs right, or category A or B)
#or 4 different trial types 2 (direction) X 2 (category)

if task_local == True:
	complexity += 1
if task_disc == True:
	complexity += 1

if complexity == 1:
	if N_trials % 2 != 0: #if we have one of these two tasks,
		N_trials += 1  #we only need to check whether the number of trials is even rather than odd
if complexity == 2:
	while N_trials % 4 != 0: #if it's both tasks,
		N_trials += 1 #the number of trials needs to be divisible by 4

i = 0

if complexity == 1:  #if there is one of these 2 tasks
	if task_local == True: #we check the type of task, if it's localization...
		while i < (N_trials/2):
			N_types.append(1) #half the trials will be on the left
			N_types.append(2) #the other on the right
	else: #if it's the discrimination task
		while i < (N_trials/2):
			N_types.append(5) #half the trials will show targets (in the middle of the screen)
			N_types.append(6) #the other half, will show foils (in the middle of the screen)
elif complexity == 2: #if it's both
	while i < (N_trials/4):
			N_types.append(1) #a quarter shows target on the left
			N_types.append(2) #another quarter shows target on the right
			N_types.append(3) #another: foils on the left
			N_types.append(4) #another: foils on the right
else: #if it's neither of these 2 tasks
	while i < N_trials:
		N_types.append(5) #on all trials, stimuli are presented in the middle of the screen

i = 0
while i < N_blanks:
	N_types.append(9) #then, we add the blank trials (if there are any)
shuffle(N_types) #And finally, randomize the order of trials


'''Actual implementation of the experiment'''
welcome_txt.draw()
win.flip()
waitKeys(keyList=[button_welcome_quit]) #display the welcome text, til people want to continue

clearEvents()	#makes sure that pressing the quit button before trial onset is ignored

for trial_number in len(N_types): #for every trial that is implemented
	quitkey = getKeys(keyList = [button_quit]) #check if the quit button has been pressed last trial
	if len(quitkey) > 0: #if that's the case,
		break #stop the experiment (or at least, the trials / for-loop)

	if	N_types[trial_number] < 5: #if the stimuli is supposed to be shown non-centrally (indicated by trial_type index)
		if	N_types[trial_number] % 2 ==1: #if they're supposed to be shown left (i.e., their index is an odd number)
			example_mask.setPos(left) #all pictures are shown left
			example_target.setPos(left)
			example_foil.setPos(left)
		else: #if they're supposed to be shown on the right
			example_mask.setPos(right) #all pictures are shown right
			example_target.setPos(right)
			example_foil.setPos(right)
	else: #else they're showen in the center
		example_mask.setPos(center) #which is true for trials with indices of >= 5
		example_target.setPos(center)
		example_foil.setPos(center)

	if fixation_cross == True: #implement a fixation cross, if requested
		fix.draw()
		win.flip()
		wait(0.1) #fixation cross is shown for 100ms before trial onset
		wait(0.008) #wait for half a frame to counteract refresh rate imprecisions

	#forward masking / (first half of the sandwich masking)
	if mask_forw == True:
		example_mask.draw()
		win.flip()
		wait((mask_forw_durat-0.008)) #display the mask for the requested duration (minus half a frame)

	#show stimulus
	wait(0.008) #Note to reviewer: I'm not quite sure I remember this half-frame adjustment correctly, feel free to correct me
	if	N_types[trial_number] == 9: #if no stimulus is supposed to be shown
		wait(0) #do nothing
	elif N_types[trial_number] in [1, 2, 5]: #if a target stimulus is shown (i.e., if it has index number 1, 2, or 5)
		example_target.draw()
	else: #if a foil stimulus is shown
		example_foil.draw()
	win.flip()
	wait((target_durat-0.008))

	#backward masking / (second half of the sandwich masking)
	if mask_backw == True:
		wait(0.008)
		example_mask.draw()
		win.flip()
		wait((mask_backw_durat-0.008)) #display the mask for the requested duration (minus half a frame)

	win.flip() #clear screen (either after backward mask or after target)

	log.write(f'{trial_number}\t') #log trial number, before we get to task-specific logging

	#Implement the tasks (insofar as requested)

	#Detection task
	if task_detec == True:
		detec_instructions.draw()
		key_detec = waitKeys(keyList=[button_detec_pres, button_detec_abs]) #get the relevant pressed key
		log.write('{key_detec}\t')		#log the key press

	#Localization task
	if task_local == True:
		local_instructions.draw()
		key_local = waitKeys(keyList=[button_local_left, button_local_right])
		log.write('{key_local}\t')

	#Discrimination task
	if task_disc == True:
		disc_instructions.draw()
		key_disc = waitKeys(keyList=[button_disc_A, button_disc_B])
		log.write('{key_disc}\t')

	log.write('\n') #after the tasks, go to the next row in the log (for the next trial)


win.close() #after the participant made it through all trials, shut down the screen
log.close() #and close the log
