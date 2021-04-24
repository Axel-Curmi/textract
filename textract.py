import argparse
import re

argparser = argparse.ArgumentParser(description="RFC document text extractor")

# Positional arguments
argparser.add_argument("keyword", metavar="KEYWORD", type=str,
                       help="The keyword to look for")
argparser.add_argument("file", metavar="FILE", type=argparse.FileType("r"),
                       help="The text file to look into")

# Optional arguments
argparser.add_argument("--case-sensitive", default=False, action="store_true",
                       help="Enable case sensitivity when searching")

args = argparser.parse_args()

content = args.file.read()
content = content.replace("   ", "") # RFC documents tend to have
                                     # 3-space indentation.

# Find all keywords and obtain line numbers
all_keyword_line_numbers = []

args.file.seek(0) # Move to the beginning of the file
for num, line in enumerate(args.file, 1):
    if (args.case_sensitive and args.keyword in line) or \
       (not args.case_sensitive and (args.keyword.upper() in line) or \
                                    (args.keyword.lower() in line)):
        all_keyword_line_numbers.append(num)

# Find all sentences containing the keyword
all_sentence_line_numers = []

pattern = f'(?:["(]*(?:\w|[<>=.\'])+[:;",)]*\s)*["(]*{args.keyword}[;",)]*(?:\s?["(]*(?:\w|[<>=.\'-])+[:;",)]*)*'
sentence_regex = re.compile(pattern,
                            0 if args.case_sensitive else re.IGNORECASE)

for sentence in sentence_regex.findall(content):
    # Obtain the line number of the sentence (if possible)
    sentence_line_numbers = []

    for lookup in sentence.split("\n"):
        if (args.case_sensitive and args.keyword not in lookup) or \
                (not args.case_sensitive and \
                 args.keyword.upper() not in lookup and \
                 args.keyword.lower() not in lookup):
            continue

        args.file.seek(0) # Move to the beginning of the file
        for num, line in enumerate(args.file, 1):
            if lookup in line:
                sentence_line_numbers.append(num)
                all_sentence_line_numers.append(num)
                break

    sentence = sentence.replace("\n", " ")

    # Highlight the keyword
    if args.case_sensitive:
        sentence = sentence.replace(args.keyword,
                                    f"\033[92m{args.keyword}\033[0m")
    else:
        sentence = sentence.replace(args.keyword.upper(),
                                    f"\033[92m{args.keyword.upper()}\033[0m")
        sentence = sentence.replace(args.keyword.lower(),
                                    f"\033[92m{args.keyword.lower()}\033[0m")

    print("{} > {}".format(sentence_line_numbers, sentence))

not_found_line_numbers = [ i for i in all_keyword_line_numbers \
                           if i not in all_sentence_line_numers ]
print(f"Line numbers missing containg keyword: {not_found_line_numbers}")
