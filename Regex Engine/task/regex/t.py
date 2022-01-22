#from colorama import init, Fore  # disable before test as Jetbrains don't have it installed


import sys

sys.setrecursionlimit(50)
#init(autoreset=True)


only_beginning = False


# if len(template) < len(string) and template[-1] == "$", strip "$"!2

def string_scanner(_string, _template):
    if _template:
        if _template[0] in "*?+":
            print("REGEX PATERN ERROR. you can't have '*?+' at the beginning of the string\nTRY AGAIN")
            return main()
        if _template[0] == "^":
            _template = _template[1:]
            global only_beginning
            only_beginning = True

        if _template[-1] == "$":
            # try to play with index in _string that is following $ in template.
            if not char_match(_template[-2], _string[-1]):
                return "a", "b"  # temporarily fix to repr "FALSE"
    return _template, _string


def char_match(_regex_char, _char) -> bool:
    return any([not _regex_char, _regex_char == ".", _regex_char == _char])


def string_match(_template, _string):
    loop_range = len(_string)
    # print(f"checking {_template, _string}")

    for i in range(loop_range):
        #print("loop starts with:", _template, _string)
        try:
            if not char_match(_template[i], _string[i]):
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

                        return full_match(_template[i+2:], _string[i+1:])


                elif "?" in _template:
                    next_step = 1 if _template[i] == "?" else 2

                    # do not make it recursive
                    next_symbol_check = char_match(_template[i + next_step], _string[
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
                        return full_match(_template[i + next_step::], _string[i::])

                    elif _template[i - 1] == ".":
                        next_letter = _template[i + 1]
                        next_letter_index = _string.find(next_letter)

                        # removing repittive chars.
                        _string = _string[:i] + _string[next_letter_index]

                        _template = _template[i + 1::]
                        _string = _string[i + 1::]
                        # print(_template, _string)

                        return full_match(_template, _string)

                    elif _template[i + 1] == _string[i]:  # abscent letter case
                        """abscent letter case """
                        return full_match(_template[i + 1::], _string[i::])

                    elif _template[i + 1] == _string[i]:  # 0 repititions, (letter presented only once here)
                        """0 repititions"""
                        return full_match(_template[i + next_step::], _string[i::])

                elif "+" in _template:
                    # print(_template, _string)

                    if _template[i] == "+":


                        _template = _template[:i] + _template[i + 1:]

                        _string = _string[:i] + _string[i::].strip(_string[i - 1])  # right template version
                        i += 1

                        return string_match(_template, _string)
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


def template_without_optional_chars(_template):
    """ with good string match function this may not be needed"""

    symbols = {"*", "?", "$"}
    while any(["?" in _template, "*" in _template, "$" in _template]):
        for s in symbols:
            index = _template.find(s)
            if index != -1:
                _template = _template[:index - 1] + _template[index + 1:]
    return _template


def full_match(_template, _string):
    # if _template and not _string - checking if _template will still be True after removing optional characters.
    if _template and not _string:
        if template_without_optional_chars(_template):
            return False
        # if _template is bigger than _string - checking if that is that the case after removing optional characters.
        elif len(_template) > len(_string):
            if len(template_without_optional_chars(_template)) > len(_string):
                return False
    elif not _template:
        return True

    if string_match(_template, _string):
        return True

    elif only_beginning:
        return False

    else:
        i = 1
        # creating the loop and checking if template can be found in string
        while i < len(_string):

            if string_match(_template, _string[i:]):
                return True
            else:
                if len(_string[i]) < len(_template) and _string[i] == "$":
                    return True
                i += 1
        return False


def main():
    try:
        template, string = input().split("|")
    except ValueError:
        print("ERROR! Input should be like a|a. Please try again")
        return main()
    template, string = string_scanner(string, template)

    print(full_match(template, string))


def run_tests():
    # test input -> answer
    test_pool = {'\\?|Is this working?': True,
                 '\\.$|end.': True,
                 'colou?r|color': True,
                 'colou?r|colour': True,
                 'colou?r|colouur': False,
                 'colou*r|color': True,
                 'colou*r|colour': True,
                 'colou*r|colouur': True,
                 'col.*r|color': True,
                 'col.*r|colour': True,
                 'col.*r|colr': True,
                 'col.*r|collar': True,
                 'col.*r$|colors': False,
                 'colou+r|color': False,
                 'colo+r|color': True,
                 '^no+pe$|noooooooope': True,
                 '^apple$|apple pie': False,
                 '^.*c$|abcabc': True,
                 '3\\+3|3+3=6': True,
                 '\\|\\': True,
                 'colou\\?r|color': False,
                 'colou\\?r|colour': False,
                 'colou?rama|colorama': True,
                 }

    for pair in test_pool.keys():
        template, string = pair.split("|")
        template, string = string_scanner(string, template)
        # print(f"templ: {template}, str: {string}, expected result {test_pool[pair]}, actual result: {full_match(template, string)}")
        print(f"{pair} {Fore.GREEN}passed" if full_match(template, string) == test_pool[
            pair] else f"{pair} {Fore.RED}failed")


if __name__ == '__main__':
    main()
    #run_tests()


# from string match need to return to full match with recalculated index

# ^no+pe$ noooooooope great example to not allow recursion in full match in such cases.


# colou?rama|colorama

colou?r|xxxcolour

colou?r|xxxcolouur

^no+|noooooooope
