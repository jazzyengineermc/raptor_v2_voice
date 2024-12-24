import sys
import datetime
    

def help():
	sa = """Usage :-
$ ./todo add "todo item" # Add a new todo
$ ./todo ls			 # Show remaining todos
$ ./todo del NUMBER	 # Delete a todo
$ ./todo done NUMBER	 # Complete a todo
$ ./todo help			 # Show usage
$ ./todo report		 # Statistics"""
	sys.stdout.buffer.write(sa.encode('utf8'))


def add(s):
	f = open('todo.lst', 'a')
	f.write(s)
	f.write("\n")
	f.close()
	s = '"'+s+'"'
	print(f"Added todo: {s}")


td_list = []

def ls():
	try:
		d = {}
		f = open('todo.lst', 'r')
		c = 1
		for line in f:
			line = line.strip('\n')
			#speech = [str(c) + str(line)]
            #tts_piper(textToSpeak=speech)
			d.update({c: line})
			c = c+1
		l = len(d)
		k = l

		for i in d:
			td_list.append(sys.stdout.buffer.write(f"[{l}] {d[l]}\n".encode('utf8')))
			#sys.stdout.buffer.write("\n".encode('utf8'))
			l = l-1

	except Exception as e:
		raise e


def deL(no):
	try:
		if no == 'one':
			no = 1
		if no == 'two':
			no = 2
		if no == 'to':
			no = 2
		if no == 'three':
			no = 3
		if no == 'four':
			no = 4
		if no == 'five':
			no = 5
		if no == 'six':
			no = 6
		if no == 'seven':
			no = 7
		if no == 'eight':
			no = 8
		if no == 'ate':
			no = 8
		if no == 'nine':
			no = 9
		if no == 'ten':
			no = 10
		print(no)
		no = int(no)
		d = {}
		f = open('todo.lst', 'r')
		c = 1
		for line in f:
			line = line.strip('\n')
			d.update({c: line})
			c = c+1
		with open("todo.lst", "r+") as f:
			lines = f.readlines()
			f.seek(0)
			for i in lines:
				if i.strip('\n') != d[no]:
					f.write(i)
			f.truncate()
		print(f"Deleted todo #{no}")

	except Exception as e:
		print(f"Error: todo #{no} does not exist. Nothing deleted.")


def done(no):
	try:
		if no == 'one':
			no = 1
		if no == 'two':
			no = 2
		if no == 'to':
			no = 2
		if no == 'three':
			no = 3
		if no == 'four':
			no = 4
		if no == 'five':
			no = 5
		if no == 'six':
			no = 6
		if no == 'seven':
			no = 7
		if no == 'eight':
			no = 8
		if no == 'ate':
			no = 8
		if no == 'nine':
			no = 9
		if no == 'ten':
			no = 10
		print(no)
		d = {}
		f = open('todo.lst', 'r')
		c = 1
		for line in f:
			line = line.strip('\n')
			d.update({c: line})
			c = c+1
		no = int(no)
		f = open('done.txt', 'a')
		st = 'x '+str(datetime.datetime.today()).split()[0]+' '+d[no]
		f.write(st)
		f.write("\n")
		f.close()
		print(f"Marked todo #{no} as done.")
		
		with open("todo.lst", "r+") as f:
			lines = f.readlines()
			f.seek(0)
			for i in lines:
				if i.strip('\n') != d[no]:
					f.write(i)
			f.truncate()
	except:
		print(f"Error: todo #{no} does not exist.")


def report():
	d = {}
	f = open('todo.lst', 'r')
	c = 1
	for line in f:
		line = line.strip('\n')
		d.update({c: line})
		c = c+1
	try:
		don = {}
		nf = open('done.txt', 'r')
		c = 1
		for line in nf:
			line = line.strip('\n')
			don.update({c: line})
			c = c+1
		print(
			f'{str(datetime.datetime.today()).split()[0]} Pending : {len(d)} Completed : {len(don)}')
	except:
		print(
			f'{str(datetime.datetime.today()).split()[0]} Pending : {len(d)} Completed : {len(don)}')


def nec():
    try:
        f = open('todo.lst', 'r')
        c = 1
        for line in f:
            
            line = line.strip('\n')
            #print(c, line)
            d.update({c: line})
            c = c+1
        print(d)
    except:
        sys.stdout.buffer.write("There are no pending todos!".encode('utf8'))


if __name__ == '__main__':
	try:
		d = {}
		don = {}
		args = sys.argv
		if(args[1] == 'del'):
			args[1] = 'deL'
		if(args[1] == 'add' and len(args[2:]) == 0):
			sys.stdout.buffer.write(
				"Error: Missing todo string. Nothing added!".encode('utf8'))

		elif(args[1] == 'done' and len(args[2:]) == 0):
			sys.stdout.buffer.write(
				"Error: Missing NUMBER for marking todo as done.".encode('utf8'))

		elif(args[1] == 'deL' and len(args[2:]) == 0):
			sys.stdout.buffer.write(
				"Error: Missing NUMBER for deleting todo.".encode('utf8'))
		else:
			globals()[args[1]](*args[2:])

	except Exception as e:

		s = """Usage :-
$ ./todo add "todo item"     # Add a new todo
$ ./todo ls                  # Show remaining todos
$ ./todo del NUMBER          # Delete a todo
$ ./todo done NUMBER         # Complete a todo
$ ./todo help                # Show usage
$ ./todo report              # Statistics
"""
		sys.stdout.buffer.write(s.encode('utf8'))