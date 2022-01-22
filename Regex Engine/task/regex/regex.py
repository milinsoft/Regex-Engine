
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

    def string_match(self, _template=None, _string=None):

        if not _template or not _string:
            _template = self.template
            _string = self.string

        # print(_template, _string)
            
        loop_range = len(_string)
        # print(f"checking {_template, _string}")
    
        for i in range(loop_range):
            # print("loop starts with:", _template, _string)
            try:
                if not RegexEngine.char_match(_template[i], _string[i]):
                    if _template[i] == '\\':
    
                        if _template[i+1] != _string[i]:
                            return False
                        else:
                            try:
                                _template[i + 1 + 1]
                            except IndexError:
                                return True
    
                            if _template[i+2] == "$" or len(_template[i+1]) == i+1:
                                return True
                            return self.full_match(_template[i+2:], _string[i+1:])

                    elif "?" in _template:
                        next_step = 1 if _template[i] == "?" else 2
    
                        # do not make it recursive
                        next_symbol_check = self.char_match(_template[i + next_step], _string[
                            i])  # skipping '?' and comparing next mandatory sign, test 'ca?t|cat'
                        if not next_symbol_check:  # problem  that this variable doesn't change it's name
                            return False
                        i += 1
                        if i == loop_range:
                            return True
    
                    # maybe rethink next_symbol check and inplement below as well?
                    elif "*" in _template:
    
                        next_step = 1 if _template[i] == "*" else 2
                        """repeative letter case"""
                        if _template[i - 1] == _string[i]:  # repeative letter case
                            _string = _string[:i] + _string[i::].strip(_template[i - 1])  # cut repittive leters in _string
                            return self.full_match(_template[i + next_step::], _string[i::])
    
                        elif _template[i - 1] == ".":
                            next_letter = _template[i + 1]
                            next_letter_index = _string.find(next_letter)
    
                            # removing repittive chars.
                            _string = _string[:i] + _string[next_letter_index]
    
                            _template = _template[i + 1::]
                            _string = _string[i + 1::]
                            # print(_template, _string)
    
                            return self.full_match(_template, _string)
    
                        elif _template[i + 1] == _string[i]:  # abscent letter case
                            """abscent letter case """
                            return self.full_match(_template[i + 1::], _string[i::])
    
                        elif _template[i + 1] == _string[i]:  # 0 repititions, (letter presented only once here)
                            """0 repititions"""
                            return self.full_match(_template[i + next_step::], _string[i::])
    
                    elif "+" in _template:
                        # print(_template, _string)
    
                        if _template[i] == "+":
                            _template = _template[:i] + _template[i + 1:]
    
                            _string = _string[:i] + _string[i::].strip(_string[i - 1])  # right template version
                            i += 1
    
                            return self.string_match(_template, _string)
                        return False
    
                    elif _template[i] == '$' and not _string:
                        return False
    
                    else:  # in none of IFs triggered
                        return False
            except IndexError:
                return _template[i] == _template[-1] == '?'  # should be True :)
            else:
                if i == len(_template) - 1:
                    return True
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
        if not _template or not _string:
            _template, _string =\
                self.template, self.string
            
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
    
        if self.string_match(_template, _string):
            return True
    
        elif self.match_from_start:
            return False
    
        else:
            i = 1
            # creating the loop and checking if template can be found in string
            while i < len(_string):
                if self.string_match(_template, _string[i:]):
                    return True
                else:
                    if len(_string[i]) < len(_template) and _string[i] == "$":
                        return True
                    i += 1
            return False


def main():
    try:
        # template, string = "^app|apple".split("|")
        template, string = input().split("|")
    except ValueError:
        print("ERROR! Input should be like a|a. Please try again")
        return main()

    match_case = RegexEngine(template, string)
    match_case.string_scanner()

    print(match_case.full_match())


if __name__ == '__main__':
    main()

# from string match need to return to full match with recalculated index

# ^no+pe$ noooooooope great example to not allow recursion in full match in such cases.
