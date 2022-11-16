from tron_explorer.account import Account, AccountDataMap
from tron_explorer.block import Block, BlockDataMap
from tron_explorer.proposals import Proposals, ProposalsDataMap
from tron_explorer.smart_contract import SmartContract, SmartContractDataMap
from tron_explorer.sr import SR, SrDataMap
from tron_explorer.token_list import TokenList, TokenListDataMap
from tron_explorer.token_single import TokenSingle, TokenSingleDataMap
from tron_explorer.transaction import Transaction, TransactionDataMap


# noinspection PyIncorrectDocstring
class Explore:
    """
    instantiate an object that contains methods for all requests.
    """

    def __init__(self):
        self.account = Account()
        self.block = Block()
        self.proposals = Proposals()
        self.smart_contracts = SmartContract()
        self.sr = SR()
        self.token_single = TokenSingle()
        self.token_list = TokenList()
        self.transaction = Transaction()

    @staticmethod
    def get_account_properties():

        """
        get available properties for accounts.

        :return: list of properties
        :rtype: list
        """

        return list(AccountDataMap.properties_dict.keys())

    @staticmethod
    def get_block_properties():

        """
        get available properties for blocks.

        :return: list of properties
        :rtype: list
        """

        return list(BlockDataMap.properties_dict.keys())

    @staticmethod
    def get_proposals_properties():
        """
        get available properties for proposals.

        :return: list of properties
        :rtype: list
        """

        return list(ProposalsDataMap.properties_dict.keys())

    @staticmethod
    def get_smart_contract_properties():
        """
        get available properties for smart contracts.

        :return: list of properties
        :rtype: list
        """
        return list(SmartContractDataMap.properties_list)

    @staticmethod
    def get_sr_properties():
        """
        get available properties for sr.

        :return: list of properties
        :rtype: list
        """
        return list(SrDataMap.properties_dict.keys())

    @staticmethod
    def get_transaction_properties():
        """
        get available properties for transaction.

        :return: list of properties
        :rtype: list
        """
        return list(TransactionDataMap.properties_list)

    @staticmethod
    def get_token_single_properties_trc10():
        """
        get available properties for single token query (trc10).

        :return: list of properties
        :rtype: list
        """
        return list(TokenSingleDataMap.properties_dict_trc10.keys())

    @staticmethod
    def get_token_single_properties_trc20():
        """
        get available properties for single token query (trc20).

        :return: list of properties
        :rtype: list
        """
        return list(TokenSingleDataMap.properties_dict_trc20.keys())

    @staticmethod
    def get_token_list_properties():
        """
        get available properties for list token query.

        :return: list of properties
        :rtype: list
        """
        return list(TokenListDataMap.properties_dict.keys())

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

        return self.account.get_account(account_address, properties)

    def get_account_list(self
                         , save_live: bool = False
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

        return self.account.get_account_list(save_live, save_path, sort, order, properties, count)

    def get_account_analysis(self, type_: str, account_address: str, start_timestamp: int = 1):
        """
        get analysis for an account.

        :param type_: indicates type of analysis.
                      balance: balance analysis
                      token_transfer: token transfer analysis
                      energy: energy usage analysis
                      bandwidth: bandwidth usage analysis
        :type type_: int

        :param account_address: address of desired account.
        :type account_address: str

        :args:
            * *start_timestamp* (``int``)
                start timestamp of query. default is 1 (for this specific query input 0 returns only 100 items). (milliseconds)

        :returns: a panda dataframe containing data of desired accounts.
        :rtype: Pandas Dataframe

        """
        type_dict = {"balance": 0, "token_transfer": 1, "energy": 2, "bandwidth": 3}
        return self.account.get_account_analysis(type_dict[type_], account_address, start_timestamp)

    def get_latest_block(self, properties: list = None):
        """
        get the latest block data.

        :args:
            * *properties* (``list``)
                properties of blocks that will be returned. default is all.

        :returns: the latest block data.
        :rtype: BlockDataMap

        """

        return self.block.get_latest_block(properties)

    def get_block(self, number: int, properties: list = None):
        """
        get a specific block.

        :param number: the number of desired block.
        :type number: int

        :args:
            * *properties* (``list``)
                properties of blocks that will be returned. default is all.

        :returns: the desired block data.
        :rtype: BlockDataMap

        """

        return self.block.get_block(number, properties)

    def get_block_list(self, start_timestamp: int = None
                       , end_timestamp: int = None
                       , save_live: bool = False
                       , save_path: str = ""
                       , order: str = "DESC"
                       , properties: list = None
                       , count: int = 10000):
        r"""
        get multiple blocks data.

        :args:
            * *start_timestamp* (``int``)
                start timestamp of query. default is None. (milliseconds)
            * *end_timestamp* (``int``)
                end timestamp of query. default is None. (milliseconds)
            * *properties* (``list``)
                properties of blocks that will be returned. default is all.
            * *order* (``str``)
                order of blocks by time ("ASC" : Ascending , "DESC" : descending).
            * *count* (``int``)
                number of desired blocks. default is 10000. is ignored when both times are specified.
            * *save_live* (``bool``)
                if set to True the downloaded data will be saved to a file in each page downloaded to avoid losing data
                in case of an error.
            * *save_path* (``str``)
                path of folder that data is saved to. default is ""

        :returns: a panda dataframe containing data of desired blocks.
        :rtype: Pandas Dataframe

        """

        return self.block.get_block_list(start_timestamp, end_timestamp
                                         , save_live, save_path, order, properties, count)

    def get_list_proposals(self, save_live: bool = False
                           , save_path: str = ""
                           , properties: list = None
                           , count: int = 100
                           ):
        """
        get data for a list of proposals.

        :args:
            * *properties* (``list``)
                properties of proposals that will be returned. default is all.
            * *count* (``int``)
                number of desired proposals. default is 100. is ignored when both times are specified.
            * *save_live* (``bool``)
                if set to True the downloaded data will be saved to a file in each page downloaded to avoid losing data
                in case of an error.
            * *save_path* (``str``)
                path of folder that data is saved to. default is ""

        :returns: a panda dataframe containing data of desired proposals.
        :rtype: Pandas Dataframe

        """

        return self.proposals.get_list_proposals(save_live, save_path, properties, count)

    def get_list_network_parameters(self):
        """
        get data for a list of network parameters.

        :returns: a list containing network parameters and their current value.
        :rtype: list

        """

        return self.proposals.get_list_network_parameters()

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

        return self.smart_contracts.get_smart_contract(contract_address, properties)

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

        return self.smart_contracts.get_smart_contract_list_blockchain(
            start_timestamp, end_timestamp, save_live, save_path
            , sort, order, properties, count, verified_only, open_source_only)

    def get_sr(self, sr_address: str, properties: list = None):
        """
        get a specific SR.

        :param sr_address: the number of desired block.
        :type sr_address: str

        :args:
            * *properties* (``list``)
                properties of blocks that will be returned. default is all.

        :returns: the desired block data.
        :rtype: BlockDataMap

        """

        return self.sr.get_sr(sr_address, properties)

    def get_sr_list(self, sr_type: str = "all", properties: list = None):
        r"""
        get multiple SR data.

        :args:
            * *sr_type* (``int``)
                all : returns all SRs.
                sr : returns only SR.
                sr_partners : returns only SR partners.
                sr_candidates : returns only SR candidates.
                default is all.

        :returns: a panda dataframe containing data of desired blocks.
        :rtype: Pandas Dataframe

        """

        return self.sr.get_sr_list(sr_type, properties)

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

        return self.transaction.get_transaction(hash_, properties)

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

        return self.transaction.get_transaction_list_block(number, save_live, save_path, order, properties, count)

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

        return self.transaction.get_transaction_list_account(address, save_live, save_path, order, properties, count)

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

        return self.transaction.get_transaction_list_blockchain(start_timestamp, end_timestamp, save_live, save_path
                                                                , order, properties, count)

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

        return self.token_list.get_token_list(save_live, save_path, sort, order, properties, count, token_type)

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

        return self.token_single.get_trc10_token(token_id, properties)

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

        return self.token_single.get_trc20_token(contract_address, properties)