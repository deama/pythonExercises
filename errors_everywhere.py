alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
alphabet2 = []
word = ""

for i, letter in enumerate(alphabet):
    alphabet2.append( alphabet[len(alphabet)-i-1] )

alphabet2.sort()

for letter in alphabet2:
    word = word+letter

print(word)
