class APIMandatoryFieldList(object):
    field_list = {
        'post': ['email', 'title', 'story'],
        'id': ['id'],
    }

    @staticmethod
    def get_mandatory_field_list(key):
        try:
            return APIMandatoryFieldList.field_list[key]
        except AttributeError:
            return None
