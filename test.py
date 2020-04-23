import re


def is_valid_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True if '.ac.ke' in email or '.edu' in email else False
    return False


print(is_valid_email('students@pacuniversity.ac.ke'))








