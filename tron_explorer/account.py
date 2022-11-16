from pandas import DataFrame
from tron_explorer.data_map import DataMap

# noinspection PyAttributeOutsideInit
from tron_explorer.exceptions import ParameterException, ParameterWarning
from tron_explorer.utils import SendRequestSingle, SendRequestMultiple


# noinspection PyAttributeOutsideInit
class AccountDataMap(DataMap):
    properties_dict = {"address": "address", "address_tag": "addressTag", "balance": "balance"
        , "power": "power", "number_of_transactions": "totalTransactionCount"
        , "latest_operation_time": "latestOperationTime"}

    """
    a DataMap type class that is responsible for filtering properties of account data instances.

    :param data: the data instance.
    :type data: dict

    :param properties: properties of account instance that will be returned. to see what properties are included see below
    :type properties: list

    :properties:

        * *address* (``str``)
            address of the account.
        * *address_tag* (``str``)
            name of the account.
        * *balance* (``int``)
            balance of the account (trx).
        * *power* (``int``)
            amount of votes that this account has.
        * *total_transactions* (``int``)
            number of transaction related to the account.
        * *latest_operation_time* (``int``)
            timestamp of last operation the account has performed.
    """

    def __init__(self, data: dict, properties: list):
        super().__init__(data, properties)

    def filter_data(self):

        """
        filters data based on parameter properties.
        """

        self.CLASS_NAME = "Account"
        self.properties_list = self.properties_dict.keys()

        super().filter_data()
        data = self.data
        properties = self.check_properties()

        for p in properties:
            try:
                setattr(self, p, data[self.properties_dict[p]])
            except KeyError:
                setattr(self, p , None)


# noinspection PyIncorrectDocstring
class Account:
    """
    instantiate an object that contains a methods for multiple request related to accounts.
    """

    _API_ACCOUNT_ADDRESS = "/account/list"
    _API_ACCOUNT_ANALYSIS_ADDRESS = "/account/analysis"

    def __init__(self):
        pass

    @staticmethod
    def _check_list_params(sort):
        """
        checks list request params for exceptions.

        :param sort: the property that accounts are ordered by.
        :type sort: str

        """

        if sort != "balance" and sort != "power" :
            ParameterException(ParameterException.SORT_EXCEPTION_MESSAGE, ["sort"])

    def get_account(self, account_address: str, properties: list = None):
        """
        get data for a specific account.

        :param account_address: address of the account.
        :type account_address: str

        :args:
            * *properties* (``list``)
                properties of accounts that will be returned. default is all.

        :returns: the desired account data.
        :rtype: AccountDataMap

        """
        params = {"address": account_address}
        req = SendRequestSingle(self._API_ACCOUNT_ADDRESS, params)
        data = req.get_data()
        return AccountDataMap(data["data"][0], properties)

    def get_account_list(self , save_live: bool = False
                         , save_path: str = ""
                         , sort: str = "power"
                         , order: str = "DESC"
                         , properties: list = None
                         , count: int = 10000):
        """
        get data for a list of accounts.

        :args:
            * *start_timestamp* (``int``)
                start timestamp of query. default is None. (milliseconds)
            * *end_timestamp* (``int``)
                end timestamp of query. default is None. (milliseconds)
            * *properties* (``list``)
                properties of accounts that will be returned. default is all.
            * *sort* (``str``)
                the property that accounts are ordered by. can be sorted by "power", "balance".
                default is "power".
            * *order* (``str``)
                order of accounts by sort ("ASC" : Ascending , "DESC" : descending).
            * *count* (``int``)
                number of desired accounts. default is 10000. is ignored when both times are specified.
            * *save_live* (``bool``)
                if set to True the downloaded data will be saved to a file in each page downloaded to avoid losing data
                in case of an error.
            * *save_path* (``str``)
                path of folder that data is saved to. default is ""

        :returns: a panda dataframe containing data of desired accounts.
        :rtype: Pandas Dataframe

        """

        self._check_list_params(sort)
        params = {"sort": sort, "order": order, "start_timestamp": None, "end_timestamp": None}

        address = self._API_ACCOUNT_ADDRESS
        req = SendRequestMultiple(address, save_live, save_path, params, max_query=2000)
        data = req.get_data_multiple(count, properties, AccountDataMap)
        return data

    def get_account_analysis(self, type_: int, account_address: str, start_timestamp: int = 1):

        """
        get analysis for an account.

        :param type_: indicates type of analysis.
                      0: balance analysis
                      1: token transfer analysis
                      2: energy usage analysis
                      3: bandwidth usage analysis
        :type type_: int

        :param account_address: address of desired account.
        :type account_address: str

        :args:
            * *start_timestamp* (``int``)
                start timestamp of query. default is 1 (for this specific query input 0 returns only 100 items). (milliseconds)

        :returns: a panda dataframe containing data of desired accounts.
        :rtype: Pandas Dataframe

        """

        if start_timestamp < 1:
            ParameterWarning(ParameterWarning.START_TIME_ACCOUNT_ANALYSIS_WARNING, '"start_timestamp"')

        params = {"address": account_address, "type": type_, "start_timestamp": start_timestamp}
        req = SendRequestSingle(self._API_ACCOUNT_ANALYSIS_ADDRESS, params)
        data = req.get_data()
        df = DataFrame(data["data"])
        return df