from datetime import datetime


def time_function():
    myFile = open('append.txt', 'a')
    myFile.write('\nAccessed on ' + str(datetime.now()))


if __name__ == '__main__':
    time_function()
