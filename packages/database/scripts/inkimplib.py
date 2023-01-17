from copy import deepcopy
import os, warlock, json
import pandas as pd
import uuid
from datetime import datetime

from DataHolder import DataHolder

import logging
#logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s %(levelname)s %(message)s')
DATA_ERROR = 15
logging.addLevelName(15, 'DATA_ERROR')

class DatorLogger(logging.Logger):
    #super(logging.Logger)

    def data_error(self, msg, *args, **kwargs):
        if self.isEnabledFor(DATA_ERROR):
            self._log(DATA_ERROR, msg, args, **kwargs)


logging.setLoggerClass(DatorLogger)
#logger = DatorLogger('dator_logger')
#root = logging.getLogger()
logger = logging.getLogger('dator_logger')




schema_path = '../schemas/'


def get_uuid_id():
    return str(uuid.uuid4())

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

class InkVisitorJSONObjectFactory:

  json_class_defaults = {
    'IAction': {
      'class': 'A', 'id': '', 'legacyId': '', 'label': '', 'language': '', 'detail': '',
      'data': {'entities': {'a1': [], 'a2': [], 's': []}, 'valencies': {'a1': '', 'a2': '', 's': ''}}, 'props': [],
      'notes': [], 'status': '1', 'references': []
    },
    'IConcept': {
      'class': 'C', 'id': '', 'legacyId': '', 'label': '', 'language': '', 'detail': '', 'data': {}, 'props': [],
      'notes': [], 'status': '1', 'references': []
    },
    'IValue': {
      'class': 'V', 'id': '', 'label': '', 'language': '', 'detail': '', 'data': {'logicalType': '1'}, 'props': [],
      'notes': [], 'status': '1', 'references': []
    },
    'IProp': {
      'bundleEnd': False, 'bundleStart': False, 'certainty': '0', 'children': [], 'elvl': '3', 'id': '', 'logic': '1',
      'mood': ['1'], 'moodvariant': '1', 'bundleOperator': 'a',
      'type': {'entityId': '', 'elvl': '3', 'logic': '1', 'partitivity': '1', 'virtuality': '1'},
      'value': {'entityId': '', 'elvl': '3', 'logic': '1', 'partitivity': '1', 'virtuality': '1'}
    },
    'IResource': {
      'class': 'R', 'id': '', 'label': '', 'language': '', 'detail': '',
      'data': {'url': '', 'partValueBaseURL': '', 'partValueLabel': ''}, 'props': [], 'notes': [], 'status': '1',
      'references': []
    },
    'Relation.IIdentification': {
      'id': '', 'type': 'IDE', 'certainty': '0', 'entityIds': ['', '']
    },
    'Relation.IClassification': {
      'id': '', 'type': 'CLA', 'entityIds': ['', ''], "order": 1
    },
    'Relation.IImplication': {
      'id': '', 'type': 'IMP', 'entityIds': ['', ''], "order": 1
    },
    'Relation.IHolonym': {
      'id': '', 'type': 'HOL', 'entityIds': ['', ''], "order": 1
    },
    'Relation.IRelated': {
      'id': '', 'type': 'REL', 'entityIds': ['', ''], "order": 1
    },
    'Relation.IActionEventEquivalent': {
      'id': '', 'type': 'AEE', 'entityIds': ['', '']
    },
    'Relation.ISubjectActant1Reciprocal': {
      'id': '', 'type': 'SAR', 'entityIds': ['', '']
    },
    'Relation.IPropertyReciprocal': {
      'id': '', 'type': 'PRR', 'entityIds': ['', '']
    },
    'Relation.IAntonym': {
      'id': '', 'type': 'ANT', 'entityIds': ['', ''], "order": 1
    },
    'Relation.ISynonym': {
      'id': '', 'type': 'SYN', 'entityIds': ['', '']
    },
    'Relation.ISuperordinateLocation': {
      'id': '', 'type': 'SOL', 'entityIds': ['', ''], "order": 1
    },
    'Relation.ISuperclass': {
      'id': '', 'type': 'SCL', 'entityIds': ['', ''], "order": 1
    },
    'Relation.ISubjectSemantics': {
      'id': '', 'type': 'SUS', 'entityIds': ['', ''], "order": 1
    },
    'Relation.IActant1Semantics': {
      'id': '', 'type': 'A1S', 'entityIds': ['', ''], "order": 1
    },
    'Relation.IActant2Semantics': {
      'id': '', 'type': 'A2S', 'entityIds': ['', ''], "order": 1
    },
    'IObject': {
      'class': 'O', 'id': '', 'label': '', 'language': '', 'detail': '', 'data': {'logicalType': '1'}, 'props': [],
      'notes': [], 'status': '1', 'references': []
    },
    'IStatement': {
      'class': 'S', 'id': '', 'label': '', 'language': '', 'detail': '',
      'data': {'actants': [], 'actions': [], 'tags': [], 'territory': {'territoryId': '', 'order': 0}, 'text': ''},
      'props': [], 'notes': [], 'status': '1', 'references': []
    },
    'ITerritory': {
      'class': 'T', 'id': '', 'legacyId': '', 'label': '', 'language': '', 'detail': '',
      'data': {'parent': {"territoryId": "T0", "order": 0}}, 'props': [], 'notes': [], 'status': '1', 'references': []
    },
    'ILocation': {
      'class': 'L', 'id': '', 'label': '', 'language': '', 'detail': '', 'data': {'logicalType': '1'}, 'props': [],
      'notes': [], 'status': '1', 'references': []
    },
    'IEvent': {
      'class': 'E', 'id': '', 'label': '', 'language': '', 'detail': '', 'data': {'logicalType': '1'}, 'props': [],
      'notes': [], 'status': '1', 'references': []
    },
    'IReference': {
      'id': '', 'resource': '', 'value': ''
    },
    'IAudit': {
      'id': '', 'entityId': '', 'user': '', 'date': '', 'changes': {}
    },
    'IPerson': {
      'class': 'P', 'id': '', 'label': '', 'language': '', 'detail': '', 'data': {'logicalType': '1'}, 'props': [],
      'notes': [], 'status': '1', 'references': []
    },
    'IGroup': {
      'class': 'G', 'id': '', 'label': '', 'language': '', 'detail': '', 'data': {'logicalType': '2'}, 'props': [],
      'notes': [], 'status': '1', 'references': []
    },
  }
  classes = {}
  def __init__(self, schema_path, import_note):

    self.init_json_classes(schema_path)

    for key, item in type(self).json_class_defaults.items():
      if 'notes' in item and len(item['notes']) == 0:
        item['notes'].append(import_note)

  def init_json_classes(self, schema_path):

    schema_filenames = os.listdir(schema_path)
    json_classes = {}
    json_schemas = {}

    for schema in schema_filenames:
      name = schema.split(".schema")[0]
      file_handler = open(schema_path + schema, "r")
      schema_json = json.load(file_handler)
      json_schemas[name] = schema_json
      globals()[name] = warlock.model_factory(schema_json)
      json_classes[name] = globals()[name]
      logger.info("Class " + name + " available.")

    InkVisitorJSONObjectFactory.classes = json_classes



  def make(self, entity_name, override_object=None):
    if override_object is None:
      override_object = {}
    object = type(self).json_class_defaults[entity_name]
    object.update(override_object)
    return type(self).classes[entity_name](deepcopy(object))

  def validate_defaults(self):
    for e in self.json_class_defaults:
      logger.info(f"Trying to validate class {e}.")
      test = self.make(e, self.json_class_defaults[e])
      logger.info(f"Class {e} validated.")


