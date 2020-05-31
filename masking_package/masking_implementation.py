"""
@author: Dom
"""
#Version 1.9
#Goal for Version 2.0: See ReadMe -> future directions

#Import modules
from psychopy.visual import Window, ImageStim, TextStim
from psychopy.core import wait
from psychopy.event import getKeys, clearEvents, waitKeys
from masking_functions import create_trial_sequence, determine_masking_type, reverse_to_default, adjust_integer


win = Window(size = (1280,720), units = 'pix', fullscr = False, color = (0,0,0))

#Before running the code, the user should create ImageStim for their stimuli
#(i.e., target, masks, foil), unless they just want to use the default ones

#e.g. (using another picture that comes with the package),
#mask = ImageStim(win, 'example_alternative.png')


def load_default_values():
	'''This simple function loads in default values. It is performed as part
	of the main script.'''
	global center, left, right, detec_txt, local_txt, disc_txt, disc_txt2, disc_txt3

	#Defining default values
	#Coordinates for the picture locations
	left, center, right = (-250,0), (0,0), (250,0)

	#Initializing placeholders for the pre-experiment instructions, based on
	#which tasks are chosen ("When seeing the stimuli, pay attention to ...")
	detec_txt = local_txt = disc_txt = disc_txt2 = disc_txt3 = ''
	return center, left, right, detec_txt, local_txt, disc_txt, disc_txt2, disc_txt3


def draw_stim(user_image_stim, default_image_stim, location):
	'''This function displays image stimuli (mask, foil, target). If the
	entered object is not an ImageStim (which is an object class from
	PsychoPy.visual), the example picture of the package is used, instead.'''
	if isinstance(user_image_stim, ImageStim):
		p = user_image_stim
	else:
		p = default_image_stim
		print(f'Warning, {user_image_stim} is not an object of class ImageStim!'
		      + f'The program used the default picture "{default_image_stim}", instead.')
	p.setPos(location)
	p.draw()


