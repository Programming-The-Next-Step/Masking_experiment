'''This code contains background functions, that is:
   "Functions the user does not have to see"'''


def adjust_integer(user_input):
	'''A function that converts floats into integers and negative into
	positive numbers (as negative numbers and non-integers are not valid
	input values for any of the functions)'''
	if (isinstance(user_input, int) == False) or (user_input < 0):
		try:
			output = int(user_input)
			if output < 0:
				output = output*-1
				print(f'Warning! The value {user_input} is not a positive '
					  + 'integer. '
					  + f'We assume you mistyped and, hence, adjusted it to {output}.')
		except ValueError:
			print(f'An error occured, because "{user_input}" is not an integer'
				  +' and could not be transformed into one.')
	else:
		output = user_input
	return output


def reverse_to_default(user_input, supposed_level, default_value):
	'''This function tests whether the user's input is of the desired value
	level (e.g., 'bool' for boolean). If it is not, the default value of the
	package is used, instead (e.g., 'True' for the variable 'fixation_cross').'''
	if isinstance(user_input, supposed_level):
		return user_input
	else:
		print(f'Warning! The value "{user_input}" is not a(n) {supposed_level}. '
			  +f'The program used the default value "{default_value}", instead.')
		return default_value


def determine_masking_type(mask_type):
	'''This function translates string inputs from users (about which type
	of masking they want) into boolean values which the functions
	"masking_experiment" and "create_trial_sequence" use.'''
	global mask_forw, mask_backw
	if mask_type in ('Forw', 'forw', 'Forward', 'forward', 'F', 'f'):
		mask_forw = True
		mask_backw = False
	elif mask_type in ('Backw', 'backw', 'Backward', 'backward','B', 'b'):
		mask_forw = False
		mask_backw = True
	elif mask_type in ('Sandw', 'sandw', 'Sandwich', 'sandwich', 'S', 's'):
		mask_forw = True
		mask_backw = True
	else:
		print(f'Warning, {mask_type} does not represent a value which makes '
			  + 'masks appear. Currently, no mask is displayed.')
		mask_forw = False
		mask_backw = False
	return mask_forw, mask_backw


def create_trial_sequence(N_entered, N_blanks, task_local, task_disc):
	'''This function has two tasks: Firstly, it adjusts the number of trials,
	if necessary (based on which tasks were picked). Then it creates a list
	containing the order of all trials.'''
	from random import shuffle
	#Save the entered value (for testing this function
	#and for communicating with the user, if their N was changed)
	global N_before
	N_before = N_entered

	#The first part of the function checks whether we need 1,
	#2 (left vs right, or category A or B)
	#or 4 different types of trials: 2 (direction) X 2 (category).
	complexity = 0
	if task_local:
		complexity += 1
	if task_disc:
		complexity += 1

	#If neither localization or discrimination tasks occur,
	#the number of trials does not need to be adjusted
	#(i.e., the if-statements are skipped).
	#If we have either of the two, ...
	if complexity == 1:
		#...we only need to ensure that the number of trials is even.
		if N_entered % 2 != 0:
			N_entered += 1
	#If it's both of these tasks, ...
	if complexity == 2:
		#...the number of trials needs to be divisible by 4 (2x2 trial types).
		while N_entered % 4 != 0:
			N_entered += 1

	#If the total N of trials had to be changed, we notify the user.
	if 	N_entered > N_before:
		print(f'Warning! Your N of (non-blank) trials was adjusted to {N_entered},'
			  +' so that the number of trials per condition is balanced.')

	#The second half of this function, creates the actual list of trials
	#(the trial sequence) with each number representing another type of trial.
	global N_types
	N_types = []
	i = 0
	#If there is one of the two tasks that demands multiple trial types...
	if complexity == 1:
		if task_local:  # ...we check the type of task, if it's localization...
			while i < (N_entered/2):
				N_types.append(1)  # ...half the trials will be on the left,...
				N_types.append(2)  # ...the other on the right.
				i += 1
		else:  #If it's the discrimination task...
			while i < (N_entered/2):
				#half of the trials will show targets (in the center of screen)
				N_types.append(5)
				#the other half, will show foils (center of screen).
				N_types.append(6)
				i += 1
	elif complexity == 2:  #If it's both tasks
		while i < (N_entered/4):
				N_types.append(1)  # a quarter shows target on the left,
				N_types.append(2)  # another quarter shows target on the right,
				N_types.append(3)  # another shows foils on the left,
				N_types.append(4)  # and another shows foils on the right.
				i += 1
	else:  #If it's neither of these 2 tasks (no task, or only detection task),
		while i < N_entered:
			#stimuli are presented in the middle of the screen on every trial.
			N_types.append(5)
			i += 1
	i = 0
	#Afterwards, we add the blank trials (if there are any).
	while i < N_blanks:
		N_types.append(9)
		i += 1
	#And finally, randomize the order of trials.
	shuffle(N_types)
	return(N_types)