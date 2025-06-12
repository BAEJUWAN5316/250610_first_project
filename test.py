import re


a = "A@"

def search_str(data):
    if not re.search("@", data):
        return "@이게 없다 돌아가"
    
    if not re.search(r"[a-zA-Z]", data):
        return "영어 없다 돌아가"
    
    if not re.search(r"[0-9]", data):
        return "숫자 없다 돌아가"
    return "다 있다 최고"


print(search_str(a))
