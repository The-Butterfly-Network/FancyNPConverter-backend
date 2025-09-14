from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import yaml
import tempfile
import os
from services.citizens_service import CitizensConverterService
from models.npc_models import ConversionResponse

router = APIRouter()
converter_service = CitizensConverterService()

@router.post("/to-fancynpcs", response_model=ConversionResponse)
async def convert_citizens_to_fancynpcs(file: UploadFile = File(...)):
    """
    Convert Citizens NPC YAML file to FancyNPCs format
    """
    # Validate file extension
    if not file.filename.endswith(('.yml', '.yaml')):
        raise HTTPException(status_code=400, detail="File must be a YAML file (.yml or .yaml)")
    
    try:
        # Read the uploaded file
        content = await file.read()
        yaml_content = content.decode('utf-8')
        
        # Convert Citizens format to FancyNPCs format
        converted_content = converter_service.convert_to_fancynpcs(yaml_content)
        
        # Create temporary file for output
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yml', prefix='npc_') as temp_file:
            temp_file.write(converted_content)
            temp_file_path = temp_file.name
        
        # Rename to ensure output is named npc.yml
        output_dir = os.path.dirname(temp_file_path)
        output_path = os.path.join(output_dir, 'npc.yml')
        if os.path.exists(output_path):
            os.unlink(output_path)
        os.rename(temp_file_path, output_path)
        
        # Return the converted file
        return FileResponse(
            path=output_path,
            filename="npc.yml",
            media_type="application/x-yaml",
            background=lambda: os.unlink(output_path) if os.path.exists(output_path) else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@router.get("/info")
async def get_citizens_converter_info():
    """Get information about the Citizens converter"""
    return {
        "name": "Citizens NPC Converter",
        "description": "Converts Citizens NPC YAML files to FancyNPCs format",
        "supported_formats": {
            "input": "Citizens NPC YAML",
            "output": "FancyNPCs YAML"
        },
        "features": [
            "Preserves NPC location and rotation",
            "Extracts skin textures from base64 encoded data",
            "Converts hologram text to display names",
            "Maps look-at-player behavior",
            "Generates new UUIDs for target format"
        ]
    }