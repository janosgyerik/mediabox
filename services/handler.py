# Portions of this code comes from the Oct09 project
# developed by the Moffitt Cancer Center.
# License: http://bitbucket.org/oct09/main/src/tip/COPYING
# Project: http://bitbucket.org/oct09/main/wiki/Home

from django.db.models import Model
from django.http import HttpResponse
from django.forms.fields import EMPTY_VALUES
from django.utils import simplejson
import re
import decimal


def service_error(msg):
    return HttpResponse(encode_error(msg), status=500)


def list_service(data, request, include=None, exclude=None, limit=None):
    if request.method == "GET":
        return HttpResponse(encode(data, include, exclude), mimetype=get_mimetype())

    elif request.method == "POST":
        return HttpResponse(encode_error("Write operations are not supported"), status=403)

    return HttpResponse(encode_error("%s Not Implemented" % request.method), status=501)


def query_set_service(query_set, request, include=None, exclude=None, limit=None):
    if request.method == "GET":
        collection = list(query_set)
        return HttpResponse(encode(collection, include, exclude), mimetype=get_mimetype())

    elif request.method == "POST":
        return HttpResponse(encode_error("Write operations are not supported"), status=403)

    return HttpResponse(encode_error("%s Not Implemented" % request.method), status=501)


def model_service(model, request, url, include=None, exclude=None, limit=None):
    (instance_id, rem_url) = get_model_id(request, url)

    try:
        if instance_id is not None and instance_id != '':
            return model_entity(model, request, url, include, exclude, limit)
        else:
            return model_collection(model, request, url, include, exclude, limit)
    except Exception as e:
        return HttpResponse(encode_error(e), status=500)


def model_entity(model, request, url, include=None, exclude=None, limit=None):
    (entity_id, rem_url) = get_model_id(request, url)

    try:
        if limit:
            entity = model.objects.filter(**limit).get(pk=entity_id)
        else:
            entity = model.objects.get(pk=entity_id)
    except:
        return HttpResponse(encode_error("Entity not found"), status=404)

    # Otherwise process the entity request
    if request.method == "GET":
        return HttpResponse(encode(entity, include, exclude), mimetype=get_mimetype())

    elif request.method == "PUT":
        return HttpResponse(encode_error("Write operations are not supported"), status=403)

    elif request.method == "DELETE":
        return HttpResponse(encode_error("Write operations are not supported"), status=403)

    return HttpResponse(encode_error("%s Not Implemented" % request.method), status=501)


def model_collection(model, request, url, include=None, exclude=None, limit=None):
    if request.method == "GET":
        results = do_search(model, request.GET, include, exclude, limit)

        collection = list(results)
        return HttpResponse(encode(collection, include, exclude), mimetype=get_mimetype())

    elif request.method == "POST":
        return HttpResponse(encode_error("Write operations are not supported"), status=403)

    return HttpResponse(encode_error("%s Not Implemented" % request.method), status=501)


def do_search(model, request, include=None, exclude=None, limit=None):
    search_fields = include
    if search_fields is None:
        search_fields = [f.name for f in model._meta.local_fields + model._meta.many_to_many if not f.name.endswith("_ptr")]
    if exclude is not None:
        search_fields = [f for f in search_fields if f not in exclude]
    search_values = dict([(str(key), value) for (key, value) in request.items()])

    results = model.objects.filter(**search_values)
    if limit:
        results = results.filter(**limit)

    if '_sortby' in request and request['_sortby'] not in EMPTY_VALUES:
        results = results.order_by(request.get('_sortby'))
    return results


def get_model_id(request, url):
    instance_id = None
    rem_url = None
    if url is not None and len(url) > 0:
        m = re.match(r"^([^/]+)/?(.*)", url)

        if m is not None:
            instance_id = m.group(1)
            rem_url = m.group(2)
    return (instance_id, rem_url)


def encode(entity, include=None, exclude=None):
    json = JSONEncoder(include, exclude)
    return json.encode(entity)


def decode(klass, entity, request, url=None):
    return request.raw_post_data


def get_mimetype():
    return "application/json"


def encode_error(error):
    json = JSONEncoder()
    return json.encode({'error': unicode(error)})


class JSONEncoder(simplejson.JSONEncoder):

    def __init__(self, include=None, exclude=None):
        self.include = include
        self.exclude = exclude
        super(JSONEncoder, self).__init__()

    def get_field_value(self, o, field):
        f = getattr(o, field)
        try:
            if isinstance(f, Model):
                if hasattr(f, 'pk'):
                    return self.default(f.pk)
                else:
                    return None
            if isinstance(f, decimal.Decimal):
                return o._meta.get_field_by_name(field)[0]._format(f)
            else:
                return self.default(f)
        except Exception:
            return None

    def default(self, o=None):

        if isinstance(o, Model):
            model_fields = self.include
            if model_fields is None:
                model_fields = [f.name for f in o._meta.fields + o._meta.many_to_many if not f.name.endswith("_ptr")]
            if self.exclude is not None:
                model_fields = [f for f in model_fields if f not in self.exclude]
            d = dict([(field, self.get_field_value(o, field)) for field in model_fields])
            return d
        elif o.__class__.__name__ == 'ManyRelatedManager' or o.__class__.__name__ == 'RelatedManager':
            return [r.pk for r in o.all()]
        elif isinstance(o, (int, long, float)):
            return o
        elif o is None:
            return None
        return unicode(o)
