def read_txt(filepath) -> list:
    with open(filepath, "r") as reader:
        return [int(line.replace("\n", "")) for line in reader.readlines() if not line.startswith("#")]

def factorial(n):
    result = 1
    for i in range(1, n+1):
        result = result * i
    return result

is_prime_number = lambda n: factorial(n-1) % n == n-1

real_prime_numbers = read_txt("echte_primzahlen.txt")
fake_prime_numbers = read_txt("fake_primzahlen.txt")

if False:
    for pn in real_prime_numbers:
        print(f"{pn} is prime number: {is_prime_number(pn)}")

if True:
    for pn in fake_prime_numbers:
        print(f"{pn} is prime number: {is_prime_number(pn)}")

