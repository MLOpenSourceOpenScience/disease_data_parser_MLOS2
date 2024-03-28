import re

def searching(pattern, text):
    match = re.search(pattern, text)

    if match:
        # Extract day, month, and year from the matched groups
        day = match.group(2)
        month = match.group(3)
        year = match.group(4)

        return day, month, year

pattern = r'(?s:.*)\b(\d{1,2})\s*(?:st|nd|rd|th)\s*\w{0,4}?\s*[-–—]+\s*(\d{1,2})\s*(?:st|nd|rd|th)?\s*(\w+)\s*(\d{4})?\s*\('
pattern_year = r'(?s:.*)\b(\d{1,2})\s*(?:st|nd|rd|th)\s*\w{0,4}?[-–—]+\s*(\d{1,2})\s*(?:st|nd|rd|th)?\s*(\w+)\s*(\d{4})'


given1 = '08th- 14th  July 2023  (28th Week)'
given2 = '27thJuly – 02nd August (31st Week)'
given3 = '03rd – 09th August 2013 '
given4 = '31st August – 06th September (36th Week)'
given5 = '07th  – 13th September 2013 '

# print(searching(pattern, given1))
# print(searching(pattern, given2))
# print(searching(pattern_year, given3))

print(searching(pattern, given4))
print(searching(pattern_year, given5))
