from tron_explorer.data_map import DataMap

# noinspection PyAttributeOutsideInit
from tron_explorer.utils import SendRequestSingle, MiscUtils


# noinspection PyAttributeOutsideInit
class SrDataMap(DataMap):
    properties_dict = {"address": "address", "name": "name", "url": "url", "produced_total": "producedTotal"
        , "produced_percentage": "", "realtime_votes": "realTimeVotes", "change_votes": "changeVotes"
        , "votes_percentage": "votesPercentage", "annual_rate": "annualizedRate", "distribution": "", "rank": ""}

    """
        a DataMap type class that is responsible for filtering properties of SR data instances.

        :param data: the data instance.
        :type data: dict

        :param properties: properties of SR instance that will be returned. to see what properties are included see below
        :type properties: list

        :properties:

            * *address* (``str``)
                address of the SR account.
            * *name* (``str``)
               name of the SR.
            * *url* (``str``)
                SR's official website.
            * *produced_total* (``int``)
                numbers of blocks produced by this by the SR.
            * *produced_percentage* (``float``)
                percentage of blocks produced correctly by the SR.
            * *realtime_votes* (``int``)
                number of SR votes at this moment.
            * *change_votes* (``int``)
                change in number of the votes for since the last cycle.
            * *annual_rate* (``float``)
                annual profit rate for voters.
            * *distribution_ratio* (``list``)
                distribution of reward between voters and SR.(["voters","SR"])
            * *rank* (``int``)
                rank of SR based on number of votes.

        """

    def __init__(self, data, properties):
        super().__init__(data, properties)

    def filter_data(self):
        """
        filters data based on parameter properties.
        """

        self.CLASS_NAME = "SR"
        self.properties_list = self.properties_dict.keys()

        super().filter_data()
        data = self.data
        properties = self.check_properties()

        for p in properties:
            try:
                if self.properties_dict[p] == "":
                    if p == "produced_percentage":
                        if "producePercentage" in data:
                            setattr(self, p, data["producePercentage"])
                        else:
                            setattr(self, p, data["produceEfficiency"])
                    if p == "rank":
                        if "realTimeRanking" in data:
                            setattr(self, p, data["realTimeRanking"])
                        else:
                            setattr(self, p, data["index"])

                    if p == "distribution_rate":
                        setattr(self, p, [100 - data["brokerage"], data["brokerage"]])
                else:
                    setattr(self, p, data[self.properties_dict[p]])
            except KeyError:
                setattr(self, p, None)


# noinspection PyIncorrectDocstring
class SR:
    """
    instantiate an object that contains a methods for multiple request related to SRs.

    """

    _API_SINGLE_SR_ADDRESS = "/vote/witness"
    _API_SR_LIST_ADDRESS = "/pagewitness"

    @staticmethod
    def _check_list_params(sr_type):
        """
        checks list request params for exceptions.

        :param sort: type of sr.
        :type sort: str

        """

        if sr not in ["all", "sr", "sr_partner", "sr_candidate"]:
            raise ParameterException(ParameterException.SR_TYPE_EXCEPTION_MESSAGE, ["sr_type"])

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

        params = {"address": sr_address}
        req = SendRequestSingle(self._API_SINGLE_SR_ADDRESS, params)
        data = req.get_data()
        return SrDataMap(data["data"], properties)

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
        params = {}

        if sr_type == "sr":
            params["witnesstype"] = 1
        if sr_type == "sr_partner":
            params["witnesstype"] = 2
        if sr_type == "sr_candidate":
            params["witnesstype"] = 3
        if sr_type == "all":
            pass

        address = self._API_SR_LIST_ADDRESS
        req = SendRequestSingle(address, params)
        data = req.get_data()
        all_data = []
        for d in data["data"]:
            d_filtered = SrDataMap(d, properties)
            all_data.append(d_filtered.__dict__)

        return MiscUtils.dict_list_df(all_data)
