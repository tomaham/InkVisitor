import pandas as pd

# SINGLETON
class DataHolder(object):
  _instance = None
  tables = {}
  header_infos = {}
  entity_ids = {}
  table_to_entity = {}
  editors = {}

  additional_entities = []
  relation_records = []
  audits = []

  js_objects = []

  def __new__(cls,):
    if cls._instance is None:
       print('Creating the DataHolder singleton object')
       cls._instance = super(DataHolder, cls).__new__(cls)

    return cls._instance


  def pass_data(cls,  tables, header_infos, entity_ids, table_to_entity, editors):
    cls.tables =  tables
    cls.header_infos =  header_infos
    cls.entity_ids =  entity_ids
    cls.table_to_entity =  table_to_entity
    cls.editors = editors

    cls.tables['values'] = pd.DataFrame(columns=['id', 'value', 'origin'])
    cls.tables['locations'] = pd.DataFrame(columns=['id', 'value', 'origin', 'legacyId'])
    cls.tables['events'] = pd.DataFrame(columns=['id', 'value', 'origin', 'legacyId'])
    cls.tables['props'] = pd.DataFrame(
      columns=['id', 'type', 'type_id', 'value', 'value_id', 'original_field', 'origin', 'entityId', 'legacyId'])
    cls.tables['relations'] = pd.DataFrame(columns=['id', 'type', 'logic', 'certainty', 'entityIds', 'origin'])

  def reset_generated_collection(cls):
    cls.additional_entities = []
    cls.relation_records = []
    cls.audits = []
    cls.js_objects = []

    cls.tables['values'] = pd.DataFrame(columns=['id', 'value', 'origin'])
    cls.tables['locations'] = pd.DataFrame(columns=['id', 'value', 'origin', 'legacyId'])
    cls.tables['events'] = pd.DataFrame(columns=['id', 'value', 'origin', 'legacyId'])
    cls.tables['props'] = pd.DataFrame(
      columns=['id', 'type', 'type_id', 'value', 'value_id', 'original_field', 'origin', 'entityId', 'legacyId'])
    cls.tables['relations'] = pd.DataFrame(columns=['id', 'type', 'logic', 'certainty', 'entityIds', 'origin'])
