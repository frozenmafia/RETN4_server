

def convert_phone_string_phone(phone_text):
    x = phone_text.split(None,1)
    return {
        'country_code':int(x[0]),
        'phone_number':int(x[1].replace(" ",""))
    }

print(convert_phone_string_phone("+91 96679 43369"))
print(int("+9"))


