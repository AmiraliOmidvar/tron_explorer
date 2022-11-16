from tron_explorer.data_map import DataMap
import time
import datetime

# noinspection PyAttributeOutsideInit
from tron_explorer.utils import SendRequestSingle


# noinspection PyAttributeOutsideInit
class TokenSingleDataMap(DataMap):
    properties_dict_trc10 = {"token_id": "tokenID", "name": "name", "name_abbr": "abbr"
        , "timestamp": "dateCreated", "owner_address": "ownerAddress"
        , "description": "description", "supply": ""
        , "volume_24h": "volume24h", "number_of_transactions": "totalTransactions"
        , "number_of_holders": "nrOfTokenHolders", "price_in_trx": ""
        , "price_in_usd": "", "market_cap": ""}

    properties_dict_trc20 = {"name": "symbol", "contract_name": "contract_name"
        , "owner_address": "issue_address", "gain": "", "timestamp": "", "supply": ""
        , "volume_24h": "volume24h", "number_of_transactions": "transfer_num", "number_of_holders": "holder_count"
        , "price_int_trx": ""
        , "price_in_usd": ""}

    """
    a DataMap type class that is responsible for filtering properties of token data instances.

    :param data: the data instance.
    :type data: dict

    :param properties: properties of token instance that will be returned. to see what properties are included see below
    :type properties: list

    :trc10:

    :properties:

        * *name* (``str``)
            name of the token.
        * *name_abbr* (``str``)
            abbreviation of token name.
        * *owner_address* (``str``)
            token's owner address.
        * *token_id* (``str``)
            id of the token.
        * *description* (``str``)
            token description.
        * *timestamp* (``int``)
            timestamp of token's creation.
        * *gain* (``float``)
            price changed in last 24 hours. (percentage)
        * *supply* (``int``)
            number of token in circulation.
        * *market_cap* (``int``)
            market cap of token. (trx)
        * *volume_24h* (``int``)
            token volume traded in last 24h.
        * *price_int_trx* (``int``)
            price of token in trx.
        * *price_int_usd* (``int``)
            price of token in usd.
        * *number_of_holders* (``int``)
            number of accounts that hold the token.
        * *number_of_transactions* (``int``)
            number of transactions related to token.

    :trc20:

    :properties:

        * *name* (``str``)
            name of the token.
        * *owner_address* (``str``)
            token's owner address.
        * *contract_address* (``str``)
            address of token's contract.
        * *timestamp* (``int``)
            timestamp of token's issue date.
        * *gain* (``float``)
            price changed in last 24 hours. (percentage)
        * *supply* (``int``)
            number of token in circulation.
        * *market_cap* (``int``)
            market cap of token.
        * *volume_24h* (``int``)
            token volume traded in last 24h.
        * *price_int_trx* (``int``)
            price of token in trx.
        * *price_int_usd* (``int``)
            price of token in usd.
        * *number_of_holders* (``int``)
            number of accounts that hold the token.
        * *number_of_transactions* (``int``)
            number of transactions related to token.

    """

    def __init__(self, data, properties):
        super().__init__(data, properties)

    def filter_data(self):
        """
        filters data based on parameter properties.
        """

        data = self.data

        if "tokenID" in data:
            self.token_type = "trc10"
            self.CLASS_NAME = "TokenSingle"
            self.properties_list = self.properties_dict_trc10.keys()

            super().filter_data()
            data = self.data
            properties = self.check_properties()

            for p in properties:
                try:
                    if self.properties_dict_trc10[p] == "":
                        if p == "supply":
                            setattr(self, p, data["totalSupply"] / (10 ** 5))
                        if p == "price_in_trx":
                            setattr(self, p, data["market_info"]["priceInTrx"])
                        if p == "price_in_usd":
                            setattr(self, p, data["market_info"]["priceInUsd"])
                        if p == "market_cap":
                            setattr(self, p, data["totalSupply"])
                    else:
                        setattr(self, p, data[self.properties_dict_trc10[p]])
                except KeyError:
                    setattr(self, p, None)

        else:
            self.token_type = "trc20"
            self.CLASS_NAME = "TokenSingle"
            self.properties_list = self.properties_dict_trc20.keys()

            super().filter_data()
            data = self.data
            properties = self.check_properties()

            for p in properties:
                try:
                    if self.properties_dict_trc20[p] == "":
                        if p == "gain":
                            self.gain = data["market_info"]["gain"]
                        if p == "timestamp":
                            is_date = data["issue_time"]
                            timestamp = time.mktime(
                                datetime.datetime.strptime(is_date, "%Y-%m-%d %H:%M:%S").timetuple())
                            self.timestamp = int(timestamp) * 1000
                        if p == "supply":
                            self.supply = int(data["total_supply_with_decimals"]) / (
                                        10 ** int(data["market_info"]["sPrecision"]))
                        if p == "price_in_trx":
                            self.price_in_trx = float(data["market_info"]["priceInTrx"])
                        if p == "price_in_usd":
                            self.price_in_usd = float(data["market_info"]["priceInUsd"])
                    else:
                        setattr(self, p, data[self.properties_dict_trc20[p]])
                except KeyError:
                    setattr(self, p, None)


class TokenSingle:
    _API_TRC10_ADDRESS = "/token"
    _API_TRC20_ADDRESS = "/token_trc20"

    def get_trc10_token(self, token_id: str, properties: list = None):
        """
        get data for a specific trc10 token.

        :param token_id: unique identifier of trc10 token.
        :type token_id: str

        :args:
            * *properties* (``list``)
                properties of token that will be returned. default is all.

        :returns: the desired account data.
        :rtype: AccountDataMap

        """
        params = {"id": token_id}
        req = SendRequestSingle(self._API_TRC10_ADDRESS, params)
        data = req.get_data()
        return TokenSingleDataMap(data["data"][0], properties)

    def get_trc20_token(self, contract_address: str, properties: list = None):
        """
        get data for a specific trc20 token.

        :param contract_address: contract address of trc20 token.
        :type contract_address: str

        :args:
            * *properties* (``list``)
                properties of token that will be returned. default is all.

        :returns: the desired account data.
        :rtype: AccountDataMap

        """
        params = {"contract": contract_address}
        req = SendRequestSingle(self._API_TRC20_ADDRESS, params)
        data = req.get_data()
        return TokenSingleDataMap(data["trc20_tokens"][0], properties)
