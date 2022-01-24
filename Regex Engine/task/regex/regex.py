def match(_template, _string) -> bool:
    """ [1:2] is used instead of [1] to avoid exception when getting out of the given boundaries.
    for example word = 'a', word[1] -> IndexError, word[1:2] -> ' ' """

    # empty cases check
    if not _template:
        return True
    if not _string:
        return _template == "$" or (len(_template) == 2 and _template[1] in "*?")

    """ escaping symbol check """
    if _template[0] == "\\":
        if _template[1:2] != _string[0]:
            return False
        return match(_template[2:], _string[1:])

    if _template[0] != _string[0] and _template[0] != ".":
        if _template[1:2] in {"?", "*"}:
            return match(_template[2:], _string)
        return False

    match _template[1:2]:
        case "?":
            return match(_template[2:], _string[1:])

        case "*":
            """ _template[2:], _string assumes non repitive char or abscent (in case of "*")
            _string[1:] keeps template and
            moving _string to the right during each iteration to skip repitetive chars. """
            return match(_template, _string[1:]) or match(_template[2:], _string)

        case "+":
            return match(_template, _string[1:]) or match(_template[2:], _string[1:])

    # if all none of the conditions triggered that means that _template[0] == _string[0]
    return match(_template[1:], _string[1:])


def string_scanner(template, string) -> bool:
    if not template:
        return True

    if template[0] in "*?+":
        print("REGEX PATERN ERROR. you can't have '*?+' at the beginning of the string\nTRY AGAIN")
        return main()
    if template[0] == "^":
        return match(template[1:], string)
    if match(template, string):
        return True
    if not string:
        return template == "$"
    return string_scanner(template, string[1:])


def main():
    try:
        print(string_scanner(*input().split("|")))  # using asterisk for unpacking
    except ValueError:
        print("ERROR! Input should be like a|a. Please try again")
        return main()


if __name__ == '__main__':
    main()
