from tron_explorer.data_map import DataMap

# noinspection PyAttributeOutsideInit
from tron_explorer.utils import SendRequestMultiple, SendRequestSingle


# noinspection PyAttributeOutsideInit
class ProposalsDataMap(DataMap):
    properties_dict = {"proposal_id": "proposalId", "proposer_address": "", "proposal_hash": "proposalHash"
        , "network_parameter": "parameters", "timestamp_expiration": "expirationTime"
        , "timestamp_creation": "createTime", "total_votes": "totalVotes"
        , "valid_votes": "validVotes", "votes": ""}
    """
    a DataMap type class that is responsible for filtering properties of proposal data instances.

    :param data: the data instance.
    :type data: dict

    :param properties: properties of proposal instance that will be returned. to see what properties are included see below
    :type properties: list

    :properties:

        * *proposal_id* (``str``)
            id of proposal.
        * *proposer_address* (``str``)
            proposer account address.
        * *proposal_hash* (``str``)
            hash of proposal.
        * *network_parameter* (``list``)
            list of proposed parameters to changed (key) and proposed new value (value).["key","value"]
        * *timestamp_expiration* (``int``)
            creation timestamp of proposal.
        * *timestamp_expiration* (``int``)
            expiration timestamp of proposal.
        * *total_votes* (``int``)
            total number of votes on proposal.
        * *total_votes* (``int``)
            number of valid votes on proposal.
        * *total_votes* (``votes``)
            number of approvals and vetos. ["approvals","veto"]
    """

    # never initiated directly. its here only because of documentation.
    def __init__(self, data, properties):
        super().__init__(data, properties)

    def filter_data(self):
        """
        filters data based on parameter properties.
        """

        self.properties_list = self.properties_dict.keys()
        self.CLASS_NAME = "Proposal"

        super().filter_data()
        data = self.data
        properties = self.check_properties()

        for p in properties:
            try:
                if p == "proposer_address" or p == "votes":
                    if p == "proposer_address":
                        setattr(self, p, data["proposer"]["address"])
                    else:
                        setattr(self, p, [len(data["approvals"]), len(data["veto"])])
                else:
                    setattr(self, p, data[self.properties_dict[p]])
            except KeyError:
                setattr(self, p, None)


class Proposals:
    """
    instantiate an object that contains a methods for multiple request related to proposals.
    """

    _API_PROPOSAL_ADDRESS = "/proposal"
    _API_PARAMETERS_ADDRESS = "/chainparameters"

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

        params = {"start_timestamp": None, "end_timestamp": None, "order": "DESC", "sort": "timestamp"}

        address = self._API_PROPOSAL_ADDRESS
        req = SendRequestMultiple(address, save_live, save_path, params, max_query=2000)
        data = req.get_data_multiple(count, properties, ProposalsDataMap)
        return data

    def get_list_network_parameters(self):
        """
        get data for a list of network parameters.

        :returns: a list containing network parameters and their current value.
        :rtype: list

        """

        params = {}
        req = SendRequestSingle(self._API_PARAMETERS_ADDRESS, params)
        data = req.get_data()
        return data["tronParameters"]
