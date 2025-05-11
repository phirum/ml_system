from app.api.endpoints import model

api_router.include_router(model.router, prefix="/model")
api_router.include_router(user.router, prefix="/users")
