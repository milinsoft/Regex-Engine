class RegexEngine:
    def __init__(self):
        pass

    @staticmethod
    def match(_template, _string) -> bool:
        if not _template:
            return True
        if not _string:
            return _template == "$" or (len(_template) == 2 and _template[1] in "*?")

        if _template[0] == "\\":
            if _template[1:2] != _string[0]:
                return False
            return RegexEngine.match(_template[2:], _string[1:])

        if _template[0] != _string[0] and _template[0] != ".":
            if _template[1:2] in {"?", "*"}:
                return RegexEngine.match(_template[2:], _string)
            return False

        match _template[1:2]:
            case "?":
                return RegexEngine.match(_template[2:], _string[1:])

            case "*":
                # _template[2:], _string assumes non repitive char or abscent (in case of "*")
                # _string[1:] keeps template and
                # moving _string to the right during each iteration to skip repitetive chars.
                return RegexEngine.match(_template, _string[1:]) or RegexEngine.match(_template[2:], _string)

            case "+":
                return RegexEngine.match(_template, _string[1:]) or RegexEngine.match(_template[2:], _string[1:])

        # if all none of the conditions triggered:
        return RegexEngine.match(_template[1:], _string[1:])

    @staticmethod
    def string_scanner(template, string) -> bool:
        if not template:
            return True

        if template[0] in "*?+":
            print("REGEX PATERN ERROR. you can't have '*?+' at the beginning of the string\nTRY AGAIN")
            return main()
        if template[0] == "^":
            return RegexEngine.match(template[1:], string)
        if RegexEngine.match(template, string):
            return True
        if not string:
            return template == "$"
        return RegexEngine.string_scanner(template, string[1:])


def main():
    try:
        print(RegexEngine.string_scanner(*input().split("|")))  # using asterisk for unpacking
    except ValueError:
        print("ERROR! Input should be like a|a. Please try again")
        return main()


if __name__ == '__main__':
    main()
