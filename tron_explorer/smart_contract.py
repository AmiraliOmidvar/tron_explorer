from tron_explorer.data_map import DataMap
from tron_explorer.exceptions import ParameterException
from tron_explorer.utils import SendRequestSingle, SendRequestMultiple


# noinspection PyAttributeOutsideInit
class SmartContractDataMap(DataMap):

    properties_list = ["contract_address", "name", "tag", "timestamp", "balance", "number_of_calls"
        , "creator_address", "creation_address", "creation_transaction_id"
        , "energy_consumption_ratio", "remaining_energy", "token_name", "token_abbr"
        , "token_issuer_address"]

    """
        a DataMap type class that is responsible for filtering properties of smart contract data instances.

        :param data: the data instance.
        :type data: dict

        :param properties: properties of smart contract instance that will be returned. to see what properties are included see below
        :type properties: list

        :properties:

            * *contract_address* (``str``)
                address of the contract.
            * *name* (``str``)
                name of the contract.
            * *tag* (``str``)
                public tag of contract.
            * *timestamp* (``int``)
                timestamp of the contract creation. (milliseconds)
            * *balance* (``int``)
                balance of contract. (trx)
            * *number_of_calls* (``int``)
                number of times that contract has been triggered.
            * *creator_address* (``str``)
                address of the creator.
                ``only available when getting data for a single contract``.
            * *creation_transaction_id* (``str``)
                hash of the transaction that was used to create the contract.
                ``only available when getting data for a single contract``.
            * *energy_consumption_ratio* (``list``)
                energy usage percentage by the user and contract.(["user","contract"])
                ``only available when getting data for a single contract``.
            * *token_name* (``str``)
                name of trc20 contract token issued by the contract.
            * *token_abbr* (``str``)
                name abbreviation of token issued by contract.
            * *token_issuer_address* (``str``)
                address of the account that issued the token.


        """

    def __init__(self, data, properties):
        super().__init__(data, properties)

    def filter_data(self):
        """
        filters data based on parameter properties.
        """
        # because of too much variety in data filtering is handled differently.
        self.CLASS_NAME = "Smart Contract"

        super().filter_data()
        data = self.data
        properties = self.check_properties()

        if "contract_address" in properties:
            self.contract_address = data["address"]
        if "name" in properties:
            self.name = data["name"]
        if "tag" in properties:
            self.tag = data["tag1"]
        if "timestamp" in properties:
            self.timestamp = int(data["date_created"])
        if "balance" in properties:
            self.balance = int(data["balance"])
        if "number_of_calls" in properties:
            self.number_of_calls = int(data["trxCount"])
        if "creator" in data:
            if "creator_address" in properties:
                self.creator_address = data["creator"]["address"]
            if "creation_transaction_id" in properties:
                self.creation_transaction_id = data["creator"]["txHash"]
            if "energy_consumption_ratio" in properties:
                self.energy_consumption_ratio = [float(data["creator"]["consume_user_resource_percent"]),
                                                 100 - float(data["creator"]["consume_user_resource_percent"])]
            if "remaining_energy" in properties:
                self.remaining_energy = int(data["creator"]["energy_remaining"])
        if "tokenInfo" in data:
            if "token_name" in properties:
                self.token_name = data["tokenInfo"]["tokenName"]
            if "token_abbr" in properties:
                self.token_abbr = data["tokenInfo"]["tokenAbbr"]
            if "token_issuer_address" in properties:
                self.token_issuer_address = data["tokenInfo"]["issuerAddr"]
        elif "trc20token" in data:
            if "token_name" in properties:
                self.token_name = data["trc20token"]["name"]
            if "token_abbr" in properties:
                self.token_abbr = data["trc20token"]["symbol"]
            if "token_issuer_address" in properties:
                self.token_issuer_address = data["trc20token"]["issuer_addr"]


# noinspection PyIncorrectDocstring
class SmartContract:
    """
    instantiate an object that contains a methods for multiple request related to smart contracts.

    """

    _API_CONTRACT_ADDRESS = "/contract"
    _API_CONTRACTS_ADDRESS = "/contracts"

    @staticmethod
    def _check_list_params(sort):
        """
        checks list request params for exceptions.

        :param sort: the property that accounts are ordered by.
        :type sort: str

        """

        if sort not in ["number_of_calls", "balance" , "timestamp"]:
            raise ParameterException(ParameterException.SORT_EXCEPTION_MESSAGE, ["sort"])

    def get_smart_contract(self, contract_address: str, properties: list = None):
        """
        get data for a specific smart contract.

        :param contract_address: address of the contract.
        :type contract_address: str

        :args:
            * *properties* (``list``)
                properties of accounts that will be returned. default is all.

        :returns: the desired account data.
        :rtype: SmartContractDataMap

        """

        params = {"contract": contract_address}
        req = SendRequestSingle(self._API_CONTRACT_ADDRESS, params)
        data = req.get_data()
        return SmartContractDataMap(data["data"][0], properties)

    def get_smart_contract_list_blockchain(self, start_timestamp: int = None
                                           , end_timestamp: int = None
                                           , save_live: bool = False
                                           , save_path: str = ""
                                           , sort: str = "timestamp"
                                           , order: str = "DESC"
                                           , properties: list = None
                                           , count: int = 10000
                                           , verified_only: bool = False
                                           , open_source_only: bool = False):
        """
        get data for a list of account.

        :args:
            * *start_timestamp* (``int``)
                start timestamp of query. default is None. (milliseconds)
            * *end_timestamp* (``int``)
                end timestamp of query. default is None. (milliseconds)
            * *properties* (``list``)
                properties of contracts that will be returned. default is all.
            * *sort* (``str``)
                the property that contracts are ordered by. can be sorted by "number_of_calls", "balance", "timestamp".
                default is "timestamp".
            * *order* (``str``)
                order of contracts by sort ("ASC" : Ascending , "DESC" : descending).
            * *count* (``int``)
                number of desired contracts. default is 10000. is ignored when both times are specified.
            * *verified_only* (``bool``)
                get only verified contracts.
            * *open_source_only* (``bool``)
                get only open_source_only contracts.
            * *save_live* (``bool``)
                if set to True the downloaded data will be saved to a file in each page downloaded to avoid losing data
                in case of an error.
            * *save_path* (``str``)
                path of folder that data is saved to. default is ""


        :returns: a panda dataframe containing data of desired contracts.
        :rtype: Pandas Dataframe

        """
        self._check_list_params(sort)

        params = {"start_timestamp": start_timestamp, "end_timestamp": end_timestamp,
                  "order": order, "sort": sort, "verified-only": verified_only, "open-source-only": open_source_only}

        address = self._API_CONTRACTS_ADDRESS
        req = SendRequestMultiple(address, save_live, save_path, params, max_query=10000)
        data = req.get_data_multiple(count, properties, SmartContractDataMap)
        return data
