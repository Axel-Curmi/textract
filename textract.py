import argparse
import re

abbreviation_table = {
    "e.g.,": "<ABBREV_EXAMPLE>"
}

def lookup_in_str(source: str, lookup: str, case_insensitive: bool = False):
    return (case_insensitive and lookup.lower() in source.lower()) or \
           (not case_insensitive and lookup in source)

def highlight_lookup(source: str, lookup: str, case_insensitive: bool = False):
    output = source
    if case_insensitive:
        output = output.replace(lookup.upper(),
                                f"\033[92m{lookup.upper()}\033[0m")
        output = output.replace(lookup.lower(),
                                f"\033[92m{lookup.lower()}\033[0m")
    else:
        output = output.replace(lookup, f"\033[92m{lookup}\033[0m")
    return output

def preprocess(source: str):
    output = source
    for abbreviation, tag in abbreviation_table.items():
        output = output.replace(abbreviation, tag)
    return output

def postprocess(source: str):
    output = source
    for abbreviation, tag in abbreviation_table.items():
        output = output.replace(tag, abbreviation)
    return output

argparser = argparse.ArgumentParser(description="RFC document text extractor")

# Positional arguments
argparser.add_argument("keyword", metavar="KEYWORD", type=str,
                       help="The keyword to look for")
argparser.add_argument("file", metavar="FILE", type=argparse.FileType("r"),
                       help="The text file to look into")

# Optional arguments
argparser.add_argument("-i", "--case-insensitive", default=False,
                       action="store_true",
                       help="Disable case sensitivity when searching")

args = argparser.parse_args()

found = 0
print(f"\033[94mExtracting sentence(s) with keyword: \"{args.keyword}\" " +
      f"({'case-insensitive' if args.case_insensitive else 'case-sensitive'})" +
      "\033[0m.")

content = args.file.read()
content = content.replace("   ", "") # RFC documents tend to have
                                     # 3-space indentation.

content = preprocess(content) # Pre-process document content

paragraphs = content.split("\n\n") # Extract paragraphs
for paragraph in paragraphs:
    paragraph = paragraph.replace("\n", " ")
    
    sentences = paragraph.split(".") # Extract sentences
    for sentence in sentences:
        sentence = sentence.strip()

        if lookup_in_str(sentence, args.keyword, args.case_insensitive):
            found += 1

            sentence = postprocess(sentence) # Post-process sentence
                                             # Undo pre-process (where required)
            output = highlight_lookup(sentence, args.keyword,
                                      args.case_insensitive)
            print(f"> {output}")

print(f"\033[94m{found} sentence(s) extracted.\033[0m")