from parser import is_phd_or_postdoc

texts = [
    "John is a PhD Student in the Computer Science department.",
    "Jane is a Fellow researcher.",
    "Dr. Smith is a Professor of Economics and a former Postdoc.",
    "Alice is a Lecturer and Doctoral Researcher.",
    "Bob is a research fellow studying Mathematics."
]

for t in texts:
    print(f"'{t}' -> {is_phd_or_postdoc(t)}")
