from extensions import db
from sqlalchemy import asc,desc, or_


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    num_of_servings = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    directions = db.Column(db.String(1000))
    is_publish = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    cover_image = db.Column(db.String(100), default=None)

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    
    # def data(self):
    #     return {
    #         'id':self.id,
    #         'name':self.name,
    #         'description':self.description,
    #         'num_of_servings':self.num_of_servings,
    #         'cook_time':self.cook_time,
    #         'directions':self.directions,
    #         'user_id':self.user_id
    #     }
        
    @classmethod
    def get_all_published(cls, q, page, per_page, sort, order):
        keyword = '%{keyword}%'.format(keyword=q)
        if order == 'asc':
            sort_logic = asc(getattr(cls,sort))
        else:
            sort_logic = desc(getattr(cls, sort))
        return cls.query.filter(or_(cls.name.ilike(keyword), cls.description.ilike(keyword)), cls.is_publish.is_(True)).order_by(sort_logic).paginate(page=page,per_page=per_page)
    
    @classmethod
    def get_by_id(cls, recipe_id):
        return cls.query.filter_by(id = recipe_id).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_all_by_user(cls, user_id, visibility='public'):
        if visibility == 'public':
            return cls.query.filter_by(user_id=user_id,is_publish=True).all()
        elif visibility == 'private':
            return cls.query.filter_by(user_id=user_id, is_publish=False).all()
        else:
            return cls.query.filter_by(user_id=user_id).all()
        
    # def __init__(self, name, description, num_of_servings, cook_time, directions) -> None:
    #     self.id = get_last_id()
    #     self.name = name
    #     self.description = description
    #     self.num_of_servings = num_of_servings
    #     self.cook_time = cook_time
    #     self.directions = directions
    #     self.is_publish  = False
        
    # @property
    # def data(self):
    #     return {
    #         'id':self.id,
    #         'name':self.name,
    #         'description':self.description,
    #         'num_of_servings':self.num_of_servings,
    #         'cook_time':self.cook_time,
    #         'directions':self.directions
    #     } 