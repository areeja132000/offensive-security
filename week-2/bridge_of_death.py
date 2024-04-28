def func2(param_1,param_2,param_3):
    iVar1 = param_2 + (param_3 - param_2) // 2
    print("{0} {1}".format(param_1, iVar1))
    if (param_1 < iVar1):
        iVar2 = func2(param_1,param_2,iVar1 + -1)
        iVar1 = iVar2 + iVar1
    elif (iVar1 < param_1):
        iVar2 = func2(param_1,iVar1 + 1,param_3)
        iVar1 = iVar2 + iVar1
    return iVar1

find = False
for num1 in range(1, 100):
    for num2 in range(1, 100):
        print("Input: {0} {1}".format(num1, num2))
        iVar1 = func2(num1,0,20)
        print("End: {0} {1}".format(iVar1, num2))
        if (iVar1 == num2):
            print("Correct!")
            find = True
            break
        else:
            print("Nope!")
    if (find):
        break