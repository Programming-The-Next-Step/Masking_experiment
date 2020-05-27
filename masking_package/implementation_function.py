"""
@author: Dom
"""
#Version 1.3
#Goal: Split code into multiple files (one with input, others with hidden code)
#Goal for Version 1.5: Have the package run (successfully use functions across files)

#Import modules
from psychopy.visual import Window, ImageStim, TextStim
from psychopy.core import wait
from psychopy.event import getKeys, clearEvents, waitKeys
from random import shuffle


'''input''' #variables whose values the end user will be able to enter

#Exposure details (i.e., details about the masking and target)
fixation_cross = True  #Should we show a fixation cross
mask_type = "Sandw"
#Forw for forward masking (mask before target), Backw for backward masking
#(mask after target), Sandw for sandwich masking (mask before and after target)
mask_forw_durat = 0.1   #For how long is the forward mask shown? (in seconds)
mask_backw_durat = 0.1  #...the backward mask shown?
target_durat = 0.05       #the target stimulus shown?

#Task details
task_detec = True    #Should there be a detection task?
task_local = True    #localization task?
task_disc  = True    #discrimination task?
detec_skip = True    #if participants say they don't detect a stimulus, are the other tasks skipped?
N_trials = 9         #how many stimulus trials?,              to be implemented: must be an integer
N_blanks = 2         #how many blank trials?,                 to be implemented: must be an integer
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
button_welcome_quit = 'space' #button to quit the welcome screen with (default value = space)


'''Implementation (this part would be invisible to the end user)'''

log.write('trial_number\ttrial_type\t') #the trial number will be logged, no matter which task(s) (if any) is/are chosen

#the welcoming message and log is appended based on which tasks are chosen (if any)
if task_detec: #i.e., "if task_detec == True: "
	detec_txt = '\nPay attention to whether or not a picture is shown. ' #this part would be added to the welcome message
	log.write('button_detection\t') #add elements to the first row of the log (i.e., of the header row), because this task takes place
if task_local:
	local_txt = '\nPay attention to whether the picture is shown left or right. '
	log.write('button_localization\t')
if task_disc:
	disc_txt = f'\nPay attention to whether the picture shows a(n) {disc_cat_A} or a(n) {disc_cat_B}. '
	log.write('button_discrimination\t')

log.write('\n') #after all elements are added to the header row of the log, it goes to the next row (ready to note participants' responses)


#If no tasks are chosen, these "task_" objects will remain as initialized: ''
#Then, the welcome message will be appended with nothing (i.e., the content of empty objects).

welcome_txt.setText(f'Welcome to the experiment! \n \nIn this experiment, you will be shown '
					f'pictures.{detec_txt}{local_txt}{disc_txt} \nOnce the experiment starts, you can quit anytime'
					f' by pressing the {button_quit} button. \n\nProcede to the'
					f' experiment by pressing the "{button_welcome_quit}" button. Enjoy!')

# ^ in the second row, all appendices will be entered


'''Adjust task instructions, based on the selected buttons'''
detec_instructions.setText(f'Press "{button_detec_pres}", if a picture was shown and "{button_detec_abs}", if no picture was shown.')
local_instructions.setText(f'Press "{button_local_left}", if the picture was shown to the left and "{button_local_right}", if the picture was shown to the right.')
disc_instructions.setText(f'Press "{button_disc_A}", if the picture showed a(n) {disc_cat_A} and press "{button_disc_B}", if the picture showed a(n) {disc_cat_B}.')


determine_masking_type()

'''Create unique trial sequence'''
create_trial_sequence(N_trials, N_blanks, task_local, task_disc) #see background functions


'''Actual implementation of the experiment'''
welcome_txt.draw()
win.flip()
waitKeys(keyList = [button_welcome_quit]) #display the welcome text, til people want to continue

clearEvents()	#makes sure that pressing the quit button before trial onset is ignored

