from my_awesome_project.utils.core import CoreUtil


def get_short_uuid():
    return CoreUtil.generate_short_uuid()


def get_uuid():
    return CoreUtil.generate_uuid()
