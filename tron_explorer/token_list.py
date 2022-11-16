from tron_explorer.data_map import DataMap

# noinspection PyAttributeOutsideInit
from tron_explorer.exceptions import ParameterException
from tron_explorer.utils import SendRequestMultiple


# noinspection PyAttributeOutsideInit
class TokenListDataMap(DataMap):
    properties_dict = {"name": "name", "name_abbr": "abbr", "owner_address": "ownerAddress"
        , "timestamp": "dateCreated", "description": "description", "vip": "vip", "supply": "supply"
        , "number_of_holders": "nrOfTokenHolders", "number_of_transactions": "transferCount", "token_id": "tokenId"
        , "token_hash": "hash", "gain": "gain", "market_cap": "marketcap", "volume_24h": "volume24hInTrx"
        , "price_in_trx": "priceInTrx", "price_in_usd": "priceInUsd", "contract_address": "contractAddress"
        , }
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
        * *vip* (``str``)
            vip status of token.
        * *token_hash* (``str``)
            hash of the token.
        * *timestamp* (``int``)
            timestamp of token's creation.
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

    :trc20:

    :properties:

        * *name* (``str``)
            name of the token.
        * *name_abbr* (``str``)
            abbreviation of token name.
        * *owner_address* (``str``)
            token's owner address.
        * *contract_address* (``str``)
            address of token's contract.
        * *vip* (``str``)
            vip status of token.
        * *timestamp* (``int``)
            timestamp of token's creation.
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

    :trc721 or trc1155:

    :properties:

        * *name* (``str``)
            name of the token.
        * *name_abbr* (``str``)
            abbreviation of token name.
        * *contract_address* (``str``)
            address of token's contract.
        * *timestamp* (``int``)
            timestamp of token's creation.
        * *vip* (``str``)
            vip status of token.
        * *supply* (``int``)
            number of token in circulation.
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

        self.CLASS_NAME = "TokenList"
        self.properties_list = self.properties_dict.keys()

        super().filter_data()
        data = self.data
        properties = self.check_properties()
        self.token_type = data["tokenType"]

        for p in properties:
            try:
                if p == "timestamp":
                    setattr(self, p, data[self.properties_dict[p]] * 1000)
                else:
                    setattr(self, p, data[self.properties_dict[p]])
            except KeyError:
                setattr(self, p, None)


class TokenList:
    _API_TOKEN_LIST_ADDRESS = "/tokens/overview"

    @staticmethod
    def _check_list_params(sort, token_type):
        """
        checks list request params for exceptions.

        :param sort: the property that accounts are ordered by.
        :type sort: str

        """
        if sort not in ["init", "gain", "market_cap", "number_of_holders", "volume_24h"]:
            raise ParameterException(ParameterException.SORT_EXCEPTION_MESSAGE, ["sort"])

        if token_type != "trc10" and token_type != "trc20" and \
                token_type != "trc721" and token_type != "trc1155" and token_type != "top" and token_type != "all":
            raise ParameterException(ParameterException.SORT_EXCEPTION_MESSAGE, ["token_type"])

    def get_token_list(self, save_live: bool = False
                       , save_path: str = ""
                       , sort: str = "gain"
                       , order: str = "DESC"
                       , properties: list = None
                       , count: int = 10000
                       , token_type: str = "all"):

        """
        get data for a list of tokens.

        :args:
            * *start_timestamp* (``int``)
                start timestamp of query. default is None. (milliseconds)
            * *end_timestamp* (``int``)
                end timestamp of query. default is None. (milliseconds)
            * *properties* (``list``)
                properties of tokens that will be returned. default is all.
            * *sort* (``str``)
                the property that tokens are ordered by. can be sorted by "gain", "market_cap",
                "number_of holders", "volume_24h". default is "gain".
            * *order* (``str``)
                order of tokens by sort ("ASC" : Ascending , "DESC" : descending).
            * *count* (``int``)
                number of desired tokens. default is 10000. is ignored when both times are specified.
            * *save_live* (``bool``)
                if set to True the downloaded data will be saved to a file in each page downloaded to avoid losing data
                in case of an error.
            * *save_path* (``str``)
                path of folder that data is saved to. default is ""
            * *token_type* (``str``)
                all : return all tokens
                trc10 : return only and all trc10 tokens.
                trc20 : return only and all trc20 tokens.
                trc721 : return only and all trc721 tokens.
                trc1155 : return only and all trc1155 tokens.
                default is all.


        :returns: a panda dataframe containing data of desired tokens.
        :rtype: Pandas Dataframe

        """

        self._check_list_params(sort, token_type)

        if sort == "market_cap":
            sort = "marketcap"
        if sort == "volume_24h":
            sort = "volume24hInTrx"
        if sort == "number_holder":
            sort = "holderCount"

        order = order.lower()

        params = {"sort": sort, "order": order, "filter": token_type, "verifier": "all", "start_timestamp": None,
                  "end_timestamp": None}

        if token_type == "all":
            del params["filter"]

        address = self._API_TOKEN_LIST_ADDRESS
        req = SendRequestMultiple(address, save_live, save_path, params, max_query=2000)
        data = req.get_data_multiple(count, properties, TokenListDataMap, delete_order=False, data_key="tokens")
        return data
