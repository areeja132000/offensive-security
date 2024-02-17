from pwn import *

numbers = {"ZERO":"0", "ONE":"1", "TWO":"2", "THREE":"3", "FOUR":"4", "FIVE":"5", "SIX":"6", "SEVEN":"7", "EIGHT":"8", "NINE":"9"}
operations = [" + ", " - ", " * "]

p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1236)

print(p.recvuntil(b"Can you prove that you're a real math whiz??\n"))
question = p.recvline()
question_cleaned = question.decode('utf-8')
while('?' in question_cleaned):
    print(question)
    words = False
    for key in numbers:
        if key in question_cleaned:
            words = True
            break
    if (words):

        for key in numbers:
            question_cleaned = question_cleaned.replace(key, numbers[key])

        determined_operation = ""
        for operation in operations:
            if operation in question_cleaned:
                determined_operation = operation

        two_numbers = question_cleaned.split(determined_operation)
        two_numbers[0] = two_numbers[0].replace("-", "")
        two_numbers[1] = two_numbers[1].replace("-", "")
        question_cleaned = two_numbers[0]+ determined_operation+ two_numbers[1]     
        index = question_cleaned.index(" =")
        print(question_cleaned)
        p.send(bytes(str(eval(question_cleaned[:index])) + "\n", 'utf-8'))
    else:
        index = question_cleaned.index(" =")
        p.send(bytes(str(eval(question_cleaned[:index])) + "\n", 'utf-8'))
    print(p.recvline())
    question = p.recvline()
    question_cleaned = question.decode('utf-8')

print(question_cleaned)