import sys
from parser import is_likely_name

names = [
    "Engage with us", 
    "News and Events",
    "John Doe",
    "Prof. Jane Smith-Jones",
    "Stavros Papadopoulos",
    "Dr Élodie Martin",
    "Mr. O'Connor",
    "Department of Physics",
    "X. Y. Zheng",
    "Computer Science"
]

for n in names:
    print(f"'{n}' -> {is_likely_name(n)}")
