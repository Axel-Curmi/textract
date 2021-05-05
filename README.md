# textract
Extract sentences containing a specific keyword from text documents

## Usage
```
usage: textract.py [-h] [-i] KEYWORD FILE

RFC document text extractor

positional arguments:
  KEYWORD           The keyword to look for
  FILE              The text file to look into

optional arguments:
  -h, --help            show this help message and exit
  -i, --case-insensitive
                        Disable case sensitivity when searching
```

## Sample output
```
$ python3 textract.py MUST rfcdoc.txt

Extracting sentence(s) with keyword: "MUST" (case-sensitive).
> Names are case-sensitive, and MUST NOT be longer than 64 characters
> They MUST have only a single at-sign in them
> For this reason, it must be emphasized that peers MUST rekey before a wrap of the sequence numbers
> In any event, where local security policy for the server host exists, it MUST be applied and enforced correctly
4 sentence(s) extracted.
```
