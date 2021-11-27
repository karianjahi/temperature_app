class JsonResponses:
    def __init__(self,
                 name, # a string
                 description,  # a string
                 raw_dataset_ids,  # a list
                 no_of_clusters,  # an integer
                 channel_ids,  # an integer
                 cluster_ids,  # an integer
                 channel_sizes,  # a float
                 channel_reversed,  # a flag
                 errors):  # a list
        self.name = name
        self.description = description
        self.raw_dataset_ids = raw_dataset_ids
        self.no_of_clusters = no_of_clusters
        self.channel_ids = channel_ids
        self.cluster_ids = cluster_ids
        self.channel_sizes = channel_sizes
        self.channel_reversed = channel_reversed
        self.errors = errors

    def successful_json_response(self):
        Response = {"message": "success"}
        data = {}
        data["name"] = self.name
        data["description"] =self.description
        data["raw_dataset_ids"] = self.raw_dataset_ids
        data["no_of_clusters"] = self.no_of_clusters
        channels = []
        for ichannel in range(len(self.channel_ids)):
            channels.append({"channel_id": self.channel_ids[ichannel],
                             "cluster_id": self.cluster_ids[ichannel],
                             "channel_size": self.channel_sizes[ichannel],
                             "channel_reversed": self.channel_reversed[ichannel]})
        data["channels"] = channels
        Response["data"] = data
        Response["errors"] = self.errors
        return Response
    def unsuccessful_json_response(self):
        return {"message": "failed", "data":{}}