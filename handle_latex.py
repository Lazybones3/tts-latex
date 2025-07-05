import re
import pysbd
import inflect


# Needed for inflect
import locale
locale.getpreferredencoding = lambda: "UTF-8"

# Conversion of numbers
p = inflect.engine()
def convert_numbers(matchobj):
    return p.number_to_words(matchobj.group(0))

# Abbreviations
# Inspired by https://github.com/coqui-ai/TTS/discussions/987
abbreviations = {
    "a": "ay",
    "b": "bee",
    "c": "sieh",
    "d": "dea",
    "e": "ee",
    "f": "eff",
    "g": "jie",
    "h": "edge",
    "i": "eye",
    "j": "jay",
    "k": "kaye",
    "l": "elle",
    "m": "emme",
    "n": "en",
    "o": "owe",
    "p": "pea",
    "q": "cue",
    "r": "are",
    "s": "esse",
    "t": "tea",
    "u": "hugh",
    "v": "vee",
    "w": "doub you",
    "x": "ex",
    "y": "why",
    "z": "zee"
}

isin = lambda l, s: any([li in s for li in l])


def abbreviation_preprocessor(text: str):
  # A bit of duplicate work because tts does this as well
  seg = pysbd.Segmenter(language="en", clean=True)
  sentences = seg.segment(text)
  for i in range(len(sentences)):
    words = sentences[i].split(" ")
    for j in range(len(words)):
      # Take the following for subsitition
      # All upper case
      has_period = words[j].rstrip(".") != words[j]
      words[j] = words[j].rstrip(".")
      check_1 = words[j].upper() == words[j]
      # All upper case plural
      check_2 = len(words[j])> 2 and words[j][:-1].upper() == words[j][:-1]
      # One letter
      check_3 = len(words[j]) == 1
      if check_1 or check_2 or check_3:
        words[j] = abbreviation_replacement(words[j])
      if has_period:
        words[j] += "."
    sentences[i] = " ".join(words)
  return " ".join(sentences)

def abbreviation_replacement(word: str):
  """Heuristic for abbreviations"""
  subwords = word.split("-")
  for i in range(len(subwords)):
    tokens = list(subwords[i])
    # Only spell out acronyms without middle vowels
    has_s = len(tokens)> 2 and tokens[-1] == "s"
    if has_s:
      tokens = tokens[:-1]
      subwords[i] = subwords[i][:-1]
    vowels = ["a", "e", "i", "o", "u"]
    check_1 = isin(vowels, subwords[i].lower())
    check_2 = len(tokens)> 0 and tokens[0].lower() not in vowels
    check_3 = len(tokens)> 0 and tokens[-1].lower() not in vowels
    if check_1 and check_2 and check_3:
      continue
    new_tokens = []
    for token in tokens:
      token = abbreviations.get(token.lower(), token)
      new_tokens.extend([token, " "])
    if has_s:
      new_tokens[-2] += "s"
    subwords[i] = "".join(new_tokens)
  return "".join(subwords)

def remove_symbol(text: str):
  for s in ["$", "\\", "{" ,"}", "#"]:
    text = text.replace(s, " ")
  return text

def replace_symbol(text: str):
  d = {
    "\%": " percent",
    "_": " sub ",
    "=": " equals ",
    "+": " plus ",
    "/": " or ",
    "^": " to the "
  }
  for k, v in d.items():
    # Percent symbols
    text = text.replace(k, v)
  return text

with open('input.txt','r',encoding = 'utf-8') as f:
  text = f.read()
smart_abbreviations = False

##### Pre-processing #####
# Clean up latex
# Strip latex citations and references
text = re.sub(r"\\cite\{[A-za-z\d,\s\-\_:]+\}", "", text)
text = re.sub(r"\\citep\{[A-za-z\d,\s\-\_:]+\}", "", text)
text = re.sub(r"\\ref\{[A-za-z\d,\s\-\_:]+\}", "", text)
# Split alphanumeric characters
pattern = r'(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])'
result = re.split(pattern, text)
text = " ".join(result)
# Convert numbers to words
text = re.sub(r"\d+(\.\d+)?", convert_numbers, text)

# Remove random latex symbols
text = remove_symbol(text)

text_with_abbrevs = replace_symbol(text)
if smart_abbreviations:
  text_final = abbreviation_preprocessor(text_with_abbrevs)
else:
  text_final = text_with_abbrevs

with open('output.txt', 'w', encoding = 'utf-8') as f:
  f.write(text_final)
