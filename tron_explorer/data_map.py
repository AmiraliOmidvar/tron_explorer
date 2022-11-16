from json import dumps

from tron_explorer.exceptions import PropertiesException


class DataMap:
    """
    an abstract class that is super of data instances map. this type of class is responsible for filtering properties of
    data instances.

    :param data: The data instance.
    :type data: dict

    :param properties: properties of instance that will be returned.
    :type properties: list

    """

    def __init__(self, data: dict, properties: list):
        self.CLASS_NAME = None
        if type(self) is DataMap:
            raise NotImplementedError('abstract class cannot be initiated')
        else:
            self.data = data
            self.properties = properties
            self.filter_data()

            del self.data
            del self.properties
            try:
                del self.properties_list
                del self.properties_dict
            except AttributeError:
                pass
            del self.CLASS_NAME


    def check_properties(self):
        properties = self.properties
        if properties is None:
            properties_to_get = self.properties_list
            return properties_to_get
        else:
            differences = set(properties).difference(set(self.properties_list))
            if len(differences) == 0:
                return properties
            else:
                raise PropertiesException(differences, self.CLASS_NAME)

    def filter_data(self):
        """
        filters data based on specified properties. this method will be overridden in child classes

        """
        pass

    def get_dict(self):
        """
        :returns: dict representation of object.
        :rtype:  dict

        """
        return self.__dict__

    def __str__(self):
        return dumps(self.__dict__)
