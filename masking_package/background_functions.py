'''Background functions, functions the user does not have to know about'''

def reverse_to_default(user_input, supposed_level, default_value):
	'''Tests whether the user input is of the desired value level (e.g., bool).
	If it is not, the default value of the package is used, instead.'''
	if isinstance(user_input, supposed_level):
		return user_input
	else:
		print(f'Warning! The value "{user_input}" is not a(n) {supposed_level}.'
			  + f'The program used the default value "{default_value}", instead.')
		return default_value

def draw_stim(image_stim_name, default_image_stim, location):
	'''Displays image stimulus (mask, foil, target). If the entered object
	is not an ImageStim (object type from PsychoPy), the example picture of
	the package is used, instead.'''
	if isinstance(image_stim_name, ImageStim):
		p = image_stim_name
		print(f'Warning, {image_stim_name} is not an object of class ImageStim!'
		      + f'The program used the default picture "{default_image_stim}", instead.' )
	else:
		p = default_image_stim
	#sets picture to the desired location
	p.setPos(location)
	p.draw()

def create_trial_sequence(N_entered, N_blanks, task_local, task_disc):
	'''Adjusts the number of trials, if necessary (based on which tasks were
	picked), then creates a list containing the order of all trials.
	task_local and task_disc are boolean variables (indicating whether the
	task is performed or not).'''
	#Finds out whether we need 1, 2 (left vs right, or category A or B)
	#or 4 different trial types 2 (direction) X 2 (category).

	complexity = 0
	if task_local:
		complexity += 1
	if task_disc:
		complexity += 1

	#if neither localization or discrimination tasks occur,
	#the number of trials does not need to be adjusted
	#(i.e., the if-statements are skipped)

	#if we have either the localization or discrimination task,
	if complexity == 1:
		#we only need to ensure that the number of trials is even
		if N_entered % 2 != 0:
			N_entered += 1
	#if it's both of these tasks,
	if complexity == 2:
		#the number of trials needs to be divisible by 4 (i.e., 2x2 trial types)
		while N_entered % 4 != 0:
			N_entered += 1

	#creating the actual list of trials (i.e, the trial sequence)

	#creating a list of trial types (each number being another type of trial)
	global N_types
	N_types = []
	i = 0
	#if there is one of tasks that demand multiple trial types
	if complexity == 1:
		if task_local: #we check the type of task, if it's localization...
			while i < (N_entered/2):
				N_types.append(1) #half the trials will be on the left
				N_types.append(2) #the other on the right
				i += 1
		else: #if it's the discrimination task
			while i < (N_entered/2):
				N_types.append(5) #half the trials will show targets (center of screen)
				N_types.append(6) #the other half, will show foils (center of screen)
				i += 1
	elif complexity == 2: #if it's both
		while i < (N_entered/4):
				N_types.append(1) #a quarter shows target on the left
				N_types.append(2) #another quarter shows target on the right
				N_types.append(3) #another: foils on the left
				N_types.append(4) #another: foils on the right
				i += 1
	else: #if it's neither of these 2 tasks (no task, or only detection task)
		while i < N_entered:
			N_types.append(5) #on all trials, stimuli are presented in the middle of the screen
			i += 1

	i = 0
	#then, we add the blank trials (if there are any)
	while i < N_blanks:
		N_types.append(9)
		i += 1
	#And finally, randomize the order of trials
	shuffle(N_types)


def determine_masking(mask_type):
	'''Translates string input from users into boolean values'''
	global mask_forw, mask_backw
	if mask_type in ('Forw', 'forw', 'Forward', 'forward', 'f'):
		mask_forw = True
	elif mask_type in ('Backw', 'backw', 'Backward', 'backward', 'b'):
		mask_backw = True
	elif mask_type in ('Sandw', 'sandw', 'Sandwich', 'sandwich', 's'):
		mask_forw = True
		mask_backw = True
	else:
		print(f'Warning, {mask_type} does not represent a value which makes '
			  + 'masks appear. Currently, no mask is displayed')
		mask_forw = False
		mask_backw = False

'''Constants (default values and objects)'''
#from psychopy.visual import Window, ImageStim, TextStim
#from psychopy.core import wait
#from psychopy.event import getKeys, clearEvents, waitKeys
#from random import shuffle

#default values
#standard coordinates for the picture locations
center, left, right = (0, 0), (-250, 0), (250, 0) #Mr/Ms reviewer, is this good or bad style?

#objects that are always needed
win = Window(size = (1280, 720), units = 'pix', fullscr = False, color = (0, 0, 0)) #create window object
fix = TextStim(win, text = "+", pos = center, height = 40) #fixation cross


#example pictures
example_mask = ImageStim(win, 'round_mask.png') # for mask
example_blank = ImageStim(win, 'blank.png') #blank screen
example_target = ImageStim(win, 'target.png') #target stimulus
example_foil = ImageStim(win, 'foil.png') #and foil stimulus

#initialize the data log
log = open('log.txt', 'w')


'''Placeholders'''
#for the welcome text
welcome_txt = TextStim(win, text = "", pos = center, height = 30)

#for the instruction texts of the 3 different tasks
detec_instructions = local_instructions = disc_instructions = TextStim(win, text = "",
																	   pos = center, height = 30)

#text placeholders (filled later, depending on which tasks are chosen)
detec_txt = local_txt = disc_txt = disc_txt2 = disc_txt3 = ''




