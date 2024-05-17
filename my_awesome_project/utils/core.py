import uuid


class CoreUtil:
    @staticmethod
    def generate_short_uuid():
        return str(uuid.uuid4()).replace("-", "")[:10].upper()

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())
