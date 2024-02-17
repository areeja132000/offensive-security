def recurse(num1,num2,num3,num4):
    num4 = ((num2 + num1) - num3) - num4
    if ((num3 == 16) and (num2 + num1 == 116369)):
        uVar1 = 1
    elif ((num3 < 16) and (((num1 < num4 or (num2 < num4)) or (num3 < num4)))):
        uVar1 = absolutely_not_useless_fn(num2,num2 + num1,num3 + 1,num4)
    else:
        uVar1 = 0
    return uVar1

def absolutely_not_useless_fn(num1,num2,num3,num4):
    useful_variable = (num4 + num1) - num3
    another_useful_one = num2 + num1
    val = recurse(num2,another_useful_one,num3 + 1,((another_useful_one + useful_variable) // 3) * 2)
    return val

find = False
for num1 in range(1, 100):
    for num2 in range(1, 100):
        print("{0} {1}".format(num1, num2))
        if ((num1 == 0) or (num2 == 0)):
            print("Values must both be non-zero!")
        else:
            iVar1 = recurse(num1,num2,0,1)
            if (iVar1 == 0):
                print("Nope!")
            else:
                print("Correct!")
                find = True
                break
    if (find):
        break