"""
Some common helper functions for the App.
"""
import re
def convert_special_german_accents_into_ascii(string):
    """
    Conversion of german special accents to english
    """
    return re.sub("ß", "ss",
                  re.sub("Ä", "a",
                         re.sub("ä", "a",
                                re.sub("Ö", "o",
                                       re.sub("ö", "o",
                                              re.sub("Ü", "u",
                                                     re.sub("ü", "u", string)))))))

def uniques(some_list):
       """
       Get unique values of a list
       """
       new_list = []
       for item in some_list:
              if item not in new_list:
                     new_list.append(item)
       return new_list

def list_to_line(alist):
       items = ""
       for item in alist:
              items = item + " " + item + ","
              
if __name__ == '__main__':
    print(convert_special_german_accents_into_ascii("münich"))
    