from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, members, groups, contributions, sms, reports

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(contributions.router, prefix="/contributions", tags=["contributions"])
api_router.include_router(sms.router, prefix="/sms", tags=["sms"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"]) 