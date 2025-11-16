import math
import re

class Arithmetic:
    
    def __init__(self):
        self.last_result = 0
        self.memory = 0
    
    def calculate(self, expression):
        try:
            expression = expression.replace(' ', '')#spaces
            
            if not expression:
                print("ERROR: No expression provided")
                return
            if any(word in expression.lower() for word in ['import', '__', 'exec', 'eval', 'open', 'file']):
                print("ERROR: Invalid expression")#invalid op
                return
            if not re.match(r'^[\d\+\-\*\/\%\(\)\.\*\*]+$', expression):
                print("ERROR: Invalid characters in expression")#num only operation
                return
            
            result = eval(expression)
            self.last_result = result
            print(f"Result: {result}")#results
            
        except ZeroDivisionError:
            print("ERROR: Division by zero")
        except SyntaxError:
            print("ERROR: Invalid syntax")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def add(self, args):#add
        try:
            numbers = [float(x) for x in args.split()]
            if len(numbers) < 2:
                print("ERROR: Need at least 2 numbers")
                return
            result = sum(numbers)
            self.last_result = result
            print(f"Sum: {result}")
        except ValueError:
            print("ERROR: Invalid numbers")
    
    def subtract(self, args):#sub
        try:
            numbers = [float(x) for x in args.split()]
            if len(numbers) < 2:
                print("ERROR: Need at least 2 numbers")
                return
            result = numbers[0]
            for num in numbers[1:]:
                result -= num
            self.last_result = result
            print(f"Result: {result}")
        except ValueError:
            print("ERROR: Invalid numbers")
    
    def multiply(self, args):#mul
        try:
            numbers = [float(x) for x in args.split()]
            if len(numbers) < 2:
                print("ERROR: Need at least 2 numbers")
                return
            result = 1
            for num in numbers:
                result *= num
            self.last_result = result
            print(f"Product: {result}")
        except ValueError:
            print("ERROR: Invalid numbers")
    
    def divide(self, args):#div
        try:
            numbers = [float(x) for x in args.split()]
            if len(numbers) < 2:
                print("ERROR: Need at least 2 numbers")
                return
            result = numbers[0]
            for num in numbers[1:]:
                if num == 0:
                    print("ERROR: Division by zero")
                    return
                result /= num
            self.last_result = result
            print(f"Result: {result}")
        except ValueError:
            print("ERROR: Invalid numbers")
    
    def power(self, args):#power
        try:
            parts = args.split()
            if len(parts) != 2:
                print("ERROR: Use format 'pow <base> <exponent>'")
                return
            base = float(parts[0])
            exp = float(parts[1])
            result = base ** exp
            self.last_result = result
            print(f"Result: {result}")
        except ValueError:
            print("ERROR: Invalid numbers")
    
    def sqrt(self, args):#squareroots
        try:
            num = float(args.strip())
            if num < 0:
                print("ERROR: Cannot calculate square root of negative number")
                return
            result = math.sqrt(num)
            self.last_result = result
            print(f"Result: {result}")
        except ValueError:
            print("ERROR: Invalid number")
    
    def mod(self, args):#modulo
        try:
            parts = args.split()
            if len(parts) != 2:
                print("ERROR: Use format 'mod <number> <divisor>'")
                return
            num = float(parts[0])
            divisor = float(parts[1])
            if divisor == 0:
                print("ERROR: Division by zero")
                return
            result = num % divisor
            self.last_result = result
            print(f"Result: {result}")
        except ValueError:
            print("ERROR: Invalid numbers")
    
    def factorial(self, args):#factorial
        try:
            num = int(args.strip())
            if num < 0:
                print("ERROR: Factorial not defined for negative numbers")
                return
            if num > 170:
                print("ERROR: Number too large for factorial")
                return
            result = math.factorial(num)
            self.last_result = result
            print(f"Result: {result}")
        except ValueError:
            print("ERROR: Invalid number")
    
    def percentage(self, args):#percentage
        try:
            parts = args.split()
            if len(parts) != 2:
                print("ERROR: Use format 'percent <percentage> <of number>'")
                return
            percentage = float(parts[0])
            of_number = float(parts[1])
            result = (percentage / 100) * of_number
            self.last_result = result
            print(f"Result: {result} ({percentage}% of {of_number})")
        except ValueError:
            print("ERROR: Invalid numbers")
#soh cah toa nightmare-----
    def sin_calc(self, args):
        try:
            angle = float(args.strip())
            result = math.sin(math.radians(angle))
            self.last_result = result
            print(f"sin({angle}°) = {result}")
        except ValueError:
            print("ERROR: Invalid number")
    
    def cos_calc(self, args):
        try:
            angle = float(args.strip())
            result = math.cos(math.radians(angle))
            self.last_result = result
            print(f"cos({angle}°) = {result}")
        except ValueError:
            print("ERROR: Invalid number")
    
    def tan_calc(self, args):
        try:
            angle = float(args.strip())
            result = math.tan(math.radians(angle))
            self.last_result = result
            print(f"tan({angle}°) = {result}")
        except ValueError:
            print("ERROR: Invalid number")
#o(n)-----------------------------
    def log_calc(self, args):
        """Logarithm base 10: log 100"""
        try:
            num = float(args.strip())
            if num <= 0:
                print("ERROR: Logarithm undefined for non-positive numbers")
                return
            result = math.log10(num)
            self.last_result = result
            print(f"log10({num}) = {result}")
        except ValueError:
            print("ERROR: Invalid number")
    
    def ln_calc(self, args):
        """Natural logarithm: ln 2.718"""
        try:
            num = float(args.strip())
            if num <= 0:
                print("ERROR: Natural logarithm undefined for non-positive numbers")
                return
            result = math.log(num)
            self.last_result = result
            print(f"ln({num}) = {result}")
        except ValueError:
            print("ERROR: Invalid number")
    
    def abs_calc(self, args):
        try:
            num = float(args.strip())
            result = abs(num)
            self.last_result = result
            print(f"Result: {result}")
        except ValueError:
            print("ERROR: Invalid number")
    
    def round_calc(self, args):
        try:
            parts = args.split()
            num = float(parts[0])
            decimals = int(parts[1]) if len(parts) > 1 else 0
            result = round(num, decimals)
            self.last_result = result
            print(f"Result: {result}")
        except (ValueError, IndexError):
            print("ERROR: Use format 'round <number> <decimals>'")
#history------------------------
    def last(self):#history
        print(f"Last result: {self.last_result}")
    
    def mem_store(self):
        self.memory = self.last_result
        print(f"Stored {self.last_result} to memory")
    
    def mem_recall(self):
        print(f"Memory: {self.memory}")
    
    def mem_clear(self):
        self.memory = 0
        print("Memory cleared")
    
    def constants(self):
        """Show mathematical constants"""
        print("Mathematical Constants:")
        print(f"  π (pi)    = {math.pi}")
        print(f"  e         = {math.e}")
        print(f"  τ (tau)   = {math.tau}")
        print(f"  φ (phi)   = {(1 + math.sqrt(5)) / 2}")  # Golden ratio