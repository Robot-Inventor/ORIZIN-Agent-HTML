import otfdlib


right = otfdlib.Otfd()
right.load("resource/dictionary/capital_dictionary.otfd")
right.parse()
country_names = right.get_index_list()
new = otfdlib.Otfd()
new.load("resource/dictionary/language_dictionary.otfd")
new.parse()
result = [f"{index}:{new.get_value(index)}" for index in country_names]
with open("resource/dictionary/language_dictionary.otfd", mode="w") as f:
    f.write("\n".join(result))