# for controlling entity and mapping of its fields
class EntityMapper:

    # simple inside values mapping from input_values in gsheets to inkVisitor enums
    # field: { FROM  : TO }
    enum_mapper = {'language': {"English":"eng","Latin":"lat","Occitan":"oci","Middle English":"enm","Czech":"ces","Italian":"ita","French":"fra","German":"deu","Spanish":"spa", "Hungarian":"hun"},"status":{"approved":"1","pending":"0","discouraged":"2","warning":"3"}, "entity_logical_type":{'definite' : "1",
  'indefinite' : "2",   'hypothetical' : "3",  'generic' : "4"}}

    # status  Pending = "0",   Approved = "1",  Discouraged = "2",  Warning = "3",
    valid_entity_classes = ['A','C','E','O','B','R','T','P','G','S','L','NULL']


    IOF = InkVisitorJSONObjectFactory(schema_path, "Import batch [development] " + str(datetime.now()))

    def __init__(self, entity_type, data_row, logger = logger):
        self.entity =  type(self).IOF.make(entity_type)
        self.entity_type = entity_type
        self.logger = logger
        self.debug = True
        self.data_row = data_row
        self.dh = DataHolder()

    def make_alive(self, legacyId="",label="", label_language="", register_id_where=""):

        self.update_id('make_alive',get_uuid_id())
        self.update_legacyId('make_alive',legacyId)
        self.update_label('make_alive',label)
        self.update_label_language('make_alive',label_language)

        if register_id_where!="" and legacyId!="":
            self.dh.entity_ids[register_id_where][legacyId] = self.entity['id']

        #save entity to the pool, which goes to import json file
        if pd.DataFrame(self.dh.additional_entities)[pd.DataFrame(self.dh.additional_entities)['id']==self.entity['id']].empty:
            self.entity = eval(str((self.entity)))
            self.dh.additional_entities.append(self.entity)
            # logger.info(f"Appending {legacyId} territory {self.entity['id']} to the pool of additional entities.")
        else:
            # logger.info(f"Territory {legacyId} {self.entity['id']} exists in the pool of additional entities.")
            pass


    def make_prop_object(self,prop_type_id, prop_value_id):
        prop_object = EntityMapper.IOF.make('IProp')
        prop_object['id'] = get_uuid_id()
        prop_object['type']['entityId'] = prop_type_id
        prop_object['value']['entityId'] = prop_value_id
        return prop_object

    def prepare_prop_object_data(self,prop_type, prop_value, origin = ""):
        prop_type_id = ""
        prop_value_id = ""

        # logger.info(f"Prepare prop object data>  {prop_type}, {prop_value}")

        # allowed entities in input
        allowed_strict_entities = ['C','M','A','E','L','R','S','V','O','T','P'] # should be followed by numbers
        allowed_free_string_entities = ['~V~']

        # checking input_value
        if not is_valid_uuid(prop_value):
            if any(prop_value.startswith(c)for c in allowed_strict_entities):
                # check for numbers
                if not prop_value[1:4].isnumeric():
                    prop_value = "~V~"+prop_value
            elif not any(prop_value.startswith(c)for c in allowed_free_string_entities):
                prop_value = "~V~"+prop_value

            # logger.info(f"Going to search for id for {prop_value}")
            prop_value_id = self.get_entity_id(prop_value, origin=origin)
        else:
           prop_value_id = prop_value

        # TODO this is useless now, because the line above will make ~V~ from everything unknown
        assert any(prop_value.startswith(c)  for c in allowed_strict_entities) or any(prop_value.startswith(c)  for c in allowed_free_string_entities) or is_valid_uuid(prop_value), f"Prop value unknown, C string or V string entity expected, or valid uuid.{prop_value}, {origin}"

        prop_type_id = self.get_entity_id(prop_type, origin=origin)

        return prop_type_id, prop_value_id



    def make_ref_object(self, ref_resource_id, ref_value_id):
        ref_object = EntityMapper.IOF.make('IReference')
        ref_object['id'] = get_uuid_id()
        ref_object['resource'] = ref_resource_id
        ref_object['value'] = ref_value_id
        return ref_object

    def get_entity_id(self,entity_string, origin = ""):
        id = ""
        # logger.info(f"Getting entity string {entity_string} in {origin}")
        try:
            if entity_string.startswith("C") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["concepts"][entity_string]
            elif entity_string.startswith("~V~"):
                ventity = self.make_ventity(entity_string, origin=origin)
                id = ventity['id']
            elif entity_string.startswith("M") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["manuscripts"][entity_string]
            elif entity_string.startswith("A") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["actions"][entity_string]
            elif entity_string.startswith("R") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["resources"][entity_string]
            elif entity_string.startswith("T") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["texts"][entity_string]
            elif entity_string.startswith("O") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["objects"][entity_string]
            elif entity_string.startswith("P") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["persons"][entity_string]
            elif entity_string.startswith("L") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["locations"][entity_string]
            elif entity_string.startswith("E") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["events"][entity_string]
            elif entity_string.startswith("T") and entity_string[1:2].isnumeric():
                id = self.dh.entity_ids["texts"][entity_string]
            elif entity_string.startswith("G") and entity_string[1:4].isnumeric():
                id = self.dh.entity_ids["groups"][entity_string]

            elif is_valid_uuid(entity_string):
                id = entity_string

        except KeyError as E:
            logger.error(f"Cannot get entity id from entity string {entity_string} in {origin}. {E}")
            # raise Exception(f"Cannot get entity id '{id}' from value  {entity_string}  in {origin}.")

        if id != "" and isinstance(id, str):
            # logger.info(f"Got entity id {id} from entity string {entity_string} in {origin}")
            return id
        else:
            logger.error(f"Cannot get entity id '{id}' from value {entity_string}  in {origin}.")
            # raise Exception(f"Cannot get entity id '{id}' from value  {entity_string}  in {origin}.")

    def make_ventity(self, value_string, origin=""):
        # logger.info(f"Generating ventity from {value_string}.")
        # generate value entity object...
        ventity = EntityMapper.IOF.make('IValue')
        ventity['id'] = get_uuid_id()
        ventity['label'] = value_string.replace("~V~","")

        if self.debug:
            ventity['notes'].append(origin)

        # register ventity
        self.dh.tables['values'] = self.dh.tables['values'].append({'id':ventity['id'] ,'value':ventity['label'],"origin":origin},ignore_index=True )
        ventity = eval(str(ventity))
        self.dh.additional_entities.append(ventity)

        # logger.info(f"Ventity id={ventity['id']} generated.")

        # create audit record
        self.create_audit_record(entity_id=ventity['id'], object=ventity)

        return ventity

    def make_rentity(self, label, url = "", origin=""):
        # logger.info(f"Generating rentity from {value_string}.")
        # generate resource entity object...
        rentity = EntityMapper.IOF.make('IResource')
        rentity['id'] = get_uuid_id()
        rentity['label'] = label
        rentity['data']['url'] = url

        # if self.debug:
        #    rentity['notes'].append(origin)

        # register rentity
        self.dh.tables['resources'] = self.dh.tables['resources'].append({'id':rentity['id'] ,'label':rentity['label'],"dissinet_respository_url":url, "origin":origin}, ignore_index=True )
        rentity = eval(str(rentity))
        self.dh.additional_entities.append(rentity)

        # logger.info(f"Rentity id={rentity['id']} generated.")
        return rentity


    def make_eentity(self, label, legacyId, url = "", origin=""):

        eentity = EntityMapper.IOF.make('IEvent')
        eentity['id'] = get_uuid_id()
        eentity['label'] = label
        eentity['legacyId'] = legacyId

        if self.debug:
            eentity['notes'].append(origin)

        # register event
        self.dh.tables['events'] = self.dh.tables['events'].append({'id':eentity['id'] ,'value':eentity['label'],"origin":origin, "legacyId":legacyId}, ignore_index=True )
        eentity = eval(str(eentity))
        self.dh.additional_entities.append(eentity)

        return eentity

    def make_lentity(self, label, legacyId="", url = "", origin=""):

        lentity = EntityMapper.IOF.make('ILocation')
        lentity['id'] = get_uuid_id()
        lentity['label'] = label
        lentity['legacyId'] = legacyId

        if self.debug:
            lentity['notes'].append(origin)

        # register lentity
        self.dh.tables['locations'] = self.dh.tables['locations'].append({'id':lentity['id'] ,'value':lentity['label'],"origin":origin,"legacyId":legacyId}, ignore_index=True )
        lentity = eval(str(lentity))
        self.dh.additional_entities.append(lentity)

        return lentity

    def make_tentity(self, label, legacyId="", url = "", origin=""):

        tentity = EntityMapper.IOF.make('ITerritory')
        tentity['id'] = get_uuid_id()
        tentity['label'] = label
        tentity['legacyId'] = legacyId

        if self.debug:
            tentity['notes'].append(origin)

        # register tentity
        self.dh.tables['territories'] = self.dh.tables['territories'].append({'id':tentity['id'] ,'value':tentity['label'],"origin":origin,"legacyId":legacyId}, ignore_index=True)
        if legacyId != "":
            self.dh.entity_ids['texts'][legacyId] = tentity['id']
        tentity = eval(str(tentity))
        self.dh.additional_entities.append(tentity)

        return tentity

    def make_relation_identity_record(self, id1, id2, certainty="", origin="", order=1):

        rir = EntityMapper.IOF.make('Relation.IIdentification')
        rir['id'] = get_uuid_id()
        rir['entityIds'] = [id1,id2]
        rir['order'] = order

        if certainty != "":
            rir['certainty'] = certainty

        # register relation
        self.dh.tables['relations'] = self.dh.tables['relations'].append({'id':rir['id'] ,'type':rir['type'], "certainty":rir['certainty'],"entityIds":rir['entityIds'], "origin":origin}, ignore_index=True )
        rir = eval(str(rir))
        self.dh.relation_records.append(rir)

        return rir

    def make_relation_classification_record(self, id1, id2, origin="", order=1):

        rcr = EntityMapper.IOF.make('Relation.IClassification')
        rcr['id'] = get_uuid_id()
        rcr['entityIds'] = [id1,id2]
        rcr['order'] = order

        # register relation
        self.dh.tables['relations'] = self.dh.tables['relations'].append({'id':rcr['id'] ,'type':rcr['type'], "entityIds":rcr['entityIds'], "origin":origin}, ignore_index=True )
        rcr = eval(str(rcr))
        self.dh.relation_records.append(rcr)

        return rcr

    def make_relation_record(self, relation_type, ids_list, origin="", order=1):
        # genereic relation fc
        # BUT synonymic relation have different logic of storage

        # a fork to custom function
        if relation_type == "Synonym":
            # rr = self.make_relation_synonymic_record(relation_type, ids_list, origin="")
            logger.error(f"Generic relation record method called, should be handled by special function.")
            return False
        else:
            rr = EntityMapper.IOF.make('Relation.I'+relation_type)
            rr['id'] = get_uuid_id()
            rr['entityIds'] = ids_list
            rr['order'] = order

        # logger.info(f"Making {relation_type} record. ID{rr['id']} EIDS{rr['entityIds']}. Origin: {origin}")

        # register lentity
        self.dh.tables['relations'] = self.dh.tables['relations'].append({'id':rr['id'] ,'type':rr['type'], "entityIds":rr['entityIds'], "origin":origin}, ignore_index=True )
        rr = eval(str(rr))
        self.dh.relation_records.append(rr)

        return rr

    def make_relation_synonimic_record(self, relation_type, ids_list, origin="", order=1):

        # make new relation object
        rr = EntityMapper.IOF.make('Relation.I'+relation_type)
        rr['id'] = get_uuid_id()
        # logger.info(f"Making synonimic relation record with {ids_list}. To be sorted to {ids_list.sort()}.")
        ids_list.sort()
        rr['entityIds'] = ids_list
        rr['order'] = order

        # check if exists a synonym relation record with the ids
        synonymic_relation_exists = False

        if synonymic_relation_exists:
            pass
        else:
            # register relation record
            self.dh.tables['relations'] = self.dh.tables['relations'].append({'id':rr['id'] ,'type':rr['type'], "entityIds":rr['entityIds'], "origin":origin}, ignore_index=True )
            # store relation record
            rr = eval(str(rr))
            self.dh.relation_records.append(rr)

        return rr

    # interprets prop_type (should be always concept or resource) and input_value (should be entity or value string)
    # get ids of the prop_type and prop_value (possibly creates and register values object)
    # make iProp object
    # puts iProp object into the entity props property
    def hook_prop_object(self, prop_type, input_value, prop_source="",  origin="", prop_source_id ="", field_name="", prop_source_field = ""):

        # allowed entities in type
        # logger.info(f"Hook prop object, {prop_type}, {origin}")
        assert prop_type!="", f"Prop type empty, C o R entity string expected? {origin}"
        assert "C" in prop_type[0] or "R" in prop_type[0], f"Prop type unknown, C or R string entity expected? {prop_type}, {origin}"

        prop_type_id, prop_value_id = self.prepare_prop_object_data(prop_type, input_value, origin=origin)
        # make IProp object
        prop_object = self.make_prop_object(prop_type_id, prop_value_id)

        # register prop object
        self.dh.tables['props'] = self.dh.tables['props'].append({'id':prop_object['id'] , 'type_id':prop_type_id,'value_id':prop_value_id,'type':prop_type,'value':input_value, "original_field":field_name, "origin":origin, 'entityId':self.entity['id'], 'legacyId':self.entity['legacyId']}, ignore_index=True)

        if prop_source_field != "":
            self.hook_2ndprop_into_props(prop_object,prop_source_field = prop_source_field, origin = origin)
        elif prop_source_id !="": # means propvalue_2nd
            self.hook_2ndprop_into_props(prop_object,prop_source_id = prop_source_id, origin = origin)
        elif prop_source !="": # means propvalue_2nd
            self.hook_2ndprop_into_props(prop_object,prop_source = prop_source, origin = origin)

        else:
            # hook directly into the entity object
            self.hook_prop_into_props(prop_object)

    def hook_ref_object(self, ref_legacyID, input_value, prop_source="",  origin=""):

        # allowed entities in ref_legacyID
        assert "R" in ref_legacyID, f"Unknown input, R legacyId expected? {ref_legacyID},{input_value}, {origin}"

        #modify value, so the value object is created
        input_value = "~V~"+input_value

        ref_resource_id = self.get_entity_id(ref_legacyID, origin=origin)
        ref_value_id = self.get_entity_id(input_value, origin=origin)

        # make IReference object
        ref_object = self.make_ref_object(ref_resource_id, ref_value_id)

        self.hook_ref_into_refs(ref_object)


    def hook_prop_into_props(self,prop_object):
        self.entity['props'].append(prop_object)

    def hook_ref_into_refs(self,ref_object):
        self.entity['references'].append(ref_object)

    def hook_2ndprop_into_props(self, prop_object, prop_source = "", prop_source_id = "", prop_source_field = "", origin = ""):  # identification by concept id

        # recognition based on the prop_source_field
        if prop_source_field != "":

            # count, value in enumerate(values)
            for count, po in enumerate(self.entity['props']):
                # po['id']
                # find whether this id is registered under the prop_source_field within this entity frame
                candidate_prop_objects = self.dh.tables['props'][(self.dh.tables['props']['legacyId'] ==self.entity['legacyId']) & (self.dh.tables['props']['original_field'] == prop_source_field)]

                #logger.info(f"2nprop: {len(candidate_prop_objects)}")
                #logger.info(f"2nprop: {len(candidate_prop_objects)} : {candidate_prop_objects.iloc[0]['id']}")

                if len(candidate_prop_objects) > 0:
                    for key, row in candidate_prop_objects.iterrows():

                        for  po in self.entity['props']:
                            if po['id'] == row['id'] and len(po['children']) == 0:
                                # logger.info(f"Found prop. {po['id']}. Adding the 2ndprop child.")
                                po['children'].append(prop_object)

                else:
                    logger.error(f"In context {self.entity['legacyId']},cannot find the proper prob object record. {prop_object} at {prop_source_field} in origin '{origin}'.")
        else:
            logger.error(f"Fc hook_2ndprop_into_props run without filled prop_source_field in origin '{origin}'.")

        # recognition based on the type concept of the parent prop object
        if prop_source != "":
            keyId = self.get_entity_id(prop_source)
            assert is_valid_uuid(keyId), f"Cannot recognize entity id from {prop_source}"

            # count, value in enumerate(values)
            for count, po in enumerate(self.entity['props']):
                if po['type']['entityId'] == keyId and len(po['children']) == 0:  # I am counting on the fact, that if there are relations from multiples, they are processed in the specific right order
                   po['children'].append(prop_object)


        # recognition based od propobject id
        if prop_source_id != "":
            keyId = prop_source_id
            assert is_valid_uuid(keyId), "Not valid uuid {keyId}"

            for count, po in enumerate(self.entity['props']):
                if po['id'] == keyId:  # I am counting on the fact, that if there are relations from multiples, they are processed in the specific right order
                   po['children'].append(prop_object)



    # method invoker for the INSIDE operation with concrete fields
    def update_inside_field(self, field_name, input_value, origin= ""):
        if input_value != '':

            if ("#" in input_value or "~" in input_value) and "note" not in field_name and "https://docs." not in input_value:
                self.logger.info(f"ALERT # or ~ in the input value {input_value}")

            update_operation = "update_" + field_name
            # update_func = getattr(self, update_operation, self.update_generic)
            update_func = getattr(self, update_operation, self.update_generic)
            update_func(field_name, input_value, origin)
        else:
            raise Exception(f"Trying to update {field_name} with empty input value.")

    #########################################################################################################
    # the naming of procedures corresponds to the name of the input_table fields,  used for inside operations

    def update_label_language(self, field_name="", input_value="", origin = ""):
        if input_value in type(self).enum_mapper['language']:
            self.entity['language'] = type(self).enum_mapper['language'][input_value]
        else:
            self.logger.error(f"Unable to set language in {origin}.")
            self.entity['language'] = input_value # will raise error

    def update_status(self, field_name, input_value, origin = ""):
        if input_value in type(self).enum_mapper['status']:
            self.entity['status'] = type(self).enum_mapper['status'][input_value]
        else:
            self.logger.error(f"Unable to set status in {origin}.")
            self.entity['status'] = input_value # will raise error

    def update_entity_logical_type(self, field_name, input_value, origin = ""):
        input_value = input_value.strip()
        # self.logger.info(f" {field_name}, {input_value}, {self.enum_mapper['entity_logical_type'].keys()}")
        # self.logger.info(f"'{input_value}' : '{self.enum_mapper['entity_logical_type'].keys()}'")
        if input_value in self.enum_mapper['entity_logical_type'].keys():
            self.entity['data']['logicalType'] = self.enum_mapper['entity_logical_type'][input_value]
        else:
            self.logger.error(f"Unable to set entity logical type '{input_value}' in {origin}.")
            raise Exception()
            # self.entity['data']['logicalType'] = input_value # will raise error

    def update_note(self, field_name, input_value, origin = ""):
        #self.logger.info(f"Updating note with {input_value}.")
        if "#" in input_value:
            values = [v.strip() for v in input_value.split("#")]
            for v in values:
                self.entity['notes'].append(v)
        else:
            self.entity['notes'].append(input_value)

    def update_notes(self, field_name, input_value, origin = ""):
        #self.logger.info(f"Updating note with {input_value}.")
        if "#" in input_value:
            values = [v.strip() for v in input_value.split("#")]
            for v in values:
                self.entity['notes'].append(v)
        else:
            self.entity['notes'].append(input_value)

    def update_localisation_notes(self, field_name, input_value, origin = ""):
        #self.logger.info(f"Updating note with {input_value}.")
        if "#" in input_value:
            values = [v.strip() for v in input_value.split("#")]
            for v in values:
                self.entity['notes'].append(v)
        else:
            self.entity['notes'].append(input_value)

    def update_id(self, field_name, input_value, origin = ""):
        # self.entity['id'] = input_value
        self.entity['id'] = input_value

    def update_legacyId(self, field_name="", input_value="", origin = ""):
        # logger.info(f"Trying to set legacyId {type(input_value)}:'{input_value}' {origin}.")
        self.entity['legacyId'] = input_value

    def update_label(self, field_name="", input_value="", origin = ""):
        self.entity['label'] = input_value

    def update_wordnet_lemma_id(self, field_name, input_value, origin = ""):
        # self.logger.info(f" wordnet_lemma_id NOT IMPLEMENTED ")
        pass

    def update_wordnet_synset_id(self, field_name, input_value, origin = ""):
        # self.logger.info(f" wordnet_synset_id NOT IMPLEMENTED ")
        pass

    def update_generic(self, field_name, input_value, origin = ""):
        self.entity[field_name] = input_value


    def create_audit_record(self, entity_id = '', editor_candidate = '', object = {}):

        data_row = self.data_row
        if entity_id == '':
            entity_id = self.entity['id']
        if object == {}:
            object = self.entity  # should be run at the end of the entity making, to the object is "full"

        # date =  {
        #     "$reql_type$": "TIME",
        #      "epoch_time": time.time(),
        #      "timezone": "+00:00"
        # }
        date =  datetime.now().strftime("%Y-%m-%dT%H:%M:%S")+"Z" #2021-12-05T19:10:15.739Z

        if editor_candidate == '' and 'editor' in data_row.keys():
            editor_candidate = data_row['editor']
        if editor_candidate in self.dh.editors.keys():
            editor_id = self.dh.editors[editor_candidate]
        else:
            editor_id = self.dh.editors['David Zbíral']

        import_audit = EntityMapper.IOF.make('IAudit')
        import_audit['id'] = get_uuid_id()
        import_audit['entityId'] = entity_id
        import_audit['user'] =  self.dh.editors['import']
        import_audit['date'] = date
        import_audit['changes'] = dict(object)

        editor_audit = EntityMapper.IOF.make('IAudit')
        editor_audit['id'] = get_uuid_id()
        editor_audit['entityId'] = entity_id
        editor_audit['user'] =  editor_id
        editor_audit['date'] = date
        editor_audit['changes'] = dict(object)

        # audits.append(import_audit)
        editor_audit = eval(str(editor_audit))
        self.dh.audits.append(editor_audit)


