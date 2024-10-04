import re


def sanitize(string: str) -> str:
    # ~ Remove all non-alphanumeric characters
    string = re.sub("[^a-zA-Z0-9]+", "", string)
    return "".join(e for e in string if e.isalnum())


class MailingList:
    data = []

    def findStudent(firstname: str, lastname: str):
        lastname = sanitize(lastname.lower())
        firstname = sanitize(firstname.lower())

        for student in MailingList.data:
            sLastname = sanitize(student["lastname"].lower())
            sFirstname = sanitize(student["firstname"].lower())

            if lastname == sLastname and firstname == sFirstname:
                print(
                    "Found student (%s %s) in mailing list (%s %s)"
                    % (lastname, firstname, student["lastname"], student["firstname"])
                )
                return student

        return None

    def findStudentByEmail(email: str):
        for student in MailingList.data:
            if email == student["email"]:
                return student

        return None
