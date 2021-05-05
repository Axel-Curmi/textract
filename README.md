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
> All documents related to the SSH protocols shall use the keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" to describe requirements
> Lorem ipsum dolor sit amet, consectetur adipiscing elit
> Morbi ornare massa urna, sed volutpat enim scelerisque et.
> Aenean quis lacinia felis.
4 sentence(s) extracted.
```