class TerritoryEntityMapper(EntityMapper):
    def __init__(self,entity_type, data_row, logger = logger):
        EntityMapper.__init__(self,entity_type, data_row, logger)

        if "legacyId" in data_row and "T" in data_row["legacyId"]:
            self.entity['data']['parent']['order'] = int(data_row["legacyId"].replace("T",""))
        else:
            # logger.info(f"In territory entity mapper, legacyId uknown, the order of the entity must be set manually.")
            pass

class ConceptEntityMapper(EntityMapper):
    def __init__(self,entity_type, data_row, logger = logger):
        EntityMapper.__init__(self,entity_type, data_row, logger)

class ActionEntityMapper(EntityMapper):
    def __init__(self,entity_type, data_row, logger = logger):
        EntityMapper.__init__(self,entity_type, data_row, logger)

    def update_subject_entity_type(self, operation, value, entity_mapper):
        # self.logger.info(f"AP custom field: subject_entity_type")
        entities = [e.strip() for e in value.split("|")]
        for e in entities:
            if e in self.valid_entity_classes:
                self.entity['data']['entities']['s'].append(e)
            elif e == "*":
                self.entity['data']['entities']['s'] = self.valid_entity_classes
            else:
                logger.error(f"Non valid entity processed: {e} while AP.update_subject_entity_type().")

    def update_subject_valency(self, operation, value, entity_mapper):
        # self.logger.info(f"AP custom field: subject_valency")
        self.entity['data']['valencies']['s'] = value

    def update_actant1_entity_type(self, operation, value, entity_mapper):
        # self.logger.info(f"AP custom field: actant1_entity_type")
        entities = [e.strip() for e in value.split("|")]
        for e in entities:
            if e in self.valid_entity_classes:
                self.entity['data']['entities']['a1'].append(e)
            elif e == "*":
                self.entity['data']['entities']['a1'] = self.valid_entity_classes
            else:
                logger.error(f"Non valid entity processed: {e} while AP.update_actant1_entity_type().")

    def update_actant2_entity_type(self, operation, value, entity_mapper):
        # self.logger.info(f"AP custom field: actant2_entity_type")
        entities = [e.strip() for e in value.split("|")]
        for e in entities:
            if e in self.valid_entity_classes:
                self.entity['data']['entities']['a2'].append(e)
            elif e == "*":
                self.entity['data']['entities']['a2'] = self.valid_entity_classes
            else:
                logger.error(f"Non valid entity processed: {e} while AP.update_actant2_entity_type().")

    def update_actant1_valency(self, operation, value, entity_mapper):
        # self.logger.info(f"AP custom field: actant1_valency")
        self.entity['data']['valencies']['a1'] = value

    def update_actant2_valency(self, operation, value, entity_mapper):
        # self.logger.info(f"AP custom field: actant1_valency")
        self.entity['data']['valencies']['a2'] = value


class ResourceEntityMapper(EntityMapper):
    def __init__(self,entity_type, data_row, logger = logger):
        EntityMapper.__init__(self,entity_type, data_row, logger)

    def update_url(self, operation, value, entity_mapper):
        # self.logger.info(f"AP custom field: subject_entity_type")
        self.entity['data']['url'] = value


class ObjectEntityMapper(EntityMapper):
    def __init__(self,entity_type, data_row, logger = logger):
        EntityMapper.__init__(self,entity_type, data_row, logger)

class EventEntityMapper(EntityMapper):
    def __init__(self,entity_type, data_row, logger = logger):
        EntityMapper.__init__(self,entity_type, data_row, logger)

class LocationEntityMapper(EntityMapper):
    def __init__(self,entity_type, data_row, logger = logger):
        EntityMapper.__init__(self,entity_type, data_row, logger)

class PersonEntityMapper(EntityMapper):
    def __init__(self,entity_type, data_row, logger = logger):
        EntityMapper.__init__(self,entity_type, data_row, logger)

class GroupEntityMapper(EntityMapper):
    def __init__(self,entity_type, data_row, logger = logger):
        EntityMapper.__init__(self,entity_type, data_row, logger)


class EntityMapperFactory:
    def __init__(self):
        pass

    def make(self, entity_name, data_row):
        if 'ITerritory' == entity_name:
            return TerritoryEntityMapper(entity_name, data_row)
        elif 'IAction' == entity_name:
            return ActionEntityMapper(entity_name, data_row)
        elif 'IConcept' == entity_name:
            return ConceptEntityMapper(entity_name,data_row)
        elif 'IResource' == entity_name:
            return ResourceEntityMapper(entity_name, data_row)
        elif 'IObject' == entity_name:
            return ObjectEntityMapper(entity_name, data_row)
        elif 'IEvent' == entity_name:
            return EventEntityMapper(entity_name, data_row)
        elif 'ILocation' == entity_name:
            return LocationEntityMapper(entity_name, data_row)
        elif 'IPerson' == entity_name:
            return PersonEntityMapper(entity_name, data_row)
        elif 'IGroup' == entity_name:
            return GroupEntityMapper(entity_name, data_row)

        else:
            logger.warning(f"Unrecognized entity class in entity mapper. Is this right?")
            return EntityMapper(entity_name)



# CONTROL CLASS
class ParseController():

    def __init__(self, entity_list = [], keyword_row_id = 3,  logger = logger):
        self.entity_list = entity_list
        self.logger = logger
        self.parsers = {}
        self.reparse_entity_list = []
        self.dh = DataHolder()

        for e in self.entity_list:
            if 'texts' in e:
                self.parsers[e] = TextParser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)
            elif 'actions' in e:
                self.parsers[e] = ActionParser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)
            elif 'concepts' in e:
                self.parsers[e] = ConceptParser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)
            elif 'resources' in e:
                self.parsers[e] = ResourceParser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)
            elif 'manuscripts' in e:
                self.parsers[e] = ManuscriptParser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)

            elif 'persons' in e:
                self.parsers[e] = PersonParser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)
            elif 'locations' in e:
                self.parsers[e] = LocationParser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)
            elif 'events' in e:
                self.parsers[e] = EventParser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)
            elif 'groups' in e:
                self.parsers[e] = GroupParser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)

            # elif 'R0006_persons' in e:
            #     self.parsers[e] = PersonParser(e, header_df = header_infos[e], table_df = tables[e], keyword_row_id = keyword_row_id, logger = logger)
            # elif 'R0007_locations' in e:
            #     self.parsers[e] = LocationParser(e, header_df = header_infos[e], table_df = tables[e], keyword_row_id = keyword_row_id, logger = logger)
            # elif 'R0008_events' in e:
            #     self.parsers[e] = EventParser(e, header_df = header_infos[e], table_df = tables[e], keyword_row_id = keyword_row_id, logger = logger)
            # elif 'R0075_persons' in e:
            #     self.parsers[e] = PersonParser(e, header_df = header_infos[e], table_df = tables[e], keyword_row_id = keyword_row_id, logger = logger)
            # elif 'R0035_locations' in e:
            #     self.parsers[e] = LocationParser(e, header_df = header_infos[e], table_df = tables[e], keyword_row_id = keyword_row_id, logger = logger)
            # elif 'R0083_events' in e:
            #     self.parsers[e] = EventParser(e, header_df = header_infos[e], table_df = tables[e], keyword_row_id = keyword_row_id, logger = logger)
            else:
                self.logger.warning(f"Coming to basic Parser entity - strange '{e}' {type(e)}.")
                self.parsers[e] = Parser(e, header_df = self.dh.header_infos[e], table_df = self.dh.tables[e], keyword_row_id = keyword_row_id, logger = logger)

    def update_parsers(self, entity_list = []):
      pass


    def parse(self, stop = False):
        for name, p in self.parsers.items():
            if len(self.reparse_entity_list) > 0:
                if name in self.reparse_entity_list:
                    self.logger.info("PARTIAL PARSE Active, reparsing "+name)
                    p.parse_rows(stop)
                else:
                    self.logger.info("PARTIAL PARSE Active, skipping "+name)
            else:
                p.parse_rows(stop)


# WORKER CLASS
class Parser():
    EMP = EntityMapperFactory()
    dh = DataHolder()

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        self.name = name
        self.logname = name.upper()
        self.input_header_df = header_df
        self.input_table_df = table_df
        self.prepared_table = pd.DataFrame()
        self.keyword_row_id =  keyword_row_id
        self.columns = self.input_header_df.columns.tolist()

        self.proptype_2nd = {} # for registering the columns, which contains proptype_2nd information

        self.parsing_instruction = {}
        self.oper_columns = {'discard':[],'inside':[],'special':[],'unknown':[],"proptype":[],'propvalue':[],'proptype_2nd':[],'propvalue_2nd':[],"dependent":[], "reference":[], "reference_object":[], "reference_part":[],"hooked-inside":[],"hooked-propvalue":[],"hooked-relation":[]}
        self.logger = logger

        self.dh = DataHolder()

        # RUN
        self.process_header_instructions()
        self.prepare_input_table()

    # "parsing" instructions
    def process_header_instructions(self) -> (pd.DataFrame, pd.DataFrame):
        keyword_row = self.input_header_df.iloc[self.keyword_row_id]
        prop_type_row = self.input_header_df.iloc[self.keyword_row_id - 1]
        source_node_row = self.input_header_df.iloc[self.keyword_row_id - 2]

        log_uncertain_instructions = []

        for c in self.columns:
            instruction_candidate = str(keyword_row.at[c]).strip()
            prop_type_candidate = str(prop_type_row.at[c]).strip()
            source_node_candidate = str(source_node_row.at[c]).strip()

            if c == '':
                self.logger.error(f"{self.logname} There is empty column in the dataset.")
                raise Exception(f"{self.logname} There is empty column in the dataset.")

            if "?" in instruction_candidate or "?" in prop_type_candidate or "?" in source_node_candidate:
                log_uncertain_instructions.append(f"{c.upper()}:{instruction_candidate},{prop_type_candidate},{source_node_candidate}")
                instruction  = {'operation':'discard', 'target': None}
                self.oper_columns['discard'].append(c)

            # logger.info(f" {instruction_candidate}, {prop_type_candidate}, {source_node_candidate}")

            # known instructions
            if 'discard' in instruction_candidate:
                instruction  = {'operation':'discard', 'target': None}
                self.oper_columns['discard'].append(c)

            elif instruction_candidate == "propvalue":
                prop_type = prop_type_candidate
                source_node = source_node_candidate

                if source_node != "" and prop_type == "":
                    prop_type = source_node

                # test whether is its propvalue proper or dependent (=proptype is dynamic, value from another column)
                if prop_type.strip() == "":
                    self.oper_columns['dependent'].append(c)
                    logger.info(f"Throwing out propvalue instruction in column {c}.")
                    continue # ignoring "dependent propvalue"

                if "?" in prop_type or "?"  in source_node:
                    instruction = {'operation':'unknown', 'target': None}
                    self.oper_columns['unknown'].append(c)
                else:
                    instruction  = {'operation':'propvalue', 'type': prop_type, 'source':source_node} # source can be ignored, because the iProp object is sitting inside of it
                    self.oper_columns['propvalue'].append(c)

            elif 'propvalue_2nd' in instruction_candidate:
                prop_type = prop_type_candidate
                source_node = source_node_candidate
                if "?" in prop_type or "?"  in source_node:
                    instruction = {'operation':'unknown', 'target': None}
                    self.oper_columns['unknown'].append(c)
                else:
                    instruction  = {'operation':'propvalue_2nd', 'type': prop_type, 'source':source_node} # source can NOT be ignored, it signals which existing iProp object will hold this iProp object
                    self.oper_columns['propvalue_2nd'].append(c)

            elif 'proptype_2nd' in instruction_candidate:
                prop_type = prop_type_candidate
                source_node = source_node_candidate
                if "?" in prop_type or "?"  in source_node:
                    instruction = {'operation':'unknown', 'target': None}
                    self.oper_columns['unknown'].append(c)
                else:
                    instruction  = {'operation':'proptype_2nd', 'type': prop_type, 'source':source_node}
                    self.oper_columns['proptype_2nd'].append(c)

            elif 'special' == instruction_candidate:
                # looks for custom functions registered by column name
                prop_type = prop_type_candidate
                source_node = source_node_candidate
                instruction  = {'operation':'special', 'type': prop_type, 'source':source_node}
                self.oper_columns['special'].append(c)

            elif 'proptype' in instruction_candidate:
                prop_type = prop_type_candidate
                source_node = source_node_candidate
                instruction  = {'operation':'proptype', 'type': prop_type, 'source':source_node}
                #logger.info(f"here ...{instruction_candidate} {c}")
                self.oper_columns['proptype'].append(c)

            elif 'dependent' in instruction_candidate:
                # ignore
                # the value is solved by another instruction
                instruction  = {'operation':'dependent', 'type': prop_type, 'source':source_node}

            elif instruction_candidate == "inside":
                if "?" in c:
                    instruction = {'operation':'unknown', 'target': None}
                    self.oper_columns['unknown'].append(c)
                else:
                    instruction  = {'operation':'inside', 'target': None}
                    if len(prop_type_candidate) > 0:
                        instruction  = {'operation':'inside', 'target': prop_type_candidate}

                    self.oper_columns['inside'].append(c)

            elif instruction_candidate == "hooked-inside":
                if "?" in c:
                    instruction = {'operation':'unknown', 'target': None}
                    self.oper_columns['unknown'].append(c)
                else:
                    instruction  = {'operation':'hooked-inside', 'target': None}
                    if len(prop_type_candidate) > 0:
                        instruction  = {'operation':'hooked-inside', 'target': prop_type_candidate}

                    self.oper_columns['hooked-inside'].append(c)

            elif instruction_candidate == "hooked-propvalue":
                if "?" in c:
                    instruction = {'operation':'unknown', 'target': None}
                    self.oper_columns['unknown'].append(c)
                else:
                    instruction  = {'operation':'hooked-propvalue', 'target': None}
                    if len(prop_type_candidate) > 0:
                        instruction  = {'operation':'hooked-propvalue', 'target': prop_type_candidate}

                    self.oper_columns['hooked-propvalue'].append(c)

            elif instruction_candidate == "hooked-relation":
                if "?" in c:
                    instruction = {'operation':'unknown', 'target': None}
                    self.oper_columns['unknown'].append(c)
                else:
                    instruction  = {'operation':'hooked-relation', 'target': None}
                    if len(prop_type_candidate) > 0:
                        instruction  = {'operation':'hooked-relation', 'target': prop_type_candidate}

                    self.oper_columns['hooked-relation'].append(c)

            elif "reference" == instruction_candidate:
                #logger.info(f"Found instruction 'reference'. {prop_type_candidate}")
                self.oper_columns["reference"].append(c)
                instruction  = {'operation':'reference', 'ref_legacy_id':prop_type_candidate}

            elif "reference_object" == instruction_candidate:
                #logger.info(f"Found instruction 'reference'. {prop_type_candidate}")
                self.oper_columns["reference_object"].append(c)
                instruction  = {'operation':'reference_object', 'ref_legacy_id':prop_type_candidate}

            elif "reference_part" == instruction_candidate:
                # logger.info(f"Found instruction 'reference_part'. {prop_type_candidate}")
                self.oper_columns["reference_part"].append(c)
                instruction  = {'operation':'reference_part', 'ref_legacy_id':prop_type_candidate}

            elif instruction_candidate == "relation":
                relation_type = prop_type_candidate
                instruction  = {'operation':'relation', 'type': relation_type}

            else:
                instruction = {'operation':'unknown', 'target': None}
                self.oper_columns['unknown'].append(c)
            self.parsing_instruction[c] = instruction

        self.logger.info(f"{self.logname} Uncertain parsing instructions in {len(log_uncertain_instructions)} columns: " + " ".join(log_uncertain_instructions) + ".")
        return self.parsing_instruction

    def prepare_input_table(self):
        ip = self.input_table_df.copy()

        # discard  columns with discard and unknown operations
        for c in self.oper_columns['discard']+self.oper_columns['unknown']:
            ip.drop(columns=c, inplace=True)
        #ip.drop(columns=self.oper_columns['discard']+self.oper_columns['unknown'], inplace=True)

        self.logger.info(f"{self.logname} {len(self.oper_columns['discard']+self.oper_columns['unknown'])} columns have been dropped (discard:{len(self.oper_columns['discard'])}, unknown:{len(self.oper_columns['unknown'])}: {self.oper_columns['unknown']}). Table now has {len(ip.columns)} columns, inside:{len(self.oper_columns['inside'])},propvalue:{len(self.oper_columns['propvalue'])}, special:{len(self.oper_columns['special'])}, proptype: {len(self.oper_columns['proptype'])}, proptype_2nd: {len(self.oper_columns['proptype_2nd'])}, dependent:{len(self.oper_columns['dependent'])}, reference_part:{len(self.oper_columns['reference_part'])}. Originally {self.input_table_df.shape[1]} columns.")

        self.prepared_table = ip

    def prepare_property(self):
        pass

    def make_row_object(self, data_row):
        class_name = self.dh.table_to_entity[self.name]
        return self.EMP.make(class_name, data_row)

    def itemize_valuestring_for_multiples(self, value_with_multiples, origin="") -> []:
        values = []
        if isinstance(value_with_multiples,str):
            parsed_value = value_with_multiples.split('#')
            values =  [item.strip() for item in parsed_value]
        else:
            raise Exception(f"Expected value to be string. Got {type(value_with_multiples)}. {origin}")
        return values

    def parse_rows(self, stop = False):
        self.logger.info(f"Starting to parse {self.name}.")

        if  self.prepared_table['label'].isnull().any():
            self.prepared_table  = self.prepared_table[self.prepared_table['label'].notna()]
            self.logger.info(f"Empty labels found in {self.name} table. (new entities added through parsing process). Adjusting - entities with empty labels not taken into account.")

        counter = 0
        for key, row in self.prepared_table.iterrows():
            counter += 1
            if stop and counter > stop:
                break
            #self.logger.info(f"{self.name} Processing row {key}")
            #self.logger.info(f"{row.to_dict()}")
            entity_mapper = self.make_row_object(row.to_dict())

            if row['legacyId'] == "":
                logger.info(f"Skipping {row['label']}, does not have set legacyId. Remnant of already run parse?")
                continue

            for name, value in row.items():
                if name in self.parsing_instruction:
                    operation = self.parsing_instruction[name]
                else:
                    continue # silently ignore unknown columns
                # logger.info(f"{self.name} Processing columns {name}, with value {value}. Op:{operation}")

                # force string
                value = str(value)

                # validation of value for question marks
                if "??" in value:
                    logger.info(f"About ??? : There is {value} in column {name} in row {str(key)}.")
                    continue

                # thrashing "NA"
                #if value == "NA":
                #    continue

                if operation['operation'] == 'inside' and value != '' and '?' not in name:
                    # logger.info(f"{self.name} Processing columns {name}, with value {value}. Op:{operation}")
                    if operation['target']:
                        name = operation['target']
                    entity_mapper.update_inside_field(name,value,operation['operation'] +">"+ str(key)+":"+str(name)+":"+str(value))

                if operation['operation'] == 'propvalue' and value != '':

                    #logger.info(f"{self.name} Processing 'propvalue' for column {name}, with value {value} and type {operation['type']} Op:{operation}")
                    prop_type = operation['type']

                    if prop_type in row.keys():  # prop type is defined in other column (it is NOT fixed for all propvalues)
                        prop_type = row[prop_type]
                        # logger.info(f"Shifting to remote proptype {prop_type} in the context of {name}, {value},{operation['type']}.")

                    if prop_type == '' or 'C' not in prop_type:
                        # raise Exception(f"Propvalue does not have prop type '{prop_type}' defined. C entity-string expected, got {key}, {name}, {value}. [{operation}]")
                        logger.error(f"Propvalue does not have prop type '{prop_type}' defined. C entity-string expected, got {key}, {name}, {value}. [{operation}]")
                        continue

                    for item in self.itemize_valuestring_for_multiples(value):
                        #logger.info(f"Propvalue value {value} item {item}.")
                        entity_mapper.hook_prop_object(prop_type = prop_type, input_value = item, origin = operation['operation'] +">"+ str(key)+f":{row['legacyId']}"+":"+str(name)+":"+str(value), field_name = name)


                if operation['operation'] == 'proptype_2nd' and value != '':
                    # logger.info(f"{self.name} Processing columns {name}, with value {value}. Op:{operation}")

                    #register proptype_2nd for the source
                    self.proptype_2nd[operation['source']] = name


                    # prop_type = operation['type']
                    # if prop_type == '' or 'C' not in prop_type:
                    #     raise Exception(f"Propvalue does not have prop type defined. C entity-string expected, got {key}, {name}, {value}")
                    # for item in self.itemize_valuestring_for_multiples(value):
                    #     entity_mapper.hook_prop_object(prop_type = prop_type, input_value = item, origin = operation['operation'] +">"+ str(key)+":"+str(name)+":"+str(value), field_name = name)

                if operation['operation'] == 'propvalue_2nd' and value != '':
                    #logger.info(f"{self.name} propvalue_2nd : Processing columns {name}, with value {value}. Op:{operation}")
                    prop_type = operation['type']
                    prop_source_name = operation['source']  # header_name,  we need concept_id
                    prop_source_id = self.parsing_instruction[prop_source_name]['type']

                    #logger.info(f"OP provalue_2nd with prop_source_name: '{prop_source_name}' : prop_source_id '{prop_source_id}' : value '{value}'")

                    #logger.info(f"There are registered proptype_2nd: {self.proptype_2nd}")
                    # logger.info(f"There are parsing instructions : {self.parsing_instruction}")

                    # assert 'C' in prop_source_id, f"Trying to get to the concept of 1st level property to address 2nd level property. Context {self.name} propvalue_2nd : Processing columns {name}, with value {value}. Op:{operation} in {row}."

                    # hack for Castellario events? other datasets do not need it ? why????
                    #if prop_type == '' and prop_source_id == '':
                    #    prop_type = row[prop_source_name]

                    # there can be two situations
                    # B - proptype is defined in proptype_2nd column
                    if prop_source_name in self.proptype_2nd.keys():
                        # logger.info(f"We have registered source type column {self.proptype_2nd[prop_source_name]} for this propvalue_2nd.")
                        prop_type = row[self.proptype_2nd[prop_source_name]]
                    else:
                        # A - proptype is fixed for the whole column, defined in proptype_2nd
                        if prop_type == '' or 'C' not in prop_type:
                            raise Exception(f"Propvalue_2nd does not have prop type defined. C entity-string expected, got prop_type '{prop_type}', key:{key}, name:{name}, value:{value}")

                    origin = operation['operation'] +">"+ str(key)+f":{row['legacyId']}"+":"+str(name)+":"+str(value)

                    for item in self.itemize_valuestring_for_multiples(value, origin=origin):
                        entity_mapper.hook_prop_object(prop_type = prop_type, input_value = item, prop_source = prop_source_id, origin = origin, field_name = name, prop_source_field = prop_source_name)

                if operation['operation'] == 'special' and value != "":
                    # logger.info(f"SPECIAL {operation} {value}")
                    func = getattr(self, 'special_'+name)
                    func(operation, value, entity_mapper)

                if operation['operation'] == 'reference' and value != "":
                    pass
                if operation['operation'] == 'reference_object' and value != "":
                    pass

                if operation['operation'] == 'reference_part' and value != "":
                    ref_object_legacy_id = operation['ref_legacy_id']

                    if ref_object_legacy_id in row.keys():
                        ref_object_legacy_id = row[ref_object_legacy_id]

                    # logger.info(f"Doing {operation}, {ref_object_legacy_id}, '{value}'. Row {row}.")
                    entity_mapper.hook_ref_object(ref_legacyID = ref_object_legacy_id, input_value = value, origin = operation['operation'] +">"+ ":"+ name + " " +str(value))

                if operation['operation'] == 'relation' and value != "" and value != "NA":
                    relation_type = operation['type']
                    related_object = value

                    id1 = entity_mapper.entity['id']

                    #for order,item in enumerate(reversed(self.itemize_valuestring_for_multiples(related_object)),1):

                    if relation_type == "Synonym":
                        synonym_ids = [id1]
                        for item in self.itemize_valuestring_for_multiples(related_object):
                            if item[0] not in entity_mapper.valid_entity_classes:
                                logger.error(f"The string {item} does not refer to valid entity class - trying to instantiate relation {relation_type} in row {key}. ")
                                continue
                            id_other = entity_mapper.get_entity_id(item, origin = str(key)+ " Getting other relation entity in bilding synonm relation. "+relation_type+ " "+item )
                            synonym_ids.append(id_other)

                        if len(synonym_ids) > 1:
                            entity_mapper.make_relation_synonimic_record(relation_type, synonym_ids, origin=operation['operation'] +">"+ ":"+ relation_type + f" {entity_mapper.entity['legacyId']}" +str(synonym_ids))
                        else:
                            logger.error(f"Heh? Empty synonym_ids in "+operation['operation'] +">"+ ":"+ relation_type + f" {entity_mapper.entity['legacyId']}: " +str(synonym_ids))

                    else:
                        for order,item in enumerate(self.itemize_valuestring_for_multiples(related_object),1):
                            if item[0] not in entity_mapper.valid_entity_classes:
                                logger.error(f"The string {item} does not refer to valid entity class - trying to instantiate relation {relation_type} in row {key}. ")
                                continue
                            id2 = entity_mapper.get_entity_id(item, origin = str(key)+ " Getting second relation entity. "+relation_type+ " "+item )

                            # checking for identification and certainty field
                            if relation_type == "Identification" and name+"_certainty" in row:
                              entity_mapper.make_relation_identity_record(id1, id2, row[name+"_certainty"], origin=operation['operation'] + ">" + ":" + relation_type + f" {entity_mapper.entity['legacyId']}>{item} " + str(id1) + " " + str(id2), order=order * 10)
                            else:
                              entity_mapper.make_relation_record(relation_type, [id1, id2], origin=operation['operation'] +">"+ ":"+ relation_type + f" {entity_mapper.entity['legacyId']}>{item} " +str(id1)+" "+str(id2), order=order*10)
            entity_mapper.entity = eval(str(entity_mapper.entity))
            self.dh.js_objects.append(entity_mapper.entity)

            # make audit records
            entity_mapper.create_audit_record()

            # break  DEV, checking parsing after first iteration


    def special_editor(self, operation, value, entity_mapper, field_name="special_editor"):
        pass

    def special_entry_main_editor(self, operation, value, entity_mapper, field_name="special_editor"):
        pass


class TextParser(Parser):

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        Parser.__init__(self, name, header_df, table_df, keyword_row_id, logger)

    # special methods for fields, which needs fully individual processing
    def special_edition_1(self, operation, value, entity_mapper, field_name="edition_1", ):
        # Parse this col. as "propvalue" - but you need to generate the target entities since they do not exist. How to do it: for any value, create an R entity with "label" = textual value in this col., "label language" = English, "status" = "approved", and "URL" = the hyperlink in the formula sitting on the textual value in this col. As usual, ignore NS and NA values (exact match) - do not import anything if the value is NA.
        # logger.info(f"Special edition1 running ...{operation} {value}")

        origin = operation['operation'] +" "+ operation['type']+ ">"+ ":"+field_name + str(value)
        prop_type = operation['type']

        # make rentity
        # logger.info(f"Rentity making {value}")
        if "|" in value:
            data = value.split("|")
            label = data[0]
            url = data[1]
        else:
            url = ""
            label = value
            # logger.warning(f"Expected char | signaling url after label. Got just {value}."+origin)

        # generate resource entity if it does not exist
        # check by label and url
        tdf = self.dh.tables['resources'].fillna("")
        check_rentity = tdf[(tdf['label'] == label) & (tdf['dissinet_repository_url'] == url)]
        #check_rentity = tdf[(tdf['label'] == label)  & (~tdf['dissinet_repository_url'].isna() | ~(tdf['dissinet_repository_url']==""))]
        if check_rentity.empty:
            rentity = entity_mapper.make_rentity(label, url, origin=origin)
            rentity['language'] = entity_mapper.enum_mapper['language']['English']
        else:
            rentity = {'id': check_rentity.iloc[0]['id']}

        entity_mapper.create_audit_record(entity_id=rentity['id'], object=rentity)
        entity_mapper.hook_prop_object(prop_type = prop_type, input_value = rentity['id'], origin = origin, field_name=field_name)

    def special_edition_2(self, operation, value, entity_mapper):
        self.special_edition_1( operation, value, entity_mapper, field_name="edition_2")

    def special_edition_3(self, operation, value, entity_mapper):
        self.special_edition_1( operation, value, entity_mapper, field_name="edition_3")

    def special_creation_event_id(self, operation, value, entity_mapper : EntityMapper, field_name="creation_event_id"):
        # old instructions
        # Create entities in this col. as new E entities, with (1) the value here as legacy_id, (2) assign (as usual) a new “hash” ID from the db, (3) label of this E: see next col., (4) logical type “definite” (default), (5) label language “English”, (6) status “approved”, and (7) attach to any of those Es the metaprop "(has) - C0565 “class” - C2642 “creation” (to instantiate the event to its event type = event class).

        # new instructionds
        # DONE
        # Create entities in this col. as new E entities, with (1) the value here as legacy_id, (2) assign (as usual) a new "hash" ID from the db, (3) label of this E: see next col., (4) logical type "definite" (default), (5) label language "English", (6) status "approved", and (7) attach to this E the Relation of the type Classification leading to C2642 "creation".

        data = entity_mapper.data_row
        origin = operation['operation']+ " " + data['legacyId'] + ">"+ ":"+field_name +" "+ str(value)

        event_entity = entity_mapper.make_eentity(data['creation_event_label'], legacyId = value, origin = origin)
        event_entity['language'] = entity_mapper.enum_mapper['language']['English']

        # prop_type_id = entity_mapper.get_entity_id("C0565")
        # prop_value_id = entity_mapper.get_entity_id("C2642")
        # make IProp object
        # prop_object = entity_mapper.make_prop_object(prop_type_id, prop_value_id)
        # hook prop object to the event entity
        # event_entity['props'].append(prop_object)
        # hook the vent event to the territory
        # entity_mapper.hook_prop_object(prop_type = "C2642", input_value = event_entity['id'], origin = origin, field_name=field_name)

        # make event part of territories props
        entity_mapper.hook_prop_object(prop_type = "C2642", input_value = event_entity['id'], origin = origin, field_name=field_name)
        # (7) attach to this E the Relation of the type Classification leading to C2642 "creation"
        entity_mapper.make_relation_record('Classification',[event_entity['id'],entity_mapper.get_entity_id("C2642")])

        # process time_relations
        t_relations = [(
            data["timerelation1_type_conceptified_id"], data["timerelation1_target_id"]
        ), (
            data["timerelation2_type_conceptified_id"], data["timerelation2_target_id"]
        ),(
            data["timerelation3_type_conceptified_id"], data["timerelation3_target_id"]
        ), (
            data["timerelation4_type_conceptified_id"], data["timerelation4_target_id"]
        )]

        for o in t_relations:
            if len(o[0]) > 0 and len(o[1]) > 0:
                prop_type_id = entity_mapper.get_entity_id(o[0], origin = origin)
                prop_value_id = entity_mapper.get_entity_id("~V~"+o[1], origin = origin)
                prop_object = entity_mapper.make_prop_object(prop_type_id, prop_value_id)
                event_entity['props'].append(prop_object)

        # create audit record
        entity_mapper.create_audit_record(entity_id=event_entity['id'], object=event_entity)


    # empty, operation is solved by f above
    def special_creation_event_label(self, operation, value, entity_mapper):
        pass


class ActionParser(Parser):

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        Parser.__init__(self, name, header_df, table_df, keyword_row_id, logger)


class ConceptParser(Parser):

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        Parser.__init__(self, name, header_df, table_df, keyword_row_id, logger)

    def special_wordnet_synset_id(self, operation, value, entity_mapper,field_name="special_wordnet_synset_id",):
        # wordnet_resource_id = R0067
        entity_mapper.hook_ref_object(ref_legacyID = "R0067", input_value = value, origin = operation['operation'] +">"+ ":"+field_name + " " +str(value))


class ManuscriptParser(Parser):

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        Parser.__init__(self, name, header_df, table_df, keyword_row_id, logger)

    def special_creation_event_id(self, operation, value, entity_mapper : EntityMapper, field_name="creation_event_id"):
        # Create entities in this col. as new E entities, with (1) the value here as legacy_id, (2) assign (as usual) a new “hash” ID from the db, (3) label of this E: see next col., (4) logical type “definite” (default), (5) label language “English”, (6) status “approved”, and (7) attach to any of those Es the metaprop "(has) - C0565 “class” - C2642 “creation” (to instantiate the event to its event type = event class).

        # new instructions
        # TODO
        # Create entities in this col. as new E entities, with (1) the value here as legacy_id, (2) assign (as usual) a new "hash" ID from the db, (3) label of this E: take from next col., (4) logical type "definite" (default), (5) label language "English", (6) status "approved", and (7) attach to this E the Relation of the type Classification leading to C2642 "creation".

        origin = operation['operation'] +">"+ ":"+field_name +" "+ str(value)

        data = entity_mapper.data_row
        event_entity = entity_mapper.make_eentity(data['creation_event_label'], legacyId = value, origin = origin)
        event_entity['language'] = entity_mapper.enum_mapper['language']['English']

        # OLD way, we have relations now
        #prop_type_id = entity_mapper.get_entity_id("C0565")
        #prop_value_id = entity_mapper.get_entity_id("C2642")
        # make IProp object
        #prop_object = entity_mapper.make_prop_object(prop_type_id, prop_value_id)
        # hook prop object to the event entity
        #event_entity['props'].append(prop_object)

        # hook the vent event to the territory
        entity_mapper.hook_prop_object(prop_type = "C2642", input_value = event_entity['id'], origin = operation['operation'] +">"+ ":"+field_name + str(value))

        # (7) attach to this E the Relation of the type Classification leading to C2642 "creation"
        entity_mapper.make_relation_record('Classification',[event_entity['id'],entity_mapper.get_entity_id("C2642")])

        # process time_relations
        t_relations = [(
            data["timerelation1_type_conceptified_id"], data["timerelation1_target_id"]
        ), (
            data["timerelation2_type_conceptified_id"], data["timerelation2_target_id"]
        ),(
            data["timerelation3_type_conceptified_id"], data["timerelation3_target_id"]
        ), (
            data["timerelation4_type_conceptified_id"], data["timerelation4_target_id"]
        )]

        origin = origin + "LegacyId: "+ data['legacyId']
        for o in t_relations:
            if len(o[0]) > 0 and len(o[1]) > 0:
                prop_type_id = entity_mapper.get_entity_id(o[0], origin = origin)
                prop_value_id = entity_mapper.get_entity_id("~V~"+o[1], origin = origin)
                prop_object = entity_mapper.make_prop_object(prop_type_id, prop_value_id)
                event_entity['props'].append(prop_object)

        # create audit record
        entity_mapper.create_audit_record(entity_id=event_entity['id'], object=event_entity)


    # empty, operation is solved by f above
    def special_creation_event_label(self, operation, value, entity_mapper):
        pass


    def special_repository_label(self, operation, value, entity_mapper, field_name = "repository_label"):
        # For each non-empty, non-NA, non-NS row: (1) generate L entity with label = value in this col., status = “approved”, entity logical type = “definite”, label language = value in the next col. (repository_label_language); (2) append to this L entity a metaprop (has) - C0565 “class” - C2646 “archive or library”, and (3) under the O entity representing the row (i.e. the physical manuscript), add a metaprop which will relate this O to this L entity (repository) through the relation: O - (has) - C2645 “repository” - L in this col.

        origin = f"Making location '{value}' from " + entity_mapper.data_row['legacyId'] + f" by field {field_name}."

        if value != "" and value!="NA" and value!="N/A" and value!="NS":  # check value
            # check whether location exists with the same label
            if self.dh.tables["locations"][self.dh.tables["locations"]['value']==value].empty: # NO
                lentity = entity_mapper.make_lentity(label=value, legacyId="L_from_"+entity_mapper.data_row['legacyId'], origin=origin)
                lentity['language'] = entity_mapper.enum_mapper['language'][entity_mapper.data_row['repository_label_language']]
            else: #YES
                lentity = {}
                lentity['id'] = self.dh.tables["locations"][self.dh.tables["locations"]['value']==value].iloc[0]['id']

            # OLD metaprop way
            #prop_type_id = entity_mapper.get_entity_id("C0565", origin = origin)
            #prop_value_id = entity_mapper.get_entity_id("C2646", origin = origin)
            #prop_object = entity_mapper.make_prop_object(prop_type_id, prop_value_id)
            #lentity['props'].append(prop_object)

            #(2) append to this L entity a RelationType.Classification leading to C2646 "archive or library"
            entity_mapper.make_relation_classification_record(lentity['id'], entity_mapper.get_entity_id('C2646'))

            # create audit record
            entity_mapper.create_audit_record(entity_id=lentity['id'], object=lentity)

            # let the manuscript O own the location
            entity_mapper.hook_prop_object(prop_type = "C2645", input_value = lentity['id'], origin = origin)


    # solves the method above
    def special_repository_label_language(self, operation, value, entity_mapper):
        pass

    def special_reproduction_online_url(self, operation, value, entity_mapper, field_name = "reproduction_online_url"):
        # If non-empty, non-NA, (1) generate an R entity with label "Reproduction of " + label of the MS (i.e. value in the B column, status = “approved”, label-language = “English”, url = the URL sitting under the hyperlink value in this cell, and (2) add metaprop to the O entity represented by this row: O - (has) - C1199 “digital reproduction” - the R entity here generated.

        origin = f"Making Resource entity '{value}' from " + entity_mapper.data_row['legacyId'] + f" by field {field_name}."

        if value != "" and value!="NA" and value!="N/A" and value!="NS":  # check value

            if "|" in value:
                data = value.split("|")
                label = data[0]
                url = data[1]

                if label == "link":
                    label = "Reproduction of " + entity_mapper.data_row['label']

            else:
                url = ""
                label = value
                logger.warning(f"Expected char | signaling url after label. Got just {value}. "+origin)


            tdf = self.dh.tables['resources']
            check_rentity = tdf[(tdf['label'] == label) & (tdf['dissinet_repository_url'] == url)]
            if check_rentity.empty:
                rentity = entity_mapper.make_rentity(label, url, origin=origin)
                rentity['language'] = entity_mapper.enum_mapper['language']['English']
            else:
                rentity = {'id': check_rentity.iloc[0]['id']}

            entity_mapper.hook_prop_object(prop_type = "C1199", input_value = rentity['id'], origin = origin)

            # create audit record
            entity_mapper.create_audit_record(entity_id=rentity['id'], object=rentity)


class ResourceParser(Parser):

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        Parser.__init__(self, name, header_df, table_df, keyword_row_id, logger)


class PersonParser(Parser):

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        Parser.__init__(self, name, header_df, table_df, keyword_row_id, logger)

    # TODO implement
    #def special_introducers_id(self, operation, value, entity_mapper, field_name = "introducers_id"):
    #    pass

class GroupParser(Parser):

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        Parser.__init__(self, name, header_df, table_df, keyword_row_id, logger)


class EventParser(Parser):

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        Parser.__init__(self, name, header_df, table_df, keyword_row_id, logger)

    def checkTerritoryExists(self,legacyId):

        if "-" in legacyId:
            if pd.DataFrame(self.dh.additional_entities)[pd.DataFrame(self.dh.additional_entities)['legacyId']== legacyId].empty:
              # logger.info(f"CheckTerritoryExists through '-' for {legacyId}. Returning false.")
              return False
            else:
              # logger.info(f"CheckTerritoryExists through '-' for {legacyId}. Returning true.")
              return True
        else: # main text
            if self.dh.tables["texts"][self.dh.tables["texts"]["legacyId"]==legacyId].empty:
              # logger.info(f"CheckTerritoryExists through 'tableTexts' for {legacyId}. Returning false.")
              return False
            else:
              # logger.info(f"CheckTerritoryExists through 'tableTexts' for {legacyId}. Returning true.")
              return True

    def special_subterritory_id(self, operation, value, entity_mapper, field_name = "subterritory_id"):
        # Light yellow: document aka Territory metadata (not Event).
        # please generate these T entities following Adam's script for parsing Robert's Sellan coding sheet IDs into a hierarchical T structure
        # and put them under their proper root T through legacy IDs (first element of ID = root T ID).
        # E.g. here, in Guglielmites, there is root, i.e. the whole T; then parts 1-4; and underneath them, the individual documents.
        # Entity type = T; T label and label_language defined in the two respective cols.; entity_logical_type = definite; status = approved. Other metadata set as metaprops in the following yellow cols.

        datarow = entity_mapper.data_row.copy()

        # override of legacyId
        # datarow['legacyId'] = value

        # create territory proper
        trt = self.EMP.make(entity_name="ITerritory", data_row=datarow)
        trt.make_alive(legacyId= datarow["subterritory_id"], label=datarow['document_label'], label_language=datarow['document_label_language'], register_id_where="texts")

        trt.create_audit_record(entity_id=trt.entity['id'], object=trt.entity)

        # propvalues
        prop_value_fields = {"state_of_conservation_id":"C3440", "participant_id":"C2863", "inquisitor_id":"C1541", "notary_id":"C1652", "witness_assessor_id":"C1540"}

        for pvf, concept in prop_value_fields.items():
            if pvf not in entity_mapper.data_row:
                continue
            for item in self.itemize_valuestring_for_multiples(datarow[pvf]):
                if item != "":
                    trt.hook_prop_object(prop_type = concept, input_value = item)

        # metaprop territory represent events
        trt.hook_prop_object(prop_type = "C2286", input_value = entity_mapper.entity['id'])


        # genre relation, "genre_id":"C0335",
        for item in self.itemize_valuestring_for_multiples(datarow["genre_id"]):
            if item != "" in  item:
                if "C" in item:
                    trt.make_relation_record("Classification",[trt.entity['id'], entity_mapper.get_entity_id(item)])
                else:
                    logger.error(f"Creating territory through event generation:  did not get C entity for its classifications. Got '{item}'.")

        # audit record
        trt.create_audit_record(entity_id=trt.entity['id'], object=trt.entity)

        # check the ancestry #####################################################
        t_parts = trt.entity['legacyId'].split("-")
        size = len(t_parts)


        # save order
        trt.entity['data']['parent']['order'] = int(t_parts[-1])

        # if exists, connect, if doesnt, create, connect to root and connect the lowest part to the new middle
        if size == 3: # = the processing territory has 3 parts
            checked_territory_lid = "-".join(t_parts[0:-1])
            # logger.info(f" Trying to go with {checked_territory_lid}. Size 3 because processing {trt.entity['legacyId']}.")
            if not self.checkTerritoryExists(checked_territory_lid): #  parent territory does not exist
                trt_new = self.EMP.make(entity_name="ITerritory", data_row=datarow)
                trt_new.make_alive(legacyId= checked_territory_lid, label=t_parts[1], label_language=datarow['document_label_language'], register_id_where="texts")
                parent_id = trt_new.entity['id']

                checked_territory_lid = "-".join(t_parts[0:-2])
                if self.checkTerritoryExists(checked_territory_lid):
                    root_territory_id = self.dh.entity_ids["texts"][checked_territory_lid]
                    trt_new.entity['data']['parent']['territoryId'] = root_territory_id
                    trt_new.entity['data']['parent']['order'] = int(t_parts[-2])
                    # logger.info(f"Writing {trt_new.entity['data']['parent']['territoryId']} to {trt_new.entity['id']}, {trt_new.entity['legacyId']}")
                else:
                    logger.error(f"The root territory {checked_territory_lid} does not exists.")

                # audit record
                trt_new.create_audit_record(entity_id=trt_new.entity['id'], object=trt_new.entity)
            else:
                parent_id =  self.dh.entity_ids['texts'][checked_territory_lid]


            # territory does exist, connect the triggering territory to its parent
            trt.entity['data']['parent']['territoryId'] = parent_id
            # logger.info(f"Writing {trt.entity['data']['parent']['territoryId']} to {trt.entity['id']}, {trt.entity['legacyId']}")
        elif size == 2:
            # just connect it to the supposedly existing root
            checked_territory_lid = "-".join(t_parts[0:1])
            if self.checkTerritoryExists(checked_territory_lid):
                root_territory_id = self.dh.entity_ids["texts"][checked_territory_lid]
                trt.entity['data']['parent']['territoryId'] = root_territory_id
                trt.entity['data']['parent']['order'] = int(t_parts[-1])
                # logger.info(f"Writing {trt.entity['data']['parent']['territoryId']} to {trt.entity['id']}, {trt.entity['legacyId']}")
            else:
                logger.error(f"The root territory {checked_territory_lid} does not exists.")


class LocationParser(Parser):

    def __init__(self, name, header_df: pd.DataFrame, table_df: pd.DataFrame, keyword_row_id: int, logger: logger):
        Parser.__init__(self, name, header_df, table_df, keyword_row_id, logger)

    def special_modern_name(self, operation, value, entity_mapper, field_name = "special_modern_name"):
        # "For non-empty, generate new L entities from this col.
        # 1) Attribute values: label = this col.; status = ""approved"", label_language = next col., entity_logical_type = same as col. D.
        # 2) Create ""identical entity"" relation between the Latin entity captured by this row (""id"") and this new entity.  Exact structure TBA (awaiting Adam) - until it is, create the relation as follows: append a metaprop to the original Latin location in ""id"", which will say: [""id"" Location] - has - C0691 identical entity - [modern location created from modern_name].)
        # 3) Attach ""class"" metaprop to this modern location from col. ""modern_name_class_id"" (described by the regular instructions)."

        origin = f"Making Location entity '{value}' from " + entity_mapper.data_row['legacyId'] + f" by field {field_name}."
        language = entity_mapper.data_row['modern_name_language']

        if value != "" and value!="NA" and value!="N/A" and value!="NS":  # check value
            label = value
            lentity = entity_mapper.make_lentity(label, origin=origin)
            lentity['language'] = entity_mapper.enum_mapper['language'][language]


            # create settlement prop OLD
            #  pt C0565  value in modern_name_class_id  OLD
            # prop_type = "C0565"
            # prop_value = entity_mapper.data_row['modern_name_class_id'] # another C
            #
            # for item in self.itemize_valuestring_for_multiples(prop_value, origin=origin):
            #     prop_type_id, prop_value_id = entity_mapper.prepare_prop_object_data(prop_type, item, origin=origin)
            #
            #     # make IProp object
            #     prop_object = entity_mapper.make_prop_object(prop_type_id, prop_value_id)
            #     # append prop to the location entity
            #     lentity['props'].append(prop_object)

            # make classification for C0565 job
            # logger.info(f"{entity_mapper.data_row}")
            class_value = entity_mapper.data_row['modern_name_class_id'] # another C
            for item in self.itemize_valuestring_for_multiples(class_value, origin=origin):
                entity_mapper.make_relation_record('Classification', [lentity['id'], entity_mapper.get_entity_id(item)])


            # make identity relation
            # {type: RelationType.Identification, entityIds: [Location 1 id, Location 2 id], certainty: [Certainty.Certain]},
            # {type: "I", entityIds: [Location 1 id, Location 2 id], certainty: "1"},
            entity_mapper.make_relation_identity_record(entity_mapper.entity['id'], lentity['id'], "1")

            # create audit record
            entity_mapper.create_audit_record(entity_id=lentity['id'], object=lentity)

    def special_name_latin(self, operation, value, entity_mapper, field_name="special_name_latin"):
      # "MACHINE
      # For non-empty values:
      # 1) IF (this procedure has not yet created an L entity of the same label)
      #    - Generate a new L entity from this col., with the following attribute values: label = value in this col.; status = ""approved"", label_language = Latin, entity_logical_type = same as value in col. D.
      #    - Attach RelationType.Classification to this modern location from col. ""class_id"".
      #   - Attach all metaprops (e.g. coordinates) and relations (e.g. superordinates) of the basic L entity (row) also to this new entity.
      # ELSE
      #    - Use the already created L entity (recognized by label) as ""target entity"".
      # END IF
      # 2) Relate the L entity described by the row with this machine-generated target entity through RelationType.Identification, certainty = certain."

      for item in self.itemize_valuestring_for_multiples(value, origin=field_name+" "+value):

        origin = f"Making Location entity '{item}' from " + entity_mapper.data_row[
          'legacyId'] + f" by field {field_name}."
        language = "Latin" # entity_mapper.data_row['modern_name_language']


        if item != "" and item != "NA" and item != "N/A" and item != "NS":  # check value
          # check, whether the location does not exist
          if self.dh.tables["locations"][self.dh.tables["locations"]['value']==item].empty:
            label = item
            lentity = entity_mapper.make_lentity(label, origin=origin)
            lentity['language'] = entity_mapper.enum_mapper['language'][language]
            lentity['data']['logicalType'] =  entity_mapper.data_row['entity_logical_type']

            # make classification for the new entity
            # logger.info(f"{entity_mapper.data_row}")
            class_value = entity_mapper.data_row['class_id']  # another C
            for item in self.itemize_valuestring_for_multiples(class_value, origin=origin):
              entity_mapper.make_relation_record('Classification', [lentity['id'], entity_mapper.get_entity_id(item)])
          else:
            lentity = {}
            lentity['id'] = ""

          # make identity relation
          # {type: RelationType.Identification, entityIds: [Location 1 id, Location 2 id], certainty: [Certainty.Certain]},
          # {type: "I", entityIds: [Location 1 id, Location 2 id], certainty: "1"},
          entity_mapper.make_relation_identity_record(entity_mapper.entity['id'], lentity['id'], "1")

          # create audit record
          entity_mapper.create_audit_record(entity_id=lentity['id'], object=lentity)

    def special_name_latin_alternative(self, operation, value, entity_mapper, field_name="special_modern_name"):
      self.special_name_latin(operation, value, entity_mapper, field_name="special_name_latin_alternative")
