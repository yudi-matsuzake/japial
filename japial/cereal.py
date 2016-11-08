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

    def __init__(self, base, session_factory, namespace='/api', meta=None, links=None, jsonapi=None, included=None):
        """japial init"""

        self.base = base
        self.type_model_dict  = {}
        self.namespace = namespace
        self.meta = meta
        self.links = links
        self.jsonapi = jsonapi
        self.included = included
        self.session_factory = session_factory

        for name, model in base._decl_class_registry.items():
            if name.startswith('_'):
                continue

            type = check_key_or_default(model, '__japial_type__', model.__tablename__)
            self.type_model_dict[type] = model

    def build_relationships(self, model):
        model_relationships  = model.__mapper__.relationships.items()
        is_a_list            = len(model_relationships) > 1
        builded_relationships = {}

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
                    builded = self.build_sqlalchemy_model(relation, is_relationship=True)
                    this_relation.append(builded)
            else:
                if isinstance(resource, list):
                    if len(resource) > 0:
                        this_relation = self.build_sqlalchemy_model(resource[0], is_relationship=True)
                    else:
                        this_relation = None
                else:
                    this_relation = self.build_sqlalchemy_model(resource, is_relationship=True)

            builded_relationships[key] = this_relation

        return builded_relationships

    def self_link(self, resource, namespace, id):
        """
        build and return the self link
        """
        self_link         = '{}{}' if namespace.endswith('/') else '{}/{}'
        self_link        += '{}' if resource.endswith('/') else '/{}'
        self_link         = self_link.format(namespace, resource, id)
        return self_link

    def build_sqlalchemy_model(self, model, is_relationship=False, with_relationship=True):
        """build a sqlalchemy model and returns a jsonapi formatted dictionary"""

        # define attributes
        all_fields    = filter(lambda k : not k.startswith('_'), model.__dict__.keys())
        fields        = check_key_or_default(model, '__japial_fields__', all_fields)
        id            = check_key_or_default(model, '__japial_id__', 'id')
        type          = check_key_or_default(model, '__japial_type__', model.__tablename__)
        meta          = check_key_or_default(model, '__japial_meta__', None)
        resource      = check_key_or_default(model, '__japial_resource__', model.__tablename__)
        namespace     = check_key_or_default(model, '__japial_namespace__', self.namespace)

        if not is_relationship and with_relationship:
            with_relationship = check_key_or_default(model, '__japial_with_relationships__', with_relationship)
        else:
            with_relationship = False

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
        if not is_relationship and with_relationship: 
            relationships = self.build_relationships(model)

        # build attributes
        attributes = {}
        for k in fields:
            attributes[k] = getattr(model, k)

        resource_id = getattr(model, id)
        no_id = resource_id == None

        # format
        if is_relationship:
            resource_object = jsonapi.formatter.RelationshipObject(
                                            id=resource_id,
                                            type=type,
                                            attributes=attributes,
                                            meta=meta,
                                            links=links)

        else:
            resource_object = jsonapi.formatter.ResourceObject(
                                            id=resource_id,
                                            type=type,
                                            attributes=attributes,
                                            relationships=relationships,
                                            meta=meta,
                                            links=links,
                                            no_id=no_id)

        return resource_object.__jsonapi__()

    def fetch_element_by_id(self, model, id):
        session = self.session_factory()
        element = session.query(model).get(id)
        session.expunge(element)
        session.close()
        return element

    def decereal_jsonapi_object(self, json_obj):
        """
        Receive an json object with type in `type_model_dict` and returns the
        appropriate sqlalchemy model
        """

        model = self.type_model_dict[json_obj['type']]
        new_obj = model(**json_obj['attributes'])

        # there is any relationship?
        if 'relationships' in json_obj:

            relation_dict = json_obj['relationships']
            for key, value in relation_dict.items():
                if not key.startswith('_'):
                    is_list_of_relation = isinstance(value, list)

                    # TODO: elegantly remove the following code redundancy
                    #       when create new_relation
                    # the relationship uses list?
                    if model.__mapper__.relationships[key].uselist:
                        setattr(new_obj, key, [])

                        if is_list_of_relation:
                            for relation in value:
                                relation_data = relation['data']
                                relation_model = self.type_model_dict[relation_data['type']]
                                new_relation = self.fetch_element_by_id(relation_model, relation_data['id'])
                                getattr(new_obj, key).append(new_relation)
                        else:
                            relation_data = value['data']
                            relation_model = self.type_model_dict[relation_data['type']]
                            new_relation = self.fetch_element_by_id(relation_model, relation_data['id'])
                            getattr(new_obj, key).append(new_relation)

                    # the relationship does not use list
                    else:
                        relation_data = value[0]['data'] if is_list_of_relation else value['data']
                        relation_model = self.type_model_dict[relation_data['type']]
                        new_relation = self.fetch_element_by_id(relation_model, relation_data['id'])
                        setattr(new_obj, key, new_relation)

        return new_obj

    def decereal(self, str):
        """deserialize the json string and returns a sqlalchemy model or a list of it"""

        json_loaded = json.loads(str)

        json_data = json_loaded['data']

        is_a_list = isinstance(json_data, list)

        list_of_model = []

        if is_a_list:
            for i in json_data:
                new_obj = self.decereal_jsonapi_object(i)
                list_of_model.append(new_obj)
        else:
            new_obj = self.decereal_jsonapi_object(json_data)
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