for trial_number in range(len(N_types)): #for every trial that is implemented
	quitkey = getKeys(keyList = [button_quit]) #check if the quit button has been pressed last trial
	if len(quitkey) > 0: #if that's the case,
		log.write('Experiment quit')
		break #stop the experiment (or at least, the trials / for-loop)

	if	N_types[trial_number] < 5: #if the stimuli is supposed to be shown non-centrally (indicated by trial_type index)
		if	N_types[trial_number] % 2 == 1: #if they're supposed to be shown left (i.e., their index is an odd number)
		    #all pictures are shown left
			example_target.setPos(left)
			example_foil.setPos(left)
		else: #if they're supposed to be shown on the right
			#all pictures are shown right
			example_target.setPos(right)
			example_foil.setPos(right)
	else: #else they're showen in the center
		#which is true for trials with indices of >= 5
		example_target.setPos(center)
		example_foil.setPos(center)

	if fixation_cross: #implement a fixation cross, if requested
		fix.draw()
		win.flip()
		wait(0.1) #fixation cross is shown for 100ms before trial onset
		wait(0.008) #wait for half a frame to counteract refresh rate imprecisions

	#forward masking / (first half of the sandwich masking)
	if mask_forw:
		if task_local: #if people have to determine whether the target was left or right
			#the mask has to be drawn on both sides
			#so that it doesn't give away the target location
			draw_stim(mask, example_mask, right)
			draw_stim(mask, example_mask, left)
		else:
			draw_stim(mask, example_mask, center)
		win.flip()
		wait((mask_forw_durat - 0.008)) #display the mask for the requested duration (minus half a frame)

	#show stimulus
	wait(0.008) #Note to reviewer: I'm not quite sure I remember this half-frame adjustment correctly, feel free to correct me
	if	N_types[trial_number] == 9: #if no stimulus is supposed to be shown
		pass
	elif N_types[trial_number] in [1, 2, 5]: #if a target stimulus is shown (i.e., if it has index number 1, 2, or 5)
		example_target.draw()
	else: #if a foil stimulus is shown
		example_foil.draw()
	win.flip()
	wait((target_durat - 0.008))

	#backward masking / (second half of the sandwich masking)
	if mask_backw:
		if task_local: #if people have to determine whether the target was left or right
			wait(0.008)
			#the mask must be drawn both left and right
			#so that it doesn't give away the target location
			draw_stim(mask, example_mask, right)
			draw_stim(mask, example_mask, left)
		else:
			wait(0.008)
			draw_stim(mask, example_mask, center)
		win.flip()
		wait((mask_backw_durat - 0.008)) #display the mask for the requested duration (minus half a frame)

	win.flip() #clear screen (either after backward mask or after target)

	log.write(f'{(trial_number+1)}\t') #log trial number, before we get to task-specific logging

	#Implement the tasks (insofar as requested)

	#Detection task
	if task_detec:
		detec_instructions.draw()
		win.flip()
		key_detec = waitKeys(keyList = [button_detec_pres, button_detec_abs, button_quit]) #get the relevant pressed key
		if key_detec[-1] == button_quit: #if they pressed the quit button
			log.write('Experiment quit')
			break #quit
		log_detec = key_detec[-1]
		log.write(f'{key_detec}\t')		#log the key press

	#Localization task
	skip = False #in general we don't skip tasks, unless:
	if detec_skip: #if we are instructed to skip trials on which people say stimuli were absent
		if task_detec: #and if a detection task actually took place
			if key_detec[-1] == button_detec_abs: #and if the participant deemed the stimulus absent
				skip = True #then the skip value is changed...
				log.write('other tasks skipped because stimulus was deemed absent') #if tasks were skipped, that's logged
	if skip == False: #...and the other 2 tasks are skipped
		#Localization task
		if task_local: #if the localization task was chosen to take place
			local_instructions.draw() #it does take place
			win.flip()
			key_local = waitKeys(keyList = [button_local_left, button_local_right, button_quit])
			if key_local[-1] == button_quit:
				log.write('Experiment quit')
				break
			log.write(f'{key_local}\t')

		#Discrimination task
		if task_disc:
			disc_instructions.draw()
			win.flip()
			key_disc = waitKeys(keyList = [button_disc_A, button_disc_B, button_quit])
			if key_disc[-1] == button_quit:
				log.write('Experiment quit')
				break
			log.write(f'{key_disc}\t')

	log.write('\n') #after the tasks, go to the next row in the log (for the next trial)
	trial_number += 1

win.close() #after the participant made it through all trials, shut down the screen
log.close() #and close the log