
import sys, copy

#chunkSize is the size to break down the input message
chunkSize = 4

def main(argv):
    if len(argv) < 2:
        print("Not enough params")
        return
    if argv[0] == "file":
        finalHash = hashFile(argv[1])
    elif argv[0] == "string":
        string = ""
        for r in argv[1:]:
            string = string + r
        finalHash = hashString(string)
    else:
        print("invalid option, options are \"file <filename>\" or \"string <message to hash>\"")
        return
    print("Hash: ", finalHash)

def hashFile(file):
    # hashFile hashes the contents of a file
    return hashChunks(fileToChunks(open(file, "rb"), chunkSize))

def hashString(string):
    # hashString hashes the string
    return hashChunks(stringToChunks(string, chunkSize))

def hashChunks(chunks):
    hashValue = [89, 103, 67, 199]
    for chunk in chunks:
        hashValue = processChunk(hashValue, chunk)
    finalHash = ""
    for h in hashValue:
        hexValue = hex(h)
        if len(hexValue) < 4:
            finalHash = finalHash + "0" + hex(h)[2:]
        else:
            finalHash = finalHash + hex(h)[2:]
    return finalHash

def processChunk(newHash, data):
    # hash is a byte array of size 4
    for word in data:
        for t in range(4):
            newHash[0] = newHash[0] ^ leftRotate(word, t)
            newHash[1] = newHash[1] ^ rightRotate(word, t)
            newHash[2] = rightRotate(newHash[2], t) ^ leftRotate(word, t)
            newHash[3] = leftRotate(newHash[3], t) ^ rightRotate(word, t)
            for t in range(3):
                newHash[t] = (newHash[t] | word) ^ (newHash[t+1] & word)
    return newHash

def stringToChunks(string, chunkSize):
    chunks = []
    currentChunk = []
    for char in string:
        if len(currentChunk) >= chunkSize:
            chunks.append(currentChunk)
            currentChunk = []
        currentChunk.append(ord(char))
    if len(currentChunk) > 0:
        while len(currentChunk) < chunkSize:
            currentChunk.append(0)
        chunks.append(currentChunk)
    return chunks

def fileToChunks(file, chunkSize):
    chunks = []
    currentChunk = []
    byte = file.read(1)
    while byte:
        if len(currentChunk) >= chunkSize:
            chunks.append(currentChunk)
            currentChunk = []
        currentChunk.append(int.from_bytes(byte, "big"))
        byte = file.read(1)
    if len(currentChunk) > 0:
        while len(currentChunk) < chunkSize:
            currentChunk.append(0)
        chunks.append(currentChunk)
    return chunks

def leftRotate(n, d):
    # leftRotate rotates bits to the left
    return ((n << d)|(n >> (8 - d))) & 0xFF

def rightRotate(n, d):
    # rightRotate rotates bits to the right
    return (n >> d)|(n << (8 - d)) & 0xFF


if __name__ == "__main__":
   main(sys.argv[1:])