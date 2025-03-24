from fastapi import APIRouter
from .endpoints import auth, users, members, groups, projects, contributions, pledges

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(contributions.router, prefix="/contributions", tags=["contributions"])
api_router.include_router(pledges.router, prefix="/pledges", tags=["pledges"]) 