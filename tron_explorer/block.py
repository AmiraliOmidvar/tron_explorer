from tron_explorer.utils import SendRequestSingle, SendRequestMultiple
from tron_explorer.data_map import DataMap


# noinspection PyAttributeOutsideInit
class BlockDataMap(DataMap):
    properties_dict = {"number": "number", "hash": "hash", "parent_hash": "parentHash"
        , "timestamp": "timestamp", "size": "size"
        , "confirmed": "confirmed", "number_of_transactions": "nrOfTrx"
        , "block_reward": "blockReward", "bandwidth_used": "netUsage"
        , "energy_used": "energyUsage", "sr_address": "witnessAddress"
        , "sr_name": "witnessName"}
    """
    a DataMap type class that is responsible for filtering properties of block data instances.

    :param data: the data instance.
    :type data: dict

    :param properties: properties of block instance that will be returned. to see what properties are included see below
    :type properties: list

    :properties:

        * *number* (``int``)
            number of the block.
        * *hash* (``str``)
           hash of the block.
        * *parent_hash* (``str``)
            hash of the parent block of this one.
        * *timestamp* (``int``)
            timestamp of the block creation. (milliseconds)
        * *size* (``int``)
            size of the block in bytes.
        * *confirmed* (``bool``)
            whether if the block is confirmed or not.
        * *number_of_transactions* (``int``)
            number of transactions in the block.
        * *block_reward* (``float``)
            number of tokens awarded to producer of the block. (trx)
        * *bandwidth_used* (``float``)
            amount of bandwidth used to create the block.
        * *energy_used* (``float``)
            amount of energy used to create the block.
        * *sr_name* (``str``)
            name of the super representative that produced the block.
        * *sr_address* (``str``)
            address of the super representative that produced the block.


    """

    def __init__(self, data, properties):
        super().__init__(data, properties)

    def filter_data(self):

        """
        filters data based on parameter properties.

        """

        self.properties_list = self.properties_dict.keys()
        self.CLASS_NAME = "Block"

        super().filter_data()
        data = self.data
        properties = self.check_properties()

        for p in properties:
            try:
                setattr(self, p, data[self.properties_dict[p]])
            except KeyError:
                setattr(self, p , None)


# noinspection PyIncorrectDocstring
class Block:
    """
    instantiate an object that contains methods for multiple request related to blocks.

    """

    _API_BLOCK_LATEST_ADDRESS = "/block/latest"
    _API_BLOCK_ADDRESS = "/block"

    def __init__(self):
        pass

    def _get_latest_block_number(self):
        """
        get the latest block number.

        :returns: the latest block number.
        :rtype: int

        """
        properties = ["number"]
        params = {}
        address = self._API_BLOCK_LATEST_ADDRESS
        req = SendRequestSingle(address, params)
        data = req.get_data()
        block_latest = BlockDataMap(data, properties)
        return block_latest.number

    def get_latest_block(self, properties: list = None):
        """
        get the latest block data.

        :args:
            * *properties* (``list``) 
                properties of blocks that will be returned. default is all.

        :returns: the latest block data.
        :rtype: BlockDataMap

        """

        number = self._get_latest_block_number()
        address = self._API_BLOCK_ADDRESS
        params = {"number": number}
        req = SendRequestSingle(address, params)
        data = req.get_data()
        return BlockDataMap(data["data"][0], properties)

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

        params = {"number": number}
        req = SendRequestSingle(self._API_BLOCK_ADDRESS, params)
        data = req.get_data()
        return BlockDataMap(data["data"][0], properties)

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

        params = {"start_timestamp": start_timestamp, "end_timestamp": end_timestamp,
                  "order": order, "sort": "timestamp"}

        address = self._API_BLOCK_ADDRESS
        req = SendRequestMultiple(address, save_live, save_path, params, max_query=10000)
        data = req.get_data_multiple(count, properties, BlockDataMap)
        return data
