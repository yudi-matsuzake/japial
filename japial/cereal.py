# -*- coding: utf-8 -*-

import json
import jsonapi

import sqlalchemy.util.langhelpers
import sqlalchemy as sql

def check_key_or_default(obj, key, default):
    """returns the obj.key if the key exists or default otherwise"""
    return obj.__class__.__dict__[key] if key in obj.__class__.__dict__ else default

class Cereal(object):
    """Serializer from SQLalchemy orm base objects to json with jsonapi specification"""

    @staticmethod
    def module_and_class(obj):
        """returns module + '.' + class of an object"""
        return obj.__module__ + '.' + obj.__name__

    def __init__(self, base, namespace='/api', meta=None, links=None, jsonapi=None, included=None):
        """japial init"""

        self.base = base
        self.type_model_dict  = {}
        self.namespace = namespace
        self.meta = meta
        self.links = links
        self.jsonapi = jsonapi
        self.included = included

        for name, model in base._decl_class_registry.items():
            if name.startswith('_'):
                continue

            type = check_key_or_default(model, '__japial_type__', model.__tablename__)
            self.type_model_dict[type] = model

    def build_relationships(self, model):
        model_relationships  = model.__mapper__.relationships.items()
        is_a_list            = len(model_relationships) > 1
        buided_relationships = [] if is_a_list else {}

        # this model does not have a relationship
        if len(model_relationships) == 0:
            return None

        # there is a list of relationships?
        for key, r in model_relationships:
            resource = getattr(model, key)
            is_a_list_of_this_relation = isinstance(resource, list) and len(resource) > 1
            this_relation = [] if is_a_list_of_this_relation else None

            # there is a list of relations in this relationship?
            if is_a_list_of_this_relation:
                for relation in resource:
                    builded = self.build_sqlalchemy_model(relation, with_relationship=False)
                    this_relation.append(builded)
            else:
                if(isinstance(resource, list)):
                    this_relation = self.build_sqlalchemy_model(resource[0], with_relationship=False)
                else:
                    this_relation = self.build_sqlalchemy_model(resource, with_relationship=False)

            if is_a_list:
                build_relationships.append({ key : this_relation })
            else:
                build_relationships = { key : this_relation}

        return build_relationships

    def self_link(self, resource, namespace, id):
        """
        build and return the self link
        """
        self_link         = '{}{}' if namespace.endswith('/') else '{}/{}'
        self_link        += '{}' if resource.endswith('/') else '/{}'
        self_link         = self_link.format(namespace, resource, id)
        return self_link

    def build_sqlalchemy_model(self, model, with_relationship=True):
        """build a sqlalchemy model and returns a jsonapi formatted dictionary"""

        # define attributes
        all_fields    = filter(lambda k : not k.startswith('_'), model.__dict__.keys())
        fields        = check_key_or_default(model, '__japial_fields__', all_fields)
        id            = check_key_or_default(model, '__japial_id__', 'id')
        type          = check_key_or_default(model, '__japial_type__', model.__tablename__)
        meta          = check_key_or_default(model, '__japial_meta__', None)
        resource      = check_key_or_default(model, '__japial_resource__', model.__tablename__)
        namespace     = check_key_or_default(model, '__japial_namespace__', self.namespace)

        if with_relationship:
            with_relationship = check_key_or_default(model, '__japial_with_relationships__', with_relationship)

        # ignore fields for attributes
        ignored_by_default = { id }
        for k, r in model.__mapper__.relationships.items():
            for j in r.local_columns:
                ignored_by_default |= { j.name, k }
        ignore_fields = check_key_or_default(model, '__japial_ignore_fields__', ignored_by_default)
        fields = set(fields) - set(ignore_fields)

        # link
        links             = { "self" : self.self_link(resource, namespace, getattr(model, id)) }

        # relationships
        relationships = self.build_relationships(model) if with_relationship else None

        # build attributes
        attributes = {}
        for k in fields:
            attributes[k] = model.__dict__[k]

        # format
        resource_object = jsonapi.formatter.ResourceObject(
                                            id=model.__dict__[id],
                                            type=type,
                                            attributes=attributes,
                                            relationships=relationships,
                                            meta=meta,
                                            links=links)

        return resource_object.__jsonapi__()

    def decereal(self, str):
        """deserialize the json string and returns a sqlalchemy model or a list of it"""

        json_loaded = json.loads(str)

        json_data = json_loaded['data']

        is_a_list = isinstance(json_data, list)

        list_of_model = []

        if is_a_list:
            for i in json_data:
                model = self.type_model_dict[i['type']]
                new_obj = model(**i['attributes'])
                list_of_model.append(new_obj)
        else:
            model = self.type_model_dict[i['type']]
            new_obj = model.__new__(model.__class__, **i['attributes'])
            list_of_model.append(new_obj)

        return list_of_model

    def cereal(self, m, meta=None, jsonapi_attr=None, links=None, included=None):
        """serialize the model in sqlalchemy object and returns a json dictionary"""

        meta = meta or self.meta
        links = links or self.links
        jsonapi_attr = jsonapi_attr or self.jsonapi
        included = included or self.included

        m_is_list = isinstance(m, list)
        data = [] if m_is_list else {}

        if m_is_list:
            for model in m:
                builded = self.build_sqlalchemy_model(model)
                data.append(builded)
        else:
            builded = self.build_sqlalchemy_model(m)
            data = builded

        j = jsonapi.formatter.TopLevel(
                                data=data,
                                meta=meta,
                                jsonapi=jsonapi_attr,
                                included=included).__jsonapi__()

        return j

    def __call__(self, obj):

        # whether is json or sqlalchemy model
        if isinstance(obj, basestring):
            return self.decereal(obj)
        else:
            return self.cereal(obj)
