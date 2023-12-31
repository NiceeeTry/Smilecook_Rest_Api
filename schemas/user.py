from marshmallow import Schema, fields
from utils import hash_password
from flask import url_for

class UserSchema(Schema):
    class Meta:
        ordered = True
        
    id =fields.Int(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Method(required=True, deserialize='load_password')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    avatar_url = fields.Method(serialize='dump_avatar_url')
    
    def dump_avatar_url(self,user):
        if user.avatar_image:
            link = url_for('static',filename='images/avatars/{}'.format(user.avatar_image),_external=True)
            return link
        else:
            link = url_for('static',filename='images/assets/default-avatar.avif',_external=True)
            return link
    def load_password(self, value):
        return hash_password(value)
