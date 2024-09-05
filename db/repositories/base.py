from db.models import BaseModel


class BaseRepository:
    model: BaseModel = BaseModel
    model_name: str

    def __init__(self, model: BaseModel = None):
        if model:
            self.model = model

    def create(self, **kwargs):
        return self.model.create(**kwargs)

    def get_list(self, **filters):
        return self.model.select().filter(**filters).execute()

    def get(self, **filters):
        return self.model.select().filter(**filters).first()

    def update(self, model, **kwargs):
        return self.model.update(**kwargs).where(self.model.id == model.id).execute()

    def delete(self, model):
        return self.model.delete().where(self.model.id == model.id).execute()
