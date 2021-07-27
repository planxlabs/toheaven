from sys import stdin, stdout

class Serial:        
    def read(self, size=-1):
        return stdin.buffer.read(size)
        
    def write(self, data):
        stdout.write(bytearray(data))
