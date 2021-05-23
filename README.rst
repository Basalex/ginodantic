
Ginodantic
===========================

Generate pydantic schema from gino models

| Python 3.7+


| **Install**: ``pip install ginodantic``

**Github**: https://github.com/Basalex/ginodantic


| Generating custom schemas

* **Meta Class Options**
    * **as_dataclass: bool** -> pydantic dataclass will be used for generated schema
    * **as_list_fields: Tuple[str]** -> listed fields will be generated as List[type]
    * **field_methods: bool** -> int and float fields will be generated with postfix __ge, and postfix __le,
    * **field_methods_by_name: Dict[str, List[str]]** -> use database field names instead of model field names
    * **fields: Tuple[str]** -> only listed fields will be used for generated schema
    * **field_methods: Tuple[str]** -> excludes listed fields from generated schema
    * **exclude: Tuple[str]** -> excludes listed fields from generated schema
    * **list_pk: bool** -> Foreign key and primary key will be interpreted as list
    * **required: Tuple[str]** -> only listed fields will be defined as required, can be set as empty tuple
    * **use_db_names: bool** -> use database field names instead of model field names

Examples of usage:
~~~~~~~~~~~~~~~~~~

.. code:: python

    from ginodantic import BaseModelSchema

    class UserSchema(BaseModelSchema):
        class Meta:
            model: User
            required: ()
            exclude: ('email', )
            use_db_names: False
            field_methods_by_name = {'age': ('le', 'ge')}

| This would be almost equal to the following schema

.. code:: python

    class UserSchema(BaseModel):
        id: Optional[int] = None
        username: Optional[str] = None
        age__le: Optional[str] = None
        age__ge: Optional[str] = None
