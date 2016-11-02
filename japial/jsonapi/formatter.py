# -*- coding: utf-8 -*-
import __init__
import jerror
from jerror import specification_must, specification_must_not

class TopLevel(object):
    """Top level document structure for jsonapi json"""
    def __init__(self,
                 data     = None,
                 errors   = None,
                 meta     = None,
                 jsonapi  = None,
                 links    = None,
                 included = None):
        """TODO: Constructs a jsonapi formatted json"""

        # --------------------------------------------------
        specification_must(
                'A document MUST contain at least one of the '      \
                'following top-level members: data, errors, meta.',
                data != None or meta != None or errors != None)

        # --------------------------------------------------
        specification_must_not(
                'The members data and errors MUST NOT '             \
                'coexist in the same document.', 
                data != None and errors != None)

        # --------------------------------------------------
        specification_must_not(
                'If a document does not contain a top-level '       \
                'data key, the included member MUST NOT be present either.',
                data == None and included != None)

        self.data     = data
        self.errors   = errors
        self.meta     = meta
        self.jsonapi  = jsonapi if jsonapi != None else { "version" : __init__.version }
        self.links    = links
        self.included = included

    def __jsonapi__(self):
        top_level = {}

        if self.data != None:
            top_level['data'] = self.data
        elif erros != None:
            top_level['errors'] = self.errors
        if self.meta != None:
            top_level['meta'] = self.meta
        if self.jsonapi != None:
            top_level['jsonapi'] = self.jsonapi
        if self.links != None:
            top_level['links'] = self.links
        if self.included != None:
            top_level['included'] = self.included

        return top_level

class ResourceObject(object):
    """Resource object for jsonapi json"""

    def __init__(self,
                 id            = None,
                 type          = None,
                 attributes    = None,
                 relationships = None,
                 links         = None,
                 meta          = None,
                 no_id         = False):

        # --------------------------------------------------
        specification_must(
               'A resource object MUST contain at '\
               'least the following top-level members: id, type.',
               (id != None or no_id) and type != None)

        # --------------------------------------------------
        try:
            self.id     = id   if isinstance(id, basestring) else str(id)
            self.type   = type if isinstance(type, basestring) else str(type)
        except:
            raise jerror.JsonapiFault(
                    'Every resource object MUST contain an id '      \
                    'member and a type member. The values of the '   \
                    'id and type members MUST be strings.')

        self.attributes    = attributes
        self.relationships = relationships
        self.links         = links
        self.meta          = meta
        self.no_id         = no_id

    def __jsonapi__(self):
        resource_object = {}

        if self.id != None:
            resource_object['id'] = self.id
        if self.type != None:
            resource_object['type'] = self.type
        if self.attributes != None:
            resource_object['attributes'] = self.attributes
        if self.relationships != None:
            resource_object['relationships'] = self.relationships
        if self.links != None:
            resource_object['links'] = self.links
        if self.meta != None:
            resource_object['meta'] = self.meta

        return resource_object