def masking_experiment(target, mask, category_b,
					   N_trials=17, N_blanks=0, type_of_masking="Backw",
					   mask_forw_durat=100, mask_backw_durat=100,
					   target_durat=34, task_detec=True, task_local=True,
					   task_disc=True, disc_cat_A='woman', disc_cat_B='man',
					   button_quit='q', button_detec_pres='z',
					   button_detec_abs='m', button_local_left='left',
					   button_local_right='right', button_disc_A='a',
					   button_disc_B='l', button_welcomescreen_quit='space',
					   fixation_cross=True, detec_skip=False):
	'''This is the main function of this module. It allows you to run several
	types of masking experiments.
	...

    Parameters / User input

	----------

	N_trials: int
		An integer indicating on how many trials you want to show stimuli
		(i.e., targets, and/or foils).
	N_blanks: int
		An integer indicating on how many trials you want to show no stimuli
		(i.e., how many "blank trials" you want).
	type_of_masking: str
		A string indicating what type of masking you want to have.
			Values: 'Forw', 'forw', 'Forward', 'forward', 'F', 'f'
						for forward masking (mask shown before target)
					'Backw', 'backw', 'Backward', 'backward','B', 'b'
						for backward masking (mask shown after target)
					'Sandw', 'sandw', 'Sandwich', 'sandwich', 'S', 's'
						for sandwich masking (mask shown before & after target)
	target: ImageStim
		An psychopy.visual ImageStim which represents the target stimulus.
	mask: ImageStim
		An psychopy.visual ImageStim which represents the mask stimulus.
	category_b: ImageStim
		An psychopy.visual ImageStim for the stimulus of category B (if you
		have a discrimination task, the participants have to indicate whether
		the picture was of category A / the "target" or of category B / the
		"foil").
	mask_forw_durat: int
		An integer indicating the length (in milliseconds) for which you want
		to display the forward mask.
	mask_backw_durat: int
		An integer indicating the length (in milliseconds) for which you want
		to display the backward mask.
	target_durat: int
		An integer indicating the length (in milliseconds) for which you want
		to display the target (and foil, if participants perform a
		discrimination task).
	task_detec: bool
		A boolean indicating whether or not you want to include a detection
		task: Participants have to indicate whether or not they saw a target.
		N.B.: If you choose this option, this module will not remind or require
		you to include blank trials, (even though the task is often
		accompanied by them), because sometimes it is used without blank trials
		(e.g., with short exposure times).
	task_local: bool
		A boolean indicating whether or not you want to include a localization
		task: Participants have to indicate whether the target (or foil, if
		discrimination task, is also chosen) was displayed on the left or the
		right.
	task_disc: bool
		A boolean indicating whether or not you want to include a
		discrimination task: Participants are shown targets of two categories
		(often called "target" and "foil") and have to indicate whether the
		displayed picture was of one category, or of the other.
	disc_cat_A: str
		A string indicating the name of the first category (or "target
		category"). Relevant only, if you have a discrimination task.
	disc_cat_B: str
		A string indicating the name of the second category (or "foil
		category"). Relevant only, if you have a discrimination task.
	button_quit: str
		A string indicating the button participants can press to quit the
		experiment.
	button_detec_pres: str
		A string indicating the button participants should press when
		they think the stimulus was present (for a detection task).
	button_detec_abs: str
		A string indicating the button participants should press when
		they think the stimulus was absent (for a detection task).
	button_local_left: str
		A string indicating the button participants should press when
		they think the stimulus was shown on the left (for a
		localization task).
	button_local_right: str
		A string indicating the button participants should press when
		they think the stimulus was shown on the right (for a
		localization task).
	button_disc_A: str
		A string indicating the button participants should press on a
		discrimination task when they think the stimulus was
		from category A (also sometimes referred to as "target category").
	button_disc_B: str
		A string indicating the button participants should press on a
		discrimination task when they think the stimulus was
		from category B (also sometimes referred to as "foil category").
	button_welcomescreen_quit: str
		A string indicating the button participants have to press to move on
		from the welcome screen.
	fixation_cross: bool
		A boolean indicating whether or not you want to include a fixation
		cross before each trial (a + in the center of the screen, indicating
		indicating the onset of a new trial as well as the center of the
		screen).
	detec_skip: bool
		A boolean indicating whether other tasks are skipped on trials where
		participants state that they did not perceive a stimulus.
	'''
	#Firstly, I define some default values...
	center, left, right, detec_txt, \
	local_txt, disc_txt, disc_txt2, disc_txt3 = load_default_values()

	#and create some necessary items (i.e., they are necessary for step 2)
	#namely, the fixation cross
	fix = TextStim(win, text = "+", pos = center, height = 40)

	#and example/default pictures
	example_mask = ImageStim(win, 'round_mask.png') # for mask
	example_target = ImageStim(win, 'target.png') #target stimulus
	example_foil = ImageStim(win, 'foil.png') #and foil stimulus

	#Secondly, I check all user input values for whether they are legal
	#if they are not, they are replaced by the functions' defaults
	#(if possible) and the user is notified.
	#They are checked in order of appearance within the input bracket:

	N_trials = adjust_integer(N_trials)
	N_blanks = adjust_integer(N_blanks)
	mask_forw_durat = adjust_integer(mask_forw_durat)
	mask_backw_durat = adjust_integer(mask_backw_durat)
	target_durat = adjust_integer(target_durat)
	type_of_masking = reverse_to_default(type_of_masking, str, 'b')
	target = reverse_to_default(target, ImageStim, example_target)
	mask = reverse_to_default(mask, ImageStim, example_mask)
	category_b = reverse_to_default(category_b, ImageStim, example_foil)
	task_detec = reverse_to_default(task_detec, bool, True)
	task_local = reverse_to_default(task_local, bool, True)
	task_disc = reverse_to_default(task_disc, bool, True)
	disc_cat_A = reverse_to_default(disc_cat_A, str, 'woman')
	disc_cat_B = reverse_to_default(disc_cat_B, str, 'man')
	button_quit = reverse_to_default(button_quit, str, 'q')
	task_detec = reverse_to_default(task_detec, bool, True)
	button_detec_pres = reverse_to_default(button_detec_pres, str, 'z')
	button_detec_abs = reverse_to_default(button_detec_abs, str, 'm')
	button_local_left = reverse_to_default(button_local_left, str, 'left')
	button_local_right = reverse_to_default(button_local_right, str, 'right')
	button_disc_A = reverse_to_default(button_disc_A, str, 'a')
	button_disc_B = reverse_to_default(button_disc_B, str, 'l')
	button_welcomescreen_quit = reverse_to_default(button_welcomescreen_quit,
												   str, 'space')
	fixation_cross = reverse_to_default(fixation_cross, bool, True)
	detec_skip = reverse_to_default(detec_skip, bool, False)


	#Afterwards, I translate some user input into values for the main function
	mask_forw, mask_backw = determine_masking_type(type_of_masking)
	mask_forw_durat = (mask_forw_durat/1000)  # e.g., Psychopy works with sec.
	mask_backw_durat = (mask_backw_durat/1000)
	target_durat = (target_durat/1000)

	#Thirdly, I prepare the log and the welcome message.

	#I create to-be-filled placeholder (text) objects...
	#...for the welcome screen
	welcome_txt = TextStim(win, text = "", pos = center, height = 30)

	#...for the (within-experiment) instructions of each task ("Press XYZ for...")
	detec_instructions = TextStim(win, text = "", pos = center, height = 30)
	local_instructions = TextStim(win, text = "", pos = center, height = 30)
	disc_instructions = TextStim(win, text = "", pos = center, height = 30)

	#I initialize the Data log
	log = open('log.txt', 'w')

	#The trial number will be logged, no matter which task(s)
	#(if any) is/are chosen.
	log.write('trial_number\ttrial_type\t')
	#The welcoming message and log is appended based on the tasks chosen
	if task_detec:  #e.g., if detection is chosen, instructions are adapted...
		detec_txt = '\nPay attention to whether or not a picture is shown. '
		log.write('button_detection\t')  #and I add to the log's header
	if task_local:
		local_txt = '\nPay attention to whether the picture is shown left or right. '
		log.write('button_localization\t')
	if task_disc:
		disc_txt = f'\nPay attention to whether the picture shows a(n) {disc_cat_A} or a(n) {disc_cat_B}. '
		log.write('button_discrimination\t')

	#After all tasks are added to the header,
	#the log moves on to the next row (ready to note participants' responses)
	log.write('\n')

	#If no tasks are chosen, these "task_" objects will remain empty
	#as initialized: ''
	#Then, only the generic parts of the welcome message are displayed
	#(i.e., it will be appended with nothing / the content of empty objects).

	welcome_txt.setText(f'Welcome to the experiment! \n \nIn this experiment, '
					 f'you will be shown pictures.{detec_txt}{local_txt}'
					 f'{disc_txt} \nOnce the experiment starts, you can quit '
					 f'anytime by pressing the "{button_quit}" button. '
					 '\n\nProcede to the experiment by pressing the '
					 f'"{button_welcomescreen_quit}" button. Enjoy!')

	#I adjust task instructions, based on the buttons users selected
	detec_instructions.setText(f'Press "{button_detec_pres}", '
							+ f'if a picture was shown and "{button_detec_abs}'
							+ '", if no picture was shown.')
	local_instructions.setText(f'Press "{button_local_left}", if the picture '
							+ f'was shown to the left and "{button_local_right}'
							+ '", if the picture was shown to the right.')
	disc_instructions.setText(f'Press "{button_disc_A}", if the picture showed'
						   + f' a(n) {disc_cat_A} and press "{button_disc_B}",'
						   + f' if the picture showed a(n) {disc_cat_B}.')

	#Onto the actual implementation of the experiment
	#Firstly, I activate a function that creates a unique trial sequence
	N_types = create_trial_sequence(N_trials, N_blanks, task_local, task_disc)

	#Then, I display the welcome text, until participants choose to move on
	welcome_txt.draw()
	win.flip()
	waitKeys(keyList = [button_welcomescreen_quit])
	clearEvents()  # Ignoring the within-trials quit button before trial onset

	for trial_number in range(len(N_types)):  # In every trial that is implemented
		quitkey = getKeys(keyList = [button_quit])  # check for the quit button
		if len(quitkey) > 0:  # if it was pressed,
			log.write('Participant quit the experiment')
			break  # stop the experiment (or at least, the trials / for-loop)
		clearEvents()
		#if the stimuli is supposed to be shown non-centrally
		#(indicated by trial_type index)
		if	N_types[trial_number] < 5:
			#if they're supposed to be shown left (i.e., their index
			#is an odd number)
			if	N_types[trial_number] % 2 == 1:
			    #all pictures are shown left.
				target.setPos(left)
				category_b.setPos(left)
			else:  # If they're supposed to be shown on the right,
				#all pictures are shown right
				target.setPos(right)
				category_b.setPos(right)
		else:  #In other cases, else they're shown in the center
			#which is true for trials with indices of >= 5 (i.e., or is '9',
			#which are blank trials, so the location of the "stimulus" does not
			#matter (since no stimulus is shown).
			target.setPos(center)
			category_b.setPos(center)
		if fixation_cross:  #Implement a fixation cross, if requested.
			fix.draw()
			win.flip()
			wait(0.1)  # A fixation cross is shown for 100ms before trial onset
			wait(0.008)  #wait for half a frame (assuming 60 Hz) to counteract
						 #refresh rate imprecisions

		#Forward masking / (or 'first half of the sandwich masking')
		if mask_forw:
			if task_local:  # if people have to determine whether the target
				#was left or right, the mask has to be drawn on both sides
				#so that it does not give away the target location
				draw_stim(mask, example_mask, right)
				draw_stim(mask, example_mask, left)
			else:
				draw_stim(mask, example_mask, center)
			win.flip()
			wait((mask_forw_durat - 0.008))  # display the mask for the
			#requested duration (minus half a frame)

		#Show stimulus (i.e., target or foil / category B stimulus)
		wait(0.008)
		if	N_types[trial_number] == 9:  # if no stimulus is supposed to be shown
			pass  # nothing happens
		elif N_types[trial_number] in [1, 2, 5]:  # These index numbers
			#indicate indicate that a target has to be drawn.
			target.draw()
		else:  # For other index numbers, a foil / category B stimulus is shown
			category_b.draw()
		win.flip()
		wait((target_durat - 0.008))

		#Backward masking / (or 'second half of the sandwich masking')
		if mask_backw:
			if task_local:  #If people have to determine whether the target
				#was left or right, the mask must be drawn both left and right
				#so that it does not give away the target location
				wait(0.008)
				draw_stim(mask, example_mask, right)
				draw_stim(mask, example_mask, left)
			else:
				wait(0.008)
				draw_stim(mask, example_mask, center)
			win.flip()
			wait((mask_backw_durat - 0.008))

		win.flip()  # Clearing the screen (either after backward mask or target)
		#Logging the trial number, before we get to task-specific logging.
		log.write(f'{(trial_number+1)}\t')

		#Implementing the tasks (insofar as requested)

		#Detection task
		if task_detec:
			detec_instructions.draw()
			win.flip()
			key_detec = waitKeys(keyList = [button_detec_pres, button_detec_abs,
								   button_quit])
			if key_detec[-1] == button_quit:  # If they pressed the quit button
				log.write('Experiment quit')
				break  # the experiment ends.
			log.write(f'{key_detec}\t')	 #Else the response is logged

		#The other two tasks might be skipped, if certain conditions occur:
		skip = False  # In general, we do not skip tasks, unless
		#the user told us to skip tasks on trials when participants say
		#stimuli were absent, assuming...
		if detec_skip:
			if task_detec: #...a detection task actually took place...
				#and the participant actually said the stimulus was absent.
				if key_detec[-1] == button_detec_abs:
					skip = True  # Then the skip value is changed...
					#...we log the skipping of followup tasks...
					log.write('Other tasks were skipped because stimulus was deemed absent')
					#...and the other 2 tasks are skipped.
		if skip == False:
			#Localization task
			if task_local:  #If the localization task was chosen to take place,
				local_instructions.draw()  #it does take place.
				win.flip()
				key_local = waitKeys(keyList = [button_local_left,
									button_local_right, button_quit])
				if key_local[-1] == button_quit:
					#Throughout the tasks, I continuously check whether
					#participants want to quit.
					log.write('Experiment quit')
					break
				log.write(f'{key_local}\t') #And else log their responses.

			#Discrimination task
			if task_disc:
				disc_instructions.draw()
				win.flip()
				key_disc = waitKeys(keyList = [button_disc_A, button_disc_B,
								   button_quit])
				if key_disc[-1] == button_quit:
					log.write('Experiment quit')
					break
				log.write(f'{key_disc}\t')

		#After the tasks, the log moves onto the next row (for the next trial).
		log.write('\n')
		trial_number += 1

	#After the participant made it through all trials, the screen is shut down
	#and the log is closed.
	win.close()
	log.close()