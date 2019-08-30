from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    """ Implement lines in such a way that, given two strings, a and b, it returns a list of the lines that are, identically, in both a and b.
    The list should not contain any duplicates. Assume that lines in a and b will be be separated by \n, but the strings in the
    returned list should not end in \n. If both a and b contain one or more blank lines (i.e., a \n immediately preceded by no other characters),
    the returned list should include an empty string (i.e., "").  """
    # TODO
    lines_a = a.splitlines()
    lines_b = b.splitlines()

    lines_a_set = set()
    lines_b_set = set()

    for line in lines_a:
        lines_a_set.add(line.rstrip("\n"))

    for line in lines_b:
        lines_b_set.add(line.rstrip("\n"))

    line_list = [] # initilize list for list of identical lines

    for line in lines_a_set:
        if line in lines_b_set:
            line_list.append(line.rstrip("\n"))



    #print(lines_a, lines_b)
    #print(lines_a_set, lines_b_set)
    #print()
    #print(line_list)
    return line_list


def sentences(a, b):
    """Return sentences in both a and b"""

    """ Implement sentences in such a way that, given two strings, a and b, it returns a list of the unique English sentences that are, identically,
    present in both a and b. The list should not contain any duplicates.
    Use sent_tokenize from the Natural Language Toolkit to "tokenize" (i.e., separate)
    each string into a list of sentences. It can be imported with: from nltk.tokenize import sent_tokenize
    Per its documentation, sent_tokenize, given a str as input, returns a list of English sentences therein.
    It assumes that its input is indeed English text (and not, e.g., code, which might coincidentally have periods too). """

    # TODO
    sentence_a = sent_tokenize(a)
    sentence_b = sent_tokenize(b)

    sentence_a_set = set()
    sentence_b_set = set()

    for sentence in sentence_a:
        sentence_a_set.add(sentence.rstrip("\n"))

    for sentence in sentence_b:
        sentence_b_set.add(sentence.rstrip("\n"))


    sentence_list = [] # initilize list for list of identical sentences

    for sentence in sentence_a_set:
        if sentence in sentence_b_set:
            sentence_list.append(sentence.rstrip("\n"))

    print(sentence_a)
    print(sentence_b)
    print(sentence_a_set)
    print(sentence_b_set)
    print(sentence_list)
    return sentence_list


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    """ Implement substrings in such a way that, given two strings, a and b, and an integer, n, it returns a list of all substrings of length n that are,
    identically, present in both a and b. The list should not contain any duplicates.

    Recall that a substring of length n of some string is just a sequence of n characters from that string.
    For instance, if n is 2 and the string is Yale, there are three possible substrings of length 2: Ya, al, and le.
    Meanwhile, if n is 1 and the string is Harvard, there are seven possible substrings of length 1: H, a, r, v, a, r, and d.
    But once we eliminate duplicates, there are only five unique substrings: H, a, r, v, and d. """

    # TODO
    # split each string into all substrings of length n
    # first extract all substrings for each string a and b
    # can use s[i:j] returns substring of s form index i to (but not inclduing) index j
    #maybe write a helpr fucntion that can take a string  and get you all of the sub strings of length n

    sub_string_list = []
    sub_string_b = []

    substring_a_set = set()
    substring_b_set = set()

    range1 = 0
    range2 = n

    for sub_string in a:
        length = len(a)
        string = a[range1:range2]
        range1 = range1 + 1
        range2 = range2 + 1
        if range2 < len(a):
            substring_a_set.add(string.rstrip("\n"))


    print(substring_a_set)

    x = substr(a, n)
    y = substr(b, n)

    for substring in x:
        if substring in y:
            sub_string_list.append(substring.rstrip("\n"))



    print(x)
    print(y)
    print()
    print(sub_string_list)

    return sub_string_list

def substr(a, n):


    substring_a_set = set()

    range1 = 0
    range2 = n

    for sub_string in a:
        length = len(a)
        string = a[range1:range2]
        range1 = range1 + 1
        range2 = range2 + 1
        if range2 < len(a):
            substring_a_set.add(string.rstrip("\n"))

    return substring_a_set