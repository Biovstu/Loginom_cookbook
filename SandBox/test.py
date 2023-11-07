sp = [9,2,1,4,4,8,6,7,7,8,9,1]

sp_new = [v for i,v in enumerate(sp) if v not in sp[:i]]
print(sp_new)
print(list(set(sp)))
print(sp[::2])