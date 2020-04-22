def contains(data, target):
  for item in data:
    if item == target:               # found a match
      return True
  return False

lst = [1,3,5,"great", "small", 321.567]
print (contains(lst, 5))
print (contains(lst, "big"))

