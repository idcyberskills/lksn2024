flag1 = False
flag2 = False
flag3 = False
flag4 = False

print("""
1. The attacker seems to build a custom rootkit-like kernel object to the victim OS. What's the kernel module load address for that rootkit?

Answer is in the hexadecimal address form 

For example if it's in the 0xffffffffabcdc0fe then the answer is 0xffffffffabcdc0fe
    """)
answer1 = input("Answer >> ")
if answer1 == "0xffffffffc0551000":
    print('Correct!\n')
    flag1 = True
else:
    print('Wrong!\n')


print("""
2. There's a zip file that is created by the user. This file is password-protected and it is cached. In what inode number that this file is cached?

Answer format is in integer.

Example, if it is resided in inode number 765 then the answer is 765.
    """)
answer2 = input("Answer >> ")
if answer2 == "2095015":
    print('Correct!\n')
    flag2 = True
else:
    print('Wrong!\n')


print("""
3. It seems the password that is used for the zip file is stored in a linux variable. Can you find its variable name? And what is the value of that? This will indicate its password

Answer format is NAMEOFTHEVARIABLE_VALUE

For example, you found that the password is stored in Linux variable called jaBa, and the value of jaja is pass123. So the answer is jaBa_pass123
    """)
answer3 = input("Answer >> ")
if answer3 == "FANATIC_cZn5xU67st3LI":
    print('Correct!\n')
    flag3 = True
else:
    print('Wrong!\n')


print("""
4. The uncovered zip content may leaks the APT plan in order to breach their targeted victim company and usually it involves a name of their higher ups. 
Can you tell us WHO will likely to be targeted (not an OSINT challenge) ?

Answer is the name format. 
Example if the name is Robi Jamada then please input it with space replaced by underscore -> Robi_Jamada
    """)
answer4 = input("Answer >> ")
if answer4 == "Armin_Bahanang":
    print('Correct!\n')
    flag4 = True
else:
    print('Wrong!\n')



if flag1 and flag2 and flag3 and flag4:
    print("You are a truly forensicator ! Cool we'll now hunt the APT-41, our cyber legacy will continue on next chapter in LKSN2025 ? :) Anyway here's your flag: ")
    print("LKSN{y0u_h4ve_overcome_the_b3ginner_Linux_Memf0ren_such_daredevils5s5s5!}")
else:
    print('If you get this message but you got all answers correct, please contact the judges and send the proof + each of your answers.')