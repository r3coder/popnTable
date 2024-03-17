lst = ["あ", "い", "2", "K"]

lst.sort()

print(lst)

for i in range(len(lst)):
    print(lst[0], ord(lst[0][0]))
    if ord(lst[0][0]) < 128:
        # send to back
        lst.append(lst.pop(0))
    print(lst)

print(lst)
