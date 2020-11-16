from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModelMixin:

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save_many(model, data):
        for airport in data:
            for k, v in airport.items():
                if k in ('latitude', 'longitude', 'altitude', 'timezone'):
                    if isinstance(v, str) and v == '':
                        airport[k] = None

        db.session.bulk_insert_mappings(model, data)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def update(cls, id, **kwargs):
        result = cls.query.get(id)
        for k, v in kwargs.items():
            setattr(result, k, v)
        return result
