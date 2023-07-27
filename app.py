from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt, image_set

from resources.user import UserListResource, UserResource, MeResource, UserRecipeListResource, UserActivateResource,UserAvatarUploadResource
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource

from resources.token import TokenResource, RefreshResourse,RevokeResource, black_list
from flask_uploads import configure_uploads, patch_request_class


def create_app():
    app =  Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
    migrate = Migrate(app,db)
    jwt.init_app(app)
    configure_uploads(app,image_set)
    patch_request_class(app,10*1024*1024)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list
    # @jwt.token_in_blocklist_loader
    # def check_if_token_revoked(jwt_header, jwt_payload):
    #     jti = jwt_payload["jti"]
    #     token = db.session.query().filter_by(jti=jti).scalar()
    #     return token is not None
    
    
def register_resources(app):
    api = Api(app)
    
    api.add_resource(MeResource,'/me')
    
    api.add_resource(UserListResource,'/users')
    api.add_resource(UserResource,'/users/<string:username>')
    api.add_resource(UserRecipeListResource, '/users/<string:username>/recipes')
    api.add_resource(UserActivateResource, '/users/activate/<string:token>')
    api.add_resource(UserAvatarUploadResource, '/users/avatar')
    
    api.add_resource(TokenResource,'/token')
    api.add_resource(RefreshResourse,'/refresh')
    api.add_resource(RevokeResource,'/revoke')
    
    api.add_resource(RecipeListResource,'/recipes')
    api.add_resource(RecipeResource,'/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource,'/recipes/<int:recipe_id>/publish')


if __name__=='__main__':
    app = create_app()
    app.run(port=5000, debug=True)