import warnings


class PropertiesException(Exception):
    """
    used to raise exceptions related to properties.

    """

    def __init__(self, properties, datamap):
        self.properties = properties
        self.datamap = datamap

    def __str__(self):
        return f"the {self.properties} properties dont exist for the {self.datamap}"


class ParameterWarning(Warning):
    """
    used to raise warnings related to parameters.

    :cvar ORDER_WARNING_MESSAGE: a warning message for incorrect use of "order" parameter.
    :type ORDER_WARNING_MESSAGE: str


    :cvar COUNT_WARNING_MESSAGE: a warning message for incorrect use of "count" parameter.
    :type COUNT_WARNING_MESSAGE: str

    :cvar TIME_WARNING_MESSAGE: a warning message for when timestamp is given in seconds
    :type TIME_WARNING_MESSAGE: str

        :cvar TIME_WARNING_MESSAGE: a warning message for when start_timestamp input is 0 in account analysis.
    :type TIME_WARNING_MESSAGE: str

    """

    COUNT_WARNING_MESSAGE = "when both start and end time are specified this parameter is ignored"
    ORDER_WARNING_MESSAGE = "when only one of the start or end time are specified this parameter is ignored" + \
                            "\n" + "only start specified : ASC" + "\n" + "only end specified : DESC"
    TIME_WARNING_MESSAGE = "timestamps should be in milliseconds."
    START_TIME_ACCOUNT_ANALYSIS_WARNING = "when start timestamp is less than 1 tronscan " \
                                          "only returns 100 items. try start_timestamp = 1 to get all the data."

    def __init__(self, message, parameter):
        self.message = message
        self.parameter = str(parameter)

    def __str__(self):
        return self.parameter + " : " + self.message

    def warn(self):
        warnings.warn(self)


class ParameterException(Exception):
    """
    used to raise exceptions related to parameters.


    :cvar ORDER_EXCEPTION_MESSAGE: an error message for incorrect use of "order" parameter.
    :type ORDER_EXCEPTION_MESSAGE: str

    :cvar TIME_EXCEPTION_BIGGER_MESSAGE: an error message for incorrect use
                                    of "start_timestamp" or "end_timestamp" parameters.
    :type TIME_EXCEPTION_BIGGER_MESSAGE: str

    :cvar TIME_EXCEPTION_NEGATIVE_MESSAGE: an error message for incorrect use
                                    of "start_timestamp" or "end_timestamp" parameters.
    :type TIME_EXCEPTION_NEGATIVE_MESSAGE: str

    :cvar SORT_EXCEPTION_MESSAGE: an error message for incorrect use
                                    of "start_timestamp" or "end_timestamp" parameters.
    :type SORT_EXCEPTION_MESSAGE: str
    """

    ORDER_EXCEPTION_MESSAGE = 'order can only be one of two values : "ASC" or "DESC"'
    COUNT_EXCEPTION_MESSAGE = "this parameter must be positive"
    SORT_EXCEPTION_MESSAGE = "the specified value is not defined for this parameter" \
                             ", please check the docs for more info."
    TIME_EXCEPTION_BIGGER_MESSAGE = "start time cant be bigger than end time"
    TIME_EXCEPTION_NEGATIVE_MESSAGE = "timestamps cant be negative"
    SR_TYPE_EXCEPTION_MESSAGE = 'sr type can only be one of these values : "all", "sr", "sr_partner", "sr_candidate"'

    def __init__(self, message, parameter):
        self.message = message
        self.parameter = str(parameter)

    def __str__(self):
        return self.parameter + " : " + self.message
