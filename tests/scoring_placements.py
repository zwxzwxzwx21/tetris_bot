class A:
    def __init__(self, i = 1):
        self.i = i

    def m1(self):
        self.i += 1

class B(A):
    def __init__(self, j = 1):
        A.__init__(self, 3)
        self.j = j

    def m1(self):
        self.j -= 1


b = B()
b.m1()
print(b.i, b.j)