import logging
from rest_framework import serializers
from rest_framework.fields import empty


class SerializerValidationError(Exception):
    def __init__(self, id=None, field=None, code=None, errors=None):
        if errors is not None:
            self.errors = errors
            self.field = next(iter(errors))
            print("error: ", errors)
            self.code = errors[self.field][0].code
        else:
            self.field = field
            self.code = code


class CustomModelSerializer(serializers.ModelSerializer):
    # def __init__(self, instance=None, data=empty, **kwargs):
    #     super().__init__(instance=None, data=empty, **kwargs)
    #     self.id = instance.id

    def is_valid(self, raise_exception=True):
        logger = logging.getLogger(__name__)
        valid = super().is_valid()
        # print(valid)
        if not valid and raise_exception:
            # print("type 2: ", type(self.errors))
            raise SerializerValidationError(errors=self.errors)
        return valid
