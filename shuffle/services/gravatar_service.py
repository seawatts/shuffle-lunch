import hashlib


class GravatarService:
    def __init__(self):
        pass

    @staticmethod
    def get_gravatar_link(email):
        email_hash = GravatarService.__get_gravatar_hash(email)
        return "http://www.gravatar.com/avatar/{0}.jpg?s=120".format(email_hash)

    @staticmethod
    def __get_gravatar_hash(email):
        undigested_hash = hashlib.md5()
        undigested_hash.update(email)
        digested_hash = undigested_hash.hexdigest()
        return digested_hash