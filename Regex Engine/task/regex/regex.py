
class RegexEngine:

    def __init__(self, template, string):
        self.template = template
        self.string = string
        self.match_from_start = False

    def string_scanner(self):
        if self.template:
            if self.template[0] in "*?+":
                print("REGEX PATERN ERROR. you can't have '*?+' at the beginning of the string\nTRY AGAIN")
                return main()
            if self.template[0] == "^":
                self.template = self.template[1:]
                self.match_from_start = True

            if self.template[-1] == "$":
                # try to play with index in _string that is following $ in template.
                if not RegexEngine.char_match(self.template[-2], self.string[-1]):
                    return False

    @staticmethod
    def char_match(_regex_char, _char) -> bool:
        return any([not _regex_char, _regex_char == ".", _regex_char == _char])

    def substring_match(self, _template=None, _string=None):

        for i in range(len(_string)):
            match = True

            try:
                if not RegexEngine.char_match(_template[i], _string[i]):
                    match = False

                    if _template[i] == "$" and _string[i]:
                        return False

                    elif _template[i] == '\\':
                        return False if _template[i+1] != _string[i]\
                            else self.full_match(_template[i+2:], _string[i+1:])

                    elif "?" in _template:

                        if _template[i] == "?":
                            next_step = 1

                        elif len(_template) > i and _template[i+1] == "?":
                            next_step = 2
                        else:
                            return False

                        return self.substring_match(_template[i+next_step:], _string[i:])

                    elif "*" in _template:
                        next_step = 1 if _template[i] == "*" else 2
                        """repeative letter case"""
                        if _template[i - 1] == _string[i]:  # repeative letter case
                            _string = _string[:i] + _string[i::].strip(_template[i - 1])  # cut repittive leters in _string
                            _template = _template[:i] + _template[i + next_step::]
                            return self.full_match(_string, _template)

                        elif _template[i - 1] == ".":
                            next_letter_index = _string.find(_template[i + 1])

                            # removing repittive chars.
                            _string = _string[:i] + _string[next_letter_index]
                            return self.full_match(_template, _string)

                        elif _template[i + 1] == _string[i]:  # abscent letter case
                            """abscent letter case """
                            # re-write variables?
                            return self.full_match(_template[i + 1::], _string[i::])

                        elif _template[i + 1] == _string[i]:  # 0 repititions, (letter presented only once here)
                            """0 repititions"""
                            return self.full_match(_template[i + next_step::], _string[i::])

                    elif _template[i] == "+":
                        _template = _template.replace("+", "")
                        _string = _string[:i] + _string[i::].strip(_string[i - 1])  # right template version
                        return self.full_match(_template, _string)
                    return False
            except IndexError:

                return match
        # in case all letters passed without any interventions
        return True

    def template_without_optional_chars(self, _template):
        """ with good string match function this may not be needed"""
        if not _template:
            _template = self.template

        symbols = {"*", "?", "$"}
        while any(["?" in _template, "*" in _template, "$" in _template]):
            for s in symbols:
                index = _template.find(s)
                if index != -1:
                    _template = _template[:index - 1] + _template[index + 1:]
        return _template

    def full_match(self, _template=None, _string=None):

        # if _template and not _string - checking if _template will still be True after removing optional characters.
        if _template and not _string:
            if self.template_without_optional_chars(_template):
                return False
            # if _template is bigger than _string - checking if that is that the case after removing optional characters.
            elif len(_template) > len(_string):
                if len(self.template_without_optional_chars(_template)) > len(_string):
                    return False
        elif not _template:
            return True

        if self.substring_match(_template, _string):
            return True

        elif self.match_from_start:
            return False

        else:
            i = 1
            # creating the loop and checking if template can be found in string
            while i < len(_string):
                if self.substring_match(_template, _string[i:]):
                    return True
                i += 1
            return False


def main():
    try:
        template, string = input().split("|")
        #template, string = "^no+|noooooooope".split("|")
    except ValueError:
        print("ERROR! Input should be like a|a. Please try again")
        return main()

    match_case = RegexEngine(template, string)
    match_case.string_scanner()
    print(match_case.full_match(match_case.template, match_case.string))


if __name__ == '__main__':
    main()
