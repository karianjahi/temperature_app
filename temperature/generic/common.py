import json

from django.shortcuts import get_object_or_404

from temperature.config import config
from temperature.lib.serializer import save_serializer_id
from temperature.responses.resp import errorResp, errorRespStatusCode
from temperature.responses.resp import successResp

class GenericDetail(object):
    def __init__(self, model, deserializer, id):
        self.model = model
        self.deserializer = deserializer
        self.id = id

    def detail_get(self):

        obj = get_object_or_404(self.model, id=self.id)
        dese = self.deserializer(obj)
        return successResp(dese.data)


class GenericList(object):
    def __init__(self, model, deserializer=None, serializer=None, id=None, data={}):
        self.model = model
        self.deserializer = deserializer
        self.serializer = serializer
        self.id = id
        self.data = data

    def handle_filter_name(self, name):
        queryset = self.model.objects.filter(name__contains=name)
        deserialized_data = (self.deserializer(queryset, many=True)).data
        return successResp(deserialized_data)

    def handle_filter_id(self, ids_to_search: [int]):
        ids = [r.id for r in self.model.objects.all()]
        available_ids = [i for i in ids if i in ids_to_search]

        results = []
        for id in available_ids:
            rd = self.model.objects.get(id=id)
            rd_deserializer = self.deserializer(rd)
            results.append(rd_deserializer.data)

        return successResp(results)

    def list_get(self, request):
        def convert_to_maybe_int(param: str):
            if param is None:
                return None
            else:
                return int(param)


        filter_name = request.query_params.get('filter[name]')
        if filter_name is not None:
            return self.handle_filter_name(filter_name)

        filter_ids = request.query_params.get('filter[ids]')
        if filter_ids is not None:
            filter_ids = json.loads(filter_ids)
            return self.handle_filter_id(filter_ids)

        param_from = convert_to_maybe_int(request.query_params.get('from'))
        param_limit = convert_to_maybe_int(request.query_params.get('limit'))

        if param_from is None and param_limit is not None:
            return errorResp(config.err_msg_from_should_exist)
        if param_limit is None and param_from is not None:
            return errorResp(config.err_msg_limit_should_exist)
        else:
            db_objs = self.model.objects.all()
            deserializer_db = self.deserializer(db_objs, many=True)

            if param_from is None and param_limit is None:
                if len(deserializer_db.data) > config.default_limit:
                    return successResp(deserializer_db.data[:config.default_limit])
                else:
                    return successResp(deserializer_db.data[:])
            else:
                assert (param_from >= 0)
                assert (param_limit >= 0)
                if param_from > len(deserializer_db.data):
                    return errorResp(config.err_msg_from_should_not_excced_number_of_models)
                try:
                    return successResp(data=deserializer_db.data[param_from:param_from + param_limit])
                except IndexError:
                    return successResp(data=deserializer_db.data[param_from:])

    def serialize_data(self):
        id = save_serializer_id(self.serializer, self.data)
        saved_model = self.model.get_by_pk(id)
        dese = self.deserializer(saved_model)
        return dese.data

    def serialize(self, schema_name):
        id = save_serializer_id(self.serializer, self.data)
        saved_model = self.model.get_by_pk(id)
        dese = self.deserializer(saved_model)

        return successResp(dese.data)
