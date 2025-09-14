from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import citizens_converter
# from routers import znpcs_converter  # TODO: Uncomment when implementing zNPCs
# from routers import znpcsplus_converter # TODO

app = FastAPI(
    title="NPC Converter API",
    description="Convert between different NPC plugin formats",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(citizens_converter.router, prefix="/citizens", tags=["Citizens"])
# app.include_router(znpcs_converter.router, prefix="/znpcs", tags=["zNPCs"])  # TODO: Uncomment when implementing

@app.get("/")
async def root():
    return {
        "message": "NPC Converter API",
        "version": "1.0.0",
        "available_converters": [
            "Citizens NPC → FancyNPCs"
            # "zNPCs → FancyNPCs"  # TODO: Add when implemented
            # "zNPCsPlus → FancyNPCs" # TODO
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7000)
