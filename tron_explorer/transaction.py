from tron_explorer.data_map import DataMap
from tron_explorer.utils import SendRequestSingle, SendRequestMultiple


# noinspection PyAttributeOutsideInit,PyBroadException
class TransactionDataMap(DataMap):
    properties_list = ["number", "hash", "timestamp", "from_address", "to_address", "token_name", "token_abbr"
                       , "value", "confirmed", "result", "trx_burned_bandwidth", "trx_burned_energy", "trx_burned_total"
                       , "energy_used", "bandwidth_used", "contract_address", "contract_data", "method", "resources"]
    """
    a DataMap type class that is responsible for filtering properties of transaction data instances.

    :param data: the data instance.
    :type data: dict

    :param properties: properties of transaction instance that will be returned. to see what properties are included see below
    :type properties: list

    :standard: the token standard transaction of tron network.

    :properties:

        * *number* (``int``)
            number of the block that transaction is in.
        * *hash* (``str``)
            hash of transaction.
        * *timestamp* (``int``)
            timestamp of the transaction. (milliseconds)
        * *from_address* (``str``)
            address of transaction creator.
        * *to_address* (``str``)
            address of transaction recipient.
        * *token_name* (``str``)
            name of the transferred token.
        * *token_abbr* (``str``)
            name abbreviation of the transferred token.
        * *value* (``int``)
            amount of the transferred token.
        * *confirmed* (``str``)
            whether if transaction is confirmed.
        * *result* (``str``)
            whether if transaction is successful.
        * *trx_burned_bandwidth* (``int``)
            amount of trx burned(fee) for bandwidth usage.
        * *trx_burned_energy* (``int``)
            amount of trx burned(fee) for energy usage.
        * *trx_burned_total* (``int``)
            total amount of trx burned(fee).
        * *energy_used* (``float``)
            energy used for verifying transaction.
        * *bandwidth_used* (``float``)
            bandwidth used for verifying transaction.


    :smart contract: transactions related to a smart contract.

    :properties:

        * *number* (``int``)
            number of the block that transaction is in.
        * *hash* (``str``)
            hash of transaction.
        * *timestamp* (``int``)
            timestamp of the transaction. (milliseconds)
        * *from_address* (``str``)
            address of transaction creator.
        * *to_address* (``str``)
            address of transaction recipient.
        * *value* (``int``)
            amount of the transferred token.
        * *contract_address* (``str``)
            contract address of the transaction.
        * *contract_data* (``str``)
            contract data of the transaction.
        * *method* (``str``)
            method name of used in contract to create the transaction.
        * *confirmed* (``str``)
            whether if transaction is confirmed.
        * *result* (``str``)
            whether if transaction is successful.
        * *trx_burned_bandwidth* (``int``)
            amount of trx burned(fee) for bandwidth usage.
        * *trx_burned_energy* (``int``)
            amount of trx burned(fee) for energy usage.
        * *trx_burned_total* (``int``)
            total amount of trx burned(fee).
        * *energy_used* (``float``)
            energy used for verifying transaction.
        * *bandwidth_used* (``float``)
            bandwidth used for verifying transaction.


    :staking: transaction related to staking.

    :properties:
        * *number* (``int``)
            number of the block that transaction is in.
        * *hash* (``str``)
            hash of transaction.
        * *timestamp* (``int``)
            timestamp of the transaction. (milliseconds)
        * *from_address* (``str``)
            address of transaction creator.
        * *to_address* (``str``)
            the resource receiving address.
        * *token_name* (``str``)
            name of the transferred token.
        * *token_abbr* (``str``)
            name abbreviation of the transferred token.
        * *value* (``int``)
            amount of the staked token.
        * *confirmed* (``str``)
            whether if transaction is confirmed.
        * *result* (``str``)
            whether if transaction is successful.
        * *trx_burned_bandwidth* (``int``)
            amount of trx burned(fee) for bandwidth usage.
        * *trx_burned_energy* (``int``)
            amount of trx burned(fee) for energy usage.
        * *trx_burned_total* (``int``)
            total amount of trx burned(fee).
        * *energy_used* (``float``)
            energy used for verifying transaction.
        * *bandwidth_used* (``float``)
            bandwidth used for verifying transaction.

    :unstaking: transaction related to unstaking.

    :properties:

        * *number* (``int``)
            number of the block that transaction is in.
        * *hash* (``str``)
            hash of transaction.
        * *timestamp* (``int``)
            timestamp of the transaction. (milliseconds)
        * *from_address* (``str``)
            address of transaction the gate.
        * *to_address* (``str``)
            address of transaction recipient.
        * *token_name* (``str``)
            name of the transferred token.
        * *token_abbr* (``str``)
            name abbreviation of the transferred token.
        * *value* (``int``)
            amount of the staked token.
        * *confirmed* (``str``)
            whether if transaction is confirmed.
        * *result* (``str``)
            whether if transaction is successful.
        * *trx_burned_bandwidth* (``int``)
            amount of trx burned(fee) for bandwidth usage.
        * *trx_burned_energy* (``int``)
            amount of trx burned(fee) for energy usage.
        * *trx_burned_total* (``int``)
            total amount of trx burned(fee).
        * *energy_used* (``float``)
            energy used for verifying transaction.
        * *bandwidth_used* (``float``)
            bandwidth used for verifying transaction.


    :reward: transaction related to reward claiming.

    :properties:

            * *number* (``int``)
                number of the block that transaction is in.
            * *hash* (``str``)
                hash of transaction.
            * *timestamp* (``int``)
                timestamp of the transaction. (milliseconds)
            * *from_address* (``str``)
                address of the reward receiver.
            * *token_name* (``str``)
                name of the transferred token.
            * *token_abbr* (``str``)
                name abbreviation of the transferred token.
            * *value* (``int``)
                amount of the reward.
            * *confirmed* (``str``)
                whether if transaction is confirmed.
            * *result* (``str``)
                whether if transaction is successful.
            * *trx_burned_bandwidth* (``int``)
                amount of trx burned(fee) for bandwidth usage.
            * *trx_burned_energy* (``int``)
                amount of trx burned(fee) for energy usage.
            * *trx_burned_total* (``int``)
                total amount of trx burned(fee).
            * *energy_used* (``float``)
                energy used for verifying transaction.
            * *bandwidth_used* (``float``)
                bandwidth used for verifying transaction.


    :vote: transaction related to voting.

    :properties:

        * *number* (``int``)
            number of the block that transaction is in.
        * *hash* (``str``)
            hash of transaction
        * *timestamp* (``int``)
            timestamp of the transaction. (milliseconds)
        * *to_address* (``str``)
            address of candidate.
        * *from_address* (``str``)
            address of the voter.
        * *token_name* (``str``)
            name of the transferred token.
        * *token_abbr* (``str``)
            name abbreviation of the transferred token.
        * *value* (``int``)
            amount of the reward.
        * *confirmed* (``str``)
            whether if transaction is confirmed.
        * *result* (``str``)
            whether if transaction is successful.
        * *trx_burned_bandwidth* (``int``)
            amount of trx burned(fee) for bandwidth usage.
        * *trx_burned_energy* (``int``)
            amount of trx burned(fee) for energy usage.
        * *trx_burned_total* (``int``)
            total amount of trx burned(fee).
        * *energy_used* (``float``)
            energy used for verifying transaction.
        * *bandwidth_used* (``float``)
            bandwidth used for verifying transaction.


        """

    def __init__(self, data, properties):
        super().__init__(data, properties)

    def filter_data(self):
        """
        filters data based on parameter properties.

        """

        super().filter_data()
        data = self.data
        properties = self.properties

        contract_type = data["contractType"]
        # calling methods based on contractType
        if contract_type == 31:
            self._smart_contract(data, properties)

        if contract_type == 1 or contract_type == 2:
            self._standard(data, properties)

        if contract_type == 11:
            self._staking(data, properties)

        if contract_type == 12:
            self._unstaking(data, properties)

        if contract_type == 13:
            self._reward(data, properties)

        if contract_type == 4:
            self._votes(data, properties)

    def _standard(self, data, properties):
        # if no property is specified all properties will be returned
        if properties is None:
            self.transaction_type = "standard"
            self.block = data["block"]
            self.hash = data["hash"]
            self.timestamp = int(data["timestamp"])
            self.from_address = data["ownerAddress"]
            self.to_address = data.get("toAddress")

            # in transaction-info response, token info is inside contractData
            if "tokenInfo" in data:
                self.token_name = data["tokenInfo"]["tokenName"]
                self.token_abbr = data["tokenInfo"]["tokenAbbr"]
                self.value = int(data["amount"]) / (10 ** 6)
            else:

                try:
                    self.token_name = data["contractData"]["tokenInfo"]["tokenName"]
                    self.token_abbr = data["contractData"]["tokenInfo"]["tokenAbbr"]
                except KeyError:
                    pass

                self.value = int(data["contractData"]["amount"]) / (10 ** 6)

            self.confirmed = data["confirmed"]

            # in transaction-info response, there is no result
            if "result" in data:
                self.result = data["result"]
            else:
                self.result = data["contractRet"]

            cost: dict = data.get("cost")
            self.trx_burned_bandwidth = int(cost.get("net_fee", 0)) / (10 ** 6)
            self.trx_burned_energy = int(cost.get("energy_fee", 0)) / (10 ** 6)
            self.trx_burned_total = int(cost.get("fee", 0)) / (10 ** 6)
            self.energy_used = float(cost.get("energy_usage_total", 0)) / (10 ** 6)
            self.bandwidth_used = float(cost.get("net_usage", 0))

        else:
            self.transaction_type = "standard"
            if "block" in properties:
                self.block = data["block"]
            if "hash" in properties:
                self.hash = data["hash"]
            if "timestamp" in properties:
                self.timestamp = int(data["timestamp"])
            if "from_address" in properties:
                self.from_address = data["ownerAddress"]
            if "to_address" in properties:
                self.to_address = data["toAddress"]

            # in transaction-info response, token info is inside contractData
            if "tokenInfo" in data:
                if "token_name" in properties:
                    self.token_name = data["tokenInfo"]["tokenName"]
                if "token_abbr" in properties:
                    self.token_abbr = data["tokenInfo"]["tokenAbr"]
                if "value" in properties:
                    self.value = int(data["amount"]) / (10 ** 6)
            else:
                if "token_name" in properties:
                    self.token_name = data["contractData"]["tokenInfo"]["tokenName"]
                if "token_abbr" in properties:
                    self.token_abbr = data["contractData"]["tokenInfo"]["tokenAbbr"]
                if "value" in properties:
                    self.value = int(data["contractData"]["amount"]) / (10 ** 6)

            if "confirmed" in properties:
                self.confirmed = data["confirmed"]

            # in transaction-info response, there is no result
            if "result" in properties:
                if "result" in data:
                    self.result = data["result"]
                else:
                    self.result = data["contractRet"]

            cost: dict = data.get("cost")
            if "trx_burned_bandwidth" in properties:
                self.trx_burned_bandwidth = int(cost.get("net_fee", 0)) / (10 ** 6)
            if "trx_burned_energy" in properties:
                self.trx_burned_energy = int(cost.get("energy_fee", 0)) / (10 ** 6)
            if "trx_burned_total" in properties:
                self.trx_burned_total = int(cost.get("fee", 0)) / (10 ** 6)
            if "energy_used" in properties:
                self.energy_used = float(cost.get("energy_usage_total", 0)) / (10 ** 6)
            if "bandwidth_used" in properties:
                self.bandwidth_used = float(cost.get("net_usage", 0))

    def _smart_contract(self, data, properties):
        # if no property is specified all properties will be returned
        if properties is None:
            self.transaction_type = "smart contract"
            self.block = data["block"]
            self.hash = data["hash"]
            self.timestamp = int(data["timestamp"])
            self.from_address = data["ownerAddress"]
            self.contract_address = data["trigger_info"]["contract_address"]

            try:
                self.method = data["trigger_info"]["methodName"]
            except KeyError:
                pass

            self.confirmed = data["confirmed"]
            self.result = data.get("result", None)

            # deposit doesn't have to address, nft doesn't have value or to_address
            # there might be no to_address or value info
            try:
                self.contract_data = data["trigger_info"]["data"]
                if self.method != "deposit":
                    if "_to" not in data["trigger_info"]["parameter"]:
                        self.to_address = data["trigger_info"]["parameter"]["to"]
                        self.value = int(data["trigger_info"]["parameter"]["value"]) / (10 ** 6)
                    else:
                        self.to_address = data["trigger_info"]["parameter"]["_to"]
                        self.value = int(data["trigger_info"]["parameter"]["_value"]) / (10 ** 6)
                else:
                    self.value = int(data["trigger_info"]["parameter"]["_amount"]) / (10 ** 6)
            except (KeyError, AttributeError):
                pass



            cost: dict = data.get("cost")
            self.trx_burned_bandwidth = int(cost.get("net_fee", 0)) / (10 ** 6)
            self.trx_burned_energy = int(cost.get("energy_fee", 0)) / (10 ** 6)
            self.trx_burned_total = int(cost.get("fee", 0)) / (10 ** 6)
            self.energy_used = float(cost.get("energy_usage_total", 0)) / (10 ** 6)
            self.bandwidth_used = float(cost.get("net_usage", 0))

        else:
            self.transaction_type = "smart contract"
            if "block" in properties:
                self.block = data["block"]
            if "hash" in properties:
                self.hash = data["hash"]
            if "timestamp" in properties:
                self.timestamp = int(data["timestamp"])
            if "from_address" in properties:
                self.from_address = data["ownerAddress"]
            if "contract_address" in properties:
                self.contract_address = data["trigger_info"]["contract_address"]
            if "method" in properties:
                self.method = data["trigger_info"]["methodName"]

            method = data["trigger_info"]["methodName"]

            # deposit doesn't have to address, nft doesn't have value or to_address
            # there might be no to_address or value info
            try:
                if method != "deposit":
                    if "_to" not in data["trigger_info"]["parameter"]:
                        if "to_address" in properties:
                            self.to_address = data["trigger_info"]["parameter"]["to"]
                        if "value" in properties:
                            self.value = int(data["trigger_info"]["parameter"]["value"]) / (10 ** 6)
                    else:
                        if "to_address" in properties:
                            self.to_address = data["trigger_info"]["parameter"]["_to"]
                        if "value" in properties:
                            self.value = int(data["trigger_info"]["parameter"]["_value"]) / (10 ** 6)
                elif self.method == "deposit":
                    if "to_address" in properties:
                        self.value = int(data["trigger_info"]["parameter"]["_amount"]) / (10 ** 6)
            except KeyError:
                pass

            if "contract_data" in properties:
                self.contract_data = data["trigger_info"]["data"]
            if "confirmed" in properties:
                self.confirmed = data["confirmed"]
            if "result" in properties:
                self.result = data["result"]
            cost: dict = data.get("cost")
            if "trx_burned_bandwidth" in properties:
                self.trx_burned_bandwidth = int(cost.get("net_fee", 0)) / (10 ** 6)
            if "trx_burned_energy" in properties:
                self.trx_burned_energy = int(cost.get("energy_fee", 0)) / (10 ** 6)
            if "trx_burned_total" in properties:
                self.trx_burned_total = int(cost.get("fee", 0)) / (10 ** 6)
            if "energy_used" in properties:
                self.energy_used = float(cost.get("energy_usage_total", 0)) / (10 ** 6)
            if "bandwidth_used" in properties:
                self.bandwidth_used = float(cost.get("net_usage", 0))

    def _staking(self, data, properties):
        self._standard(data, properties)
        self.transaction_type = "staking"
        # if no property is specified all properties will be returned
        if properties is None:

            try:
                self.resource = data["contractData"]["resource"]
            except KeyError:
                self.resource = "BANDWIDTH"
            self.value = int(data["amount"]) / (10 ** 6)

        else:

            try:
                self.resource = data["contractData"]["resource"]
            except KeyError:
                self.resource = "BANDWIDTH"

            if "value" in properties:
                self.value = int(data["amount"]) / (10 ** 6)

    def _unstaking(self, data, properties):
        self._standard(data, properties)
        self.transaction_type = "unstaking"

    def _reward(self, data, properties):
        self._standard(data, properties)
        self.transaction_type = "rewards"

    def _votes(self, data, properties):
        self.transaction_type = "vote"
        if properties is None:
            self.transaction_type = "standard"
            self.block = data["block"]
            self.hash = data["hash"]
            self.timestamp = int(data["timestamp"])
            self.vote_amount = int(data["amount"])
            self.voter = data["ownerAddress"]
            self.sr_address = data.get("toAddress")
            self.confirmed = data["confirmed"]
            cost: dict = data.get("cost")
            self.trx_burned_bandwidth = int(cost.get("net_fee", 0)) / (10 ** 6)
            self.trx_burned_energy = int(cost.get("energy_fee", 0)) / (10 ** 6)
            self.trx_burned_total = int(cost.get("fee", 0)) / (10 ** 6)
            self.energy_used = float(cost.get("energy_usage_total", 0)) / (10 ** 6)
            self.bandwidth_used = float(cost.get("net_usage", 0))

        else:
            if "block" in properties:
                self.block = data["block"]
            if "hash" in properties:
                self.hash = data["hash"]
            if "timestamp" in properties:
                self.timestamp = int(data["timestamp"])
            if 'vote_amount' in properties:
                self.vote_amount = int(data["amount"])
            if "voter" in properties:
                self.voter = data["ownerAddress"]
            if "sr_address" in properties:
                self.sr_address = data["toAddress"]

            if "confirmed" in properties:
                self.confirmed = data["confirmed"]

            # in transaction-info response, there is no result
            if "result" in properties:
                if "result" in data:
                    self.result = data["result"]
                else:
                    self.result = data["contractRet"]

            cost: dict = data.get("cost")
            if "trx_burned_bandwidth" in properties:
                self.trx_burned_bandwidth = int(cost.get("net_fee", 0)) / (10 ** 6)
            if "trx_burned_energy" in properties:
                self.trx_burned_energy = int(cost.get("energy_fee", 0)) / (10 ** 6)
            if "trx_burned_total" in properties:
                self.trx_burned_total = int(cost.get("fee", 0)) / (10 ** 6)
            if "energy_used" in properties:
                self.energy_used = float(cost.get("energy_usage_total", 0)) / (10 ** 6)
            if "bandwidth_used" in properties:
                self.bandwidth_used = float(cost.get("net_usage", 0))


