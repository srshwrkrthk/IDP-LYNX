from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_user
from app.services.event_service import list_user_events

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("")
def get_events(
    limit: int = Query(default=50, ge=1, le=200),
    current_user=Depends(get_current_user),
):
    events = list_user_events(
        user_id=str(current_user.id),
        limit=limit,
    )

    return {
        "count": len(events),
        "events": events,
    }