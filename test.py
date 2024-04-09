import re
from client import *

# Fonction pour extraire toutes les chaînes qui suivent le symbole $
def extract_strings_with_dollar(data):

    # Fonction récursive pour parcourir les données
    def recurse_extract(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                recurse_extract(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse_extract(item)
        elif isinstance(obj, str):
            matches = re.findall(r'\$[^\s"]+', obj)
            if matches:
                print(matches)
                message = lecture(matches[0].replace('$', ''))

    recurse_extract(data)


# Exemple d'un JSON
data = {
    "protocol": "rdo",
    "operation": "POST",
    "data": {
        "fName": "testfName",
        "lName": "testlName",
        "courses": [
            "$rdo://192.168.56.1:8080/test",
            {
                "code": "6gin101-11",
                "time": "soir"
            },
            "$wrdo://192.168.56.1:8080/6gen723-03",
            "$exmaple"
        ]
    }
}

# Appel de la fonction pour extraire les chaînes
extract_strings_with_dollar(data)

