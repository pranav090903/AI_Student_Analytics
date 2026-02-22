from fastapi import APIRouter, Depends, HTTPException
from features.auth.dependencies import get_current_user
from features.copilot.schemas import TeacherChatRequest
from features.copilot.service import teacher_copilot_chat

router = APIRouter(prefix="/copilot", tags=["Copilot"])

@router.post("/chat")
def chat(request: TeacherChatRequest, user=Depends(get_current_user)):
    
    # Permission Check
    if user["role"].lower() != "teacher":
        raise HTTPException(
            status_code=403, 
            detail="Only teachers can access this copilot"
        )

    try:
        response = teacher_copilot_chat(
            message=request.message,
            username=user["username"]
        )

        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
