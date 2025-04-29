from math import gcd

class RationalValueError(ValueError):
    def __init__(self, message="Invalid data provided"):
        super().__init__(message)

class Rational:
    def __init__(self, numerator, denominator=None):
        if denominator is None:
            parts = numerator.split('/')
            numerator, denominator = int(parts[0]), int(parts[1])
        if denominator == 0:
            raise RationalValueError("Denominator cannot be zero")
        self.n = numerator
        self.d = denominator
        self.reduce()

    def reduce(self):
        common_divisor = gcd(self.n, self.d)
        self.n //= common_divisor
        self.d //= common_divisor

    def __add__(self, other):
        if isinstance(other, Rational):
            numerator = self.n * other.d + other.n * self.d
            denominator = self.d * other.d
            return Rational(numerator, denominator)
        elif isinstance(other, int):
            numerator = self.n + other * self.d
            return Rational(numerator, self.d)
        else:
            raise RationalValueError("Addition requires Rational or integer")

    def __radd__(self, other):
        return self + other

    def __call__(self):
        return self.n / self.d

    def __str__(self):
        return f"{self.n}/{self.d}"

class RationalList:
    def __init__(self):
        self.elements = []

    def __getitem__(self, index):
        return self.elements[index]

    def __setitem__(self, index, value):
        if isinstance(value, Rational):
            self.elements[index] = value
        else:
            raise RationalValueError("Only Rational objects can be added to RationalList")

    def __len__(self):
        return len(self.elements)

    def __add__(self, other):
        new_list = RationalList()
        new_list.elements = self.elements.copy()
        if isinstance(other, RationalList):
            new_list.elements += other.elements
        elif isinstance(other, Rational):
            new_list.elements.append(other)
        elif isinstance(other, int):
            new_list.elements.append(Rational(other, 1))
        else:
            raise RationalValueError("Unsupported type for addition with RationalList")
        return new_list

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            self.elements += other.elements
        elif isinstance(other, Rational):
            self.elements.append(other)
        elif isinstance(other, int):
            self.elements.append(Rational(other, 1))
        else:
            raise RationalValueError("Unsupported type for addition with RationalList")
        return self

    def append(self, value):
        if isinstance(value, Rational):
            self.elements.append(value)
        else:
            raise RationalValueError("Only Rational objects can be appended to RationalList")

    def sum(self):
        total = Rational(0, 1)
        for element in self.elements:
            total += element
        return total

def process_input_files(input_files, output_file):
    rational_list = RationalList()
    for input_file in input_files:
        with open(input_file, 'r') as infile:
            for line in infile:
                numbers = line.strip().split()
                for number in numbers:
                    try:
                        if '/' in number:
                            rational_list.append(Rational(number))
                        else:
                            rational_list.append(Rational(int(number), 1))
                    except (ValueError, RationalValueError) as e:
                        print(f"Skipping invalid input '{number}': {e}")
    with open(output_file, 'w') as outfile:
        outfile.write(f"Sum of all rational numbers: {rational_list.sum()}\n")
        for rational in rational_list:
            outfile.write(f"{rational}\n")

input_files = ["input01.txt", "input02.txt", "input03.txt"]
output_file = "output.txt"

process_input_files(input_files, output_file)