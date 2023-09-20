sp = [1,2,3,4,5,6,7,8,9]

tmp = []
for i in range(1, len(sp) + 1):
    if i % 3 != 0:
        tmp.append(sp[i-1])
print(tmp)

sp_new = [v for i,v in enumerate(sp) if (i + 1) % 3 != 0]
print(sp_new)