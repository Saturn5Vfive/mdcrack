# Written by saturn5Vfive

import ctypes  # ctypes allah
import queue
import threading
import hashlib

cracked = []

# function definitions
def batch(hashs):
    while True:
        #get a task and do it
        task = master.get()
        encoded = hashlib.md5(task.encode()).hexdigest()
        matched = False
        #check if its any one of the hashes on our list
        for hashr in hashs:
            if encoded == hashr:
                matched = True
                print(f"{color.GREEN}Match! {task} : {hashr}")
                #if its a correct hash append it to the list
                cracked.append(task + " : " + hashr)
        if not matched:
            print(f"{color.GREEN}Tried {task} without success ({encoded})")
        master.task_done()


# Set up a colors class so we can make the thing look cool
class color:
    GREEN = '\033[92m'


# Format the console window so we can put the color codes in, code from online
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Start a queue so we can not make it shit and slow
master = queue.Queue()

# print out an epic logo
print(f"{color.GREEN}███╗░░░███╗██████╗░░█████╗░██████╗░░█████╗░░█████╗░██╗░░██╗")
print(f"{color.GREEN}████╗░████║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║░██╔╝")
print(f"{color.GREEN}██╔████╔██║██║░░██║██║░░╚═╝██████╔╝███████║██║░░╚═╝█████═╝░")
print(f"{color.GREEN}██║╚██╔╝██║██║░░██║██║░░██╗██╔══██╗██╔══██║██║░░██╗██╔═██╗░")
print(f"{color.GREEN}██║░╚═╝░██║██████╔╝╚█████╔╝██║░░██║██║░░██║╚█████╔╝██║░╚██╗")
print(f"{color.GREEN}╚═╝░░░░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝")

# Im just going to assume you arent stupid enough to put something into here that doesnt exist
pwlist = input(f"{color.GREEN}Passwords (file name)\n>")
hashlist = input(f"{color.GREEN}Hashes (file name)\n>")

#read hash and password files
print(f"{color.GREEN}Reading hashes file")
hashfile = open(hashlist, "r")
hashes = []
for hasha in hashfile.readlines():
    ha = hasha.strip().strip("\n")
    hashes.append(ha)
    print(f"{color.GREEN}{ha}")
print(f"{color.GREEN}Got Hashes")

print(f"{color.GREEN}Loading passwords")
passfile = open(pwlist, "r")
passwords = []
for line in passfile.readlines():
    passwords.append(line.strip().strip("\n"))
print(f"{color.GREEN}Is this information good?")
input(f"{color.GREEN}(press enter to continue)")
print(f"{color.GREEN}Starting Queue")

#load our passwords into the queue
for password in passwords:
    master.put(password)

#Start 200 threads that check for the hash
for _ in range(200):
    thread = threading.Thread(target=batch, args=(hashes,), daemon=True)
    thread.start()


#display the cracked hashes after
master.join()
print(f"{color.GREEN}Operation Completed!")
print(f"{color.GREEN}Hashes:")
for hashe in cracked:
    print(f"{color.GREEN}{hashe}")
input()
