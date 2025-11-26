from fastapi import APIRouter
from app.models.schemas import AutocompleteRequest
from app.models.response import ApiResponse
from app.services.autocomplete_service import AutocompleteService
from app.exceptions import ValidationException

router = APIRouter(tags=["autocomplete"])

@router.post("/autocomplete", response_model=ApiResponse)
def get_autocomplete(request: AutocompleteRequest):
    try:
        suggestion = AutocompleteService.get_suggestion(
            request.code, 
            request.cursorPosition, 
            request.language
        )
        return ApiResponse(
            success=True,
            message="Autocomplete suggestion generated",
            data={"suggestion": suggestion}
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            message="Failed to generate suggestion",
            data=None,
            error_code="AUTOCOMPLETE_ERROR"
        )