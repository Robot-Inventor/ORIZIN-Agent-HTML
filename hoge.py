import otfdlib


right = otfdlib.Otfd()
right.load("resource/dictionary/capital_dictionary.otfd")
right.parse()
country_names = right.get_index_list()
new = otfdlib.Otfd()
new.load("resource/dictionary/language_dictionary.otfd")
new.parse()
new_name = new.get_index_list()
print(list(set(new_name) - set(country_names)))