# noinspection PyIncorrectDocstring
class Transaction:
    """
    instantiate an object that contains a methods for multiple request related to transactions.

    """

    _API_TRANSACTION_INFO_ADDRESS = "/transaction-info"
    _API_TRANSACTION_ADDRESS = "/transaction"

    def get_transaction(self, hash_: str, properties: list = None):
        """
        get a specific transaction.

        :param hash_: the hash of desired transaction.
        :type hash_: str

        :kwargs:
            * *properties* (``list``)
                properties of transaction that will be returned. default is all.

        :returns: the desired transaction data.
        :rtype: TransactionDataMap

        """

        params = {"hash": hash_}
        req = SendRequestSingle(self._API_TRANSACTION_INFO_ADDRESS, params)
        data = req.get_data()
        return TransactionDataMap(data, properties)

    def get_transaction_list_block(self, number: str
                                   , save_live: bool = False
                                   , save_path: str = ""
                                   , order: str = "DESC"
                                   , properties: list = None
                                   , count: int = 10000):
        """
        get transactions in a block.

        :args:
            * *properties* (``list``)
                properties of transaction that will be returned. default is all.
            * *sort* (``str``)
                the property that transaction are ordered by.
            * *order* (``str``)
                order of transaction by time ("ASC" : Ascending , "DESC" : descending).
            * *count* (``int``)
                number of desired transaction. default is 10000. is ignored when both times are specified.
            * *save_live* (``bool``)
                if set to True the downloaded data will be saved to a file in each page downloaded to avoid losing data
                in case of an error.
            * *save_path* (``str``)
                path of folder that data is saved to. default is ""


        :returns: a panda dataframe containing data of desired transactions.
        :rtype: Pandas Dataframe
        """

        params = {"block": number, "sort": "timestamp",
                  "start_timestamp": None, "end_timestamp": None, "order": order}

        address = self._API_TRANSACTION_ADDRESS
        req = SendRequestMultiple(address, save_live, save_path, params, max_query=2000)
        data = req.get_data_multiple(count, properties, TransactionDataMap)
        return data

    def get_transaction_list_account(self, address: str
                                     , save_live: bool = False
                                     , save_path: str = ""
                                     , order: str = "DESC"
                                     , properties: list = None
                                     , count: int = 10000):
        """
        get transactions related to an account.

        :args:
            * *properties* (``list``)
                properties of transaction that will be returned. default is all.
            * *sort* (``str``)
                the property that transaction are ordered by.
            * *order* (``str``)
                order of transaction by time ("ASC" : Ascending , "DESC" : descending).
            * *count* (``int``)
                number of desired transaction. default is 10000. is ignored when both times are specified.
            * *save_live* (``bool``)
                if set to True the downloaded data will be saved to a file in each page downloaded to avoid losing data
                in case of an error.
            * *save_path* (``str``)
                path of folder that data is saved to. default is ""

        :returns: a panda dataframe containing data of desired transactions.
        :rtype: Pandas Dataframe
        """

        params = {"address": address, "sort": "timestamp",
                  "start_timestamp": None, "end_timestamp": None, "order": order}

        address = self._API_TRANSACTION_ADDRESS
        req = SendRequestMultiple(address, save_live, save_path, params, max_query=2000)
        data = req.get_data_multiple(count, properties, TransactionDataMap)
        return data

    def get_transaction_list_blockchain(self, start_timestamp: int = None
                                        , end_timestamp: int = None
                                        , save_live: bool = False
                                        , save_path: str = ""
                                        , order: str = "DESC"
                                        , properties: list = None
                                        , count: int = 10000):
        """
        get transactions in blockchain.

        :args:
            * *start_timestamp* (``int``)
                start timestamp of query. default is None. (milliseconds)
            * *end_timestamp* (``int``)
                end timestamp of query. default is None. (milliseconds)
            * *properties* (``list``)
                properties of transaction that will be returned. default is all.
            * *order* (``str``)
                order of transaction by time ("ASC" : Ascending , "DESC" : descending).
            * *count* (``int``)
                number of desired transactions. default is 10000. is ignored when both times are specified.
            * *save_live* (``bool``)
                if set to True the downloaded data will be saved to a file in each page downloaded to avoid losing data
                in case of an error.
            * *save_path* (``str``)
                path of folder that data is saved to. default is ""

        :returns: a panda dataframe containing data of desired transactions.
        :rtype: Pandas Dataframe
        """

        params = {"start_timestamp": start_timestamp, "end_timestamp": end_timestamp,
                  "order": order, "sort": "timestamp"}

        address = self._API_TRANSACTION_ADDRESS
        req = SendRequestMultiple(address, save_live, save_path, params, max_query=10000)
        data = req.get_data_multiple(count, properties, TransactionDataMap)
        return data
