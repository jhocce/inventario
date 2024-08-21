import os

from django.conf import settings


PATH_FULL=os.environ.get("PATH_FULL")
PRIVATE_BACK_URL=os.environ.get("PRIVATE_BACK_URL")
PUBLIC_BACK_URL=os.environ.get("PUBLIC_BACK_URL")

separador = os.path.sep
# dir_actual = os.path.dirname(os.path.abspath(__file__))
# dir = separador.join(dir_actual.split(separador)[:-1])
# print("---",dir)
# print(PUBLIC_BACK_URL)

def get_public_key():

    if PATH_FULL == '0':
        return settings.BASE_DIR + separador + PUBLIC_BACK_URL
def get_private_key():

    if PATH_FULL == '0':
        print(settings.BASE_DIR + separador + PRIVATE_BACK_URL)
        return settings.BASE_DIR + separador + PRIVATE_BACK_URL


# if __name__ == "__main__":
#     get_public_key()