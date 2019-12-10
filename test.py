class A:
    def __init__(self, hi):
        self.hi = 2
    def methodyay(self):
        print(self.hi + 4)
class B:
    def __init__(self, yo):
        self.yo = yo

a = A(2)
new = a
b = B(2)

if (a == new):
    print('working')


#whats going on with super
class ooogabooga(A):
    def __init__(self, hi, hat):
        super().__init__(hi)
        self.hat