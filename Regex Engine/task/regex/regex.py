import sys
from colorama import init, Fore

init(autoreset=True)


sys.setrecursionlimit(50)


def metachar_preprocessing(_string, _template):
    if _template:
        if _template[0] in "*?+":
            print("REGEX PATERN ERROR. you can't have '*?+' at the beginning of the string\nTRY AGAIN")
            return main()
        if _template[0] == "^":
            _template = _template[1:]
            _string = _string[:len(_template)]
        if _template[-1] == "$":
            if not char_match(_template[-2], _string[-1]):
                return "a", "b"  # temporarily fix to repr "FALSE"
            else:
                _template = _template[:-1]
                _string = _string[-len(_template):]
    return _template, _string


def char_match(_regex_char, _char) -> bool:
    return any([not _regex_char, _regex_char == ".", _regex_char == _char])


def string_match(_template, _string):
    loop_range = min([len(_template), len(_string)])
    # print(f"checking {_template, _string}")

    for i in range(loop_range):
        try:
            if not char_match(_template[i], _string[i]):
                #print(f"line #36: {_template[i]} doesn't match {_string[i]}\n")

                if "?" in _template:
                    next_step = 1 if _template[i] == "?" else 2

                    # do not make it recursive
                    next_symbol_check = char_match(_template[i + next_step], _string[i])  # skipping '?' and comparing next mandatory sign, test 'ca?t|cat'
                    if not next_symbol_check:  # problem  that this variable doesn't change it's name
                        return False
                    i += 1
                    if i == loop_range:
                        return True

                    # return full_match(_template[i + next_step::], _string[i::])

                # maybe rethink next_symbol check and inplement below as well?
                if "*" in _template:
                    next_step = 1 if _template[i] == "*" else 2
                    """repeative letter case"""
                    if _template[i-1] == _string[i]:  # repeative letter case
                        _string = _string[:i] + _string[i::].strip(_template[i-1])  # cut repittive leters in _string
                        return full_match(_template[i + next_step::], _string[i::])

                    elif _template[i-1] == ".":
                        # removing repittive chars.
                        _string = _string[:i+1] + _string[i+1::].strip(_string[i])

                        _template = _template[i+1::]
                        _string = _string[i+1::]


                        return string_match(_template, _string)

                    elif _template[i+1] == _string[i]:  # abscent letter case
                        return full_match(_template[i+1::], _string[i::])


                    elif _template[i+1] == _string[i]:  # 0 repititions, (letter presented only once here)
                        return full_match(_template[i + next_step::], _string[i::])

                    i += 1
                else:  # in none of IFs triggered
                    return False

        except IndexError:
            return _template[i] == _template[-1] == '?'  # should be True :)
    return True


def template_without_optional_chars(_template):
    symbols = {"*", "?"}
    while any(["?" in _template, "*" in _template]):
        for s in symbols:
            index = _template.find(s)
            if index != -1:
                _template = _template[:index - 1] + _template[index + 1:]
    return _template


def full_match(_template, _string, i=0):
    # if _template and not _string - checking if _template will still be True after removing optional characters.
    if _template and not _string:
        if template_without_optional_chars(_template):
            return False
        # if _template is bigger than _string - checking if that is taht case after removing optional characters.
        elif len(_template) > len(_string):
            if len(template_without_optional_chars(_template)) > len(_string):
                return False
    elif not _template:
        return True


    if string_match(_template, _string):
        return True

    else:

        i = 1
        # creating the loop and checking if template can be found in string
        while i < len(_string):

            if string_match(_template, _string[i:]):
                return True
            i += 1
        return False


def main():

    try:
        #template, string = input().split("|")
        template, string = "colou?r|colouur".split("|")
    except ValueError:
        print("ERROR! Input should be like a|a. Please try again")
        return main()
    template, string = metachar_preprocessing(string, template)
    print(full_match(template, string))


def run_tests():
    # test input -> answer
    test_pool = {'colou?r|color': True,
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
                 }

    for pair in test_pool.keys():
        template, string = pair.split("|")
        template, string = metachar_preprocessing(string, template)
        # print(f"templ: {template}, str: {string}, expected result {test_pool[pair]}, actual result: {full_match(template, string)}")
        print(f"{pair} {Fore.GREEN}passed" if full_match(template, string) == test_pool[pair] else f"{pair} {Fore.RED}failed")


if __name__ == '__main__':
    #main()
    run_tests()
