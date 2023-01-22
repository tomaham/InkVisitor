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

  def checkIDs(cls, fix_difference = False):
    # between tables and entity_ids
    errors = 0
    for k, t in cls.tables.items():
      table_errors = 0

      print("############## " + k)
      if k in [ 'values', 'locations', 'events', 'props', 'relations']:
        continue

      dupl_legacy_ids = t['legacyId'].duplicated()
      # check for duplicates
      if any(dupl_legacy_ids):
        dupls = t['legacyId'][dupl_legacy_ids]
        print(f"There are duplicates! {dupls}")

      datagroup = k.split("_")[-1]
      print(f"Data group: {datagroup}")
      for id, row in t.iterrows():

        legacyId = row['legacyId']
        # print(f"{datagroup}, {legacyId}")
        if len(str(legacyId)) > 1:

          if legacyId in cls.entity_ids[datagroup]:
            entity_uid = cls.entity_ids[datagroup][legacyId]
          else:
            entity_uid = row['id']
            cls.entity_ids[datagroup][legacyId] = row['id']

          if entity_uid != row['id']:
            # print(f"ERROR within {legacyId}, there is difference in uuids (t {row['id']}, e {entity_uid}).")

            table_errors += 1
            errors += 1

            if fix_difference:
              print(f"Corrected ERROR within {legacyId}, there were differences in uuids (t {row['id']}, e {entity_uid}).")
              #cls.entity_ids[datagroup][legacyId] = row['id']
              # let's make the fix from the other side
              cls.tables[k].at[id,'id'] = entity_uid

      print(f"############## " + k + f" {table_errors}.")

    print(f"There were {errors} errors in total.")



