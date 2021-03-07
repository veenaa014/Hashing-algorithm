import sys, random, string

from hash import hashString

def main(argv):
    dictionary = {hashString("Hello world!"): "Hello world!"}
    
    count = 0
    while True:
        input = randomString(16)
        hash = hashString(input)
        if hash in dictionary:
            print("COLLISION FOUND after", count, "attempts!\nThe following produce the same hash:")
            print(input)
            print(dictionary[hash])
            print("Hash: " + hash)
            return
        else:
            dictionary[hash] = input
        count = count + 1

def randomString(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k = size))

if __name__ == "__main__":
   main(sys.argv[1:])