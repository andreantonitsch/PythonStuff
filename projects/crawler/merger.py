import sys
import os

if __name__ == '__main__':
    path = sys.argv[1]

    concatenated = ''

    for filename in os.listdir(path):
        file_data = open(path + '/' + filename, 'r')
        
        concatenated += '\n' + file_data.read()

    output = open('data.txt', 'w')
    output.write(concatenated)
    output.close()