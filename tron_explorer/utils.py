import sys
from requests import get
import pandas as pd
from tron_explorer.exceptions import ParameterWarning, ParameterException


class SendRequestSingle:
    """
    sends get request to get one instance of data.

    :param address: The address of api segment to get data from.
    :type address: string

    :param params: parameters of api request
    :type params: dict

    :cvar BASE_API: base url of api.
    :type BASE_API: str

    """

    BASE_API = "https://apilist.tronscan.org/api"
    URL = ""

    def __init__(self, address, params: dict = None):
        self.address = address
        self.params = params
        self._add_address()

    def _add_address(self):

        """
        adds the address to base url.
        """

        self.URL = self.BASE_API + self.address

    def _param_builder(self):

        """
        removes potential None values in request params.
        """

        params = self.params.copy()
        for key, value in params.items():
            if value is None:
                del self.params[key]

    def _send_request(self):

        """
        sends get request and passes the data.

        :returns: the data returned by api.
        :rtype: dict
        """

        response = get(url=self.URL, params=self.params)
        data = response.json()
        return data

    def get_data(self):
        """
        creates the request and passes data.

        :returns: the data returned by api.
        :rtype: dict
        """
        self._add_address()
        self._param_builder()
        return self._send_request()


class SendRequestMultiple:
    """
    uses SendRequest class to get paginated data from queries with more than one instance.

    :param address: The address of used api segment.
    :type address: string

    :param params: parameters of api request.
    :type params: dict

    :param MAX: the maximum number of instances returned for a query.
    :type MAX: int

    :param save_live: if set to True the downloaded data will be saved to a file in each page downloaded
    to avoid losing data.
    :type save_live: bool

    :param save_path: path of folder that data is saved to.
    :type save_path: str

    :cvar LIMIT: the number of instances in each page of query.
    :type LIMIT: int

    """

    LIMIT = 50

    def __init__(self, address: str, save_live: bool, save_path: str, params: dict = None, max_query: int = 10000):
        self.MAX = max_query
        self.address = address
        self.params = params
        self.save_live = save_live
        self.save_path = save_path

    def _save_live(self, all_data):

        """
        saves data to csv file.
        """

        df = MiscUtils.dict_list_df(all_data)
        df.to_csv(self.save_path + "/query.csv")

    def _time_both(self, properties, data_map, data_key):
        """
        uses SendRequest class to get paginated data from multiple queries with more than one instance when both start
        and end time are specified, and return the combined data.

        :param properties: properties of instances that will be returned.
        :type properties: list

        :param data_map: the DataMap type class name that is responsible for filtering properties.
        :type data_map: DataMap

        :param data_key: the key to data segment of request result.
        :type data_key: str

        :returns: desired data instances.
        :rtype: list

        """

        all_data = []

        # getting data
        # one loop of while gets the maximum amount of instances in one query
        while True:
            self.params["start"] = 0
            # pagination
            while self.params["start"] <= self.MAX - self.LIMIT:
                data = SendRequestSingle(self.address, self.params).get_data()

                # when no more data exists return
                if len(data[data_key]) == 0:
                    return all_data

                for d in data[data_key]:
                    obj = data_map(d, properties)
                    # obj is data_map instance and will filter out properties
                    all_data.append(obj.__dict__)
                    # the return criteria depends on sort
                    if self.params["sort"] == "timestamp":
                        if d["timestamp"] > self.params["end_timestamp"]:
                            MiscUtils.progressbar(len(all_data))
                            return all_data
                    else:
                        if d["timestamp"] < self.params["start_timestamp"]:
                            MiscUtils.progressbar(len(all_data))
                            return all_data

                if self.save_live:
                    self._save_live(all_data)

                MiscUtils.progressbar(len(all_data))
                # go to next page of data
                self.params["start"] += self.LIMIT
            # creating a new query where previous one ended
            if self.params["sort"] == "timestamp":
                self.params["start_timestamp"] = all_data[-1]["timestamp"] + 1
            else:
                self.params["end_timestamp"] = all_data[-1]["timestamp"] - 1

    def _time_one(self, count, properties, data_map, side, data_key):
        """
        uses SendRequest class to get paginated data from multiple queries with more than one instance when start or end
        times are specified, and return the combined data.

        :param count: number of instances that will be returned.
        :type count: int

        :param properties: properties of instances that will be returned.
        :type properties: list

        :param data_map: the DataMap type class name that is responsible for filtering properties.
        :type data_map: DataMap

        :param data_key: the key to data segment of request result.
        :type data_key: str

        :param side: indicates which of start or end time is specified.
        :type side: str

        :returns: desired data instances.
        :rtype: list

        """

        all_data = []
        # getting data
        # one loop of while gets the maximum amount of instances in one query
        while True:
            self.params["start"] = 0
            # pagination
            while self.params["start"] <= self.MAX - self.LIMIT:
                data = SendRequestSingle(self.address, self.params).get_data()

                # when no more data exists return
                if len(data[data_key]) == 0:
                    return all_data

                for d in data[data_key]:
                    obj = data_map(d, properties)
                    # obj is data_map instance and will filter out properties
                    all_data.append(obj.__dict__)
                    # if enough there are enough instances return
                    if len(all_data) >= count:
                        MiscUtils.progressbar(len(all_data), count)
                        return all_data

                if self.save_live:
                    self._save_live(all_data)

                MiscUtils.progressbar(len(all_data), count)
                # go to no next page of data
                self.params["start"] += self.LIMIT

            # creating a new query where previous one ended
            if side == "start":
                self.params["start_timestamp"] = all_data[-1]["timestamp"] + 1
            else:
                self.params["end_timestamp"] = all_data[-1]["timestamp"] - 1

    def _time_none(self, count, properties, data_map, data_key):
        """
        uses SendRequest class to get paginated data from multiple queries with more than one instance when none
        of start or end times are specified.

        :param count: number of instances that will be returned.
        :type count: int

        :param properties: properties of instances that will be returned.
        :type properties: list

        :param data_key: the key to data segment of request result.
        :type data_key: str

        :param data_map: the DataMap type class name that is responsible for filtering properties.
        :type data_map: DataMap

        :returns: desired data instances.
        :rtype: list

        """

        all_data = []

        # getting data
        # one loop of while gets the maximum amount of instances in one query
        while True:
            self.params["start"] = 0
            # pagination
            while self.params["start"] <= self.MAX - self.LIMIT:
                data = SendRequestSingle(self.address, self.params).get_data()
                # when no more data exists return
                if len(data[data_key]) == 0:
                    return all_data

                for d in data[data_key]:
                    obj = data_map(d, properties)
                    # obj is data_map instance and will filter out properties
                    all_data.append(obj.__dict__)
                    # if enough there are enough instances return
                    if len(all_data) >= count:
                        MiscUtils.progressbar(len(all_data), count)
                        return all_data

                if self.save_live:
                    self._save_live(all_data)

                MiscUtils.progressbar(len(all_data), count)
                # go to no next page of data
                self.params["start"] += self.LIMIT
            # creating a new query where previous one ended
            self.params["end_timestamp"] = all_data[-1]["timestamp"] + 1000

    @staticmethod
    def _check_list_params(start_timestamp: int, end_timestamp: int, order: str, count: int, delete_order):
        """
        checks list request params for exceptions.

        :param start_timestamp: start timestamp for query. (in milliseconds)
        :type order: int

        :param end_timestamp: end timestamp for query. (in milliseconds)
        :type order: int

        :param order: the order of blocks by time.
        :type order: str

        :param delete_order: whether if order param should be removed before sending request.
        :type delete_order: bool

        :raise: ParameterException

        """
        # time parameters
        try:
            if start_timestamp > end_timestamp:
                raise ParameterException(ParameterException.TIME_EXCEPTION_BIGGER_MESSAGE,
                                         ["start_timestamp", "end_timestamp"])
        except TypeError:
            pass

        try:
            if start_timestamp < 0:
                raise ParameterException(ParameterException.TIME_EXCEPTION_NEGATIVE_MESSAGE, ["start_timestamp"])
        except TypeError:
            pass

        try:
            if end_timestamp < 0:
                raise ParameterException(ParameterException.TIME_EXCEPTION_NEGATIVE_MESSAGE, ["end_timestamp"])
        except TypeError:
            pass

        if len(str(start_timestamp)) < 13:
            ParameterWarning(ParameterWarning.TIME_WARNING_MESSAGE, '"start_timestamp"')

        if len(str(end_timestamp)) < 13:
            ParameterWarning(ParameterWarning.TIME_WARNING_MESSAGE, '"end_timestamp"')

        # order
        if delete_order:
            if order != "ASC" and order != "DESC" and order is not None:
                raise ParameterException(ParameterException.ORDER_EXCEPTION_MESSAGE, ["order"])

        if count <= 0:
            raise ParameterException(ParameterException.ORDER_EXCEPTION_MESSAGE, ["count"])

    def _build_params(self, count: int, order: str, sort: str, delete_order):
        """
        make full request params.

        :param count: number of instances that will be returned.
        :type count: int

        :param order: the order of blocks by sort.
        :type order: str

        :param sort: the property that data is ordered by.
        :type sort: str

        :param delete_order: whether if order param should be removed before sending request.
        :type delete_order: bool

        """

        # if desired number of instances is less than default instance limit of query, then the limit is same is desired
        # number of instances
        if self.LIMIT > count:
            self.LIMIT = count

        # setting request params
        self.params["limit"] = self.LIMIT

        if delete_order:
            if order == "DESC":
                self.params["sort"] = "-" + sort

            del self.params["order"]

    def get_data_multiple(self, count: int, properties: list, data_map, delete_order: bool = True,
                          data_key: str = "data"):

        """
        determines which of the data gathering methods should be used based on start or end time parameters.

        :param data_key: the key to data segment of request result.
        :type data_key: str

        :param count: number of instances that will be returned.
        :type count: int

        :param properties: properties of instances that will be returned.
        :type properties: list

        :param data_map: the DataMap type class name that is responsible for filtering properties.
        :type data_map: DataMap

        :param delete_order: whether if order param should be removed before sending request.
        :type delete_order: bool

        :returns: a panda dataframe containing data of desired data instances.
        :rtype: Pandas Dataframe


        """

        start_timestamp = self.params["start_timestamp"]
        end_timestamp = self.params["end_timestamp"]
        order = self.params["order"]
        sort = self.params["sort"]

        self._check_list_params(start_timestamp, end_timestamp, order, count, delete_order)
        self._build_params(count, order, sort, delete_order)

        if start_timestamp is not None and end_timestamp is not None:
            if count != self.MAX:
                ParameterWarning(ParameterWarning.COUNT_WARNING_MESSAGE, '"count"').warn()
            all_data = self._time_both(properties, data_map, data_key)
            print("\n")
            return MiscUtils.dict_list_df(all_data)

        if start_timestamp is not None and end_timestamp is None:
            # if order is not None:
            # ParameterWarning(ParameterWarning.ORDER_WARNING_MESSAGE, '"order"').warn()
            all_data = self._time_one(count, properties, data_map, "start", data_key)
            print("\n")
            return MiscUtils.dict_list_df(all_data)

        if start_timestamp is None and end_timestamp is not None:
            # if order is not None:
            # ParameterWarning(ParameterWarning.ORDER_WARNING_MESSAGE, '"order"').warn()
            all_data = self._time_one(count, properties, data_map, "end", data_key)
            print("\n")
            return MiscUtils.dict_list_df(all_data)

        if start_timestamp is None and end_timestamp is None:
            all_data = self._time_none(count, properties, data_map, data_key)
            print("\n")
            return MiscUtils.dict_list_df(all_data)


class MiscUtils:
    @staticmethod
    def progressbar(done, full=None, prefix="Downloaded"):
        if full is None:
            prog = (prefix + " " + str(done))
            sys.stdout.write('\r' + prog)
        else:
            prog = (prefix + " " + str(done) + "/" + str(full))
            sys.stdout.write('\r' + prog)

    @staticmethod
    def dict_list_df(data):
        return pd.DataFrame(data)
