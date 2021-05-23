from pydantic.main import BaseModel

from ginodantic.gino_model_meta import GinoModelMeta


class BaseModelSchema(BaseModel, metaclass=GinoModelMeta):
    pass

