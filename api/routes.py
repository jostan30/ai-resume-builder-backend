from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.ai_generator import ai_generator
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class AIContentRequest(BaseModel):
    section: str  # "summary" or "skills"
    jobTitle: str

class AIContentResponse(BaseModel):
    summary: str = None
    skills: list = None
    error: str = None

@router.post("/generate-ai-content", response_model=AIContentResponse)
async def generate_ai_content(request: AIContentRequest):
    """Generate AI content for resume based on job title"""
    try:
        logger.info(f"Generating mock {request.section} for job title: {request.jobTitle}")
        
        response = AIContentResponse()
        
        if not request.jobTitle:
            raise HTTPException(status_code=400, detail="Job title is required")
        
        if request.section == "summary":
            response.summary = ai_generator.generate_summary(request.jobTitle)
        elif request.section == "skills":
            response.skills = ai_generator.generate_skills(request.jobTitle)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported section: {request.section}. Use 'summary' or 'skills'."
            )
            
        logger.info(f"Successfully generated {request.section}")
        return response
        
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        response = AIContentResponse(error=f"Failed to generate {request.section}: {str(e)}")
        return response