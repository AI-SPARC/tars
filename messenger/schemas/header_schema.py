from pydantic import BaseModel, Field

class Header(BaseModel):
    headerId: int = Field(..., description="ID do cabeçalho da mensagem.")
    timestamp: str = Field(..., description="Timestamp no formato ISO 8601, UTC.")
    version: str = Field(..., description="Versão do protocolo no formato [Major].[Minor].[Patch].")
    manufacturer: str = Field(..., description="Fabricante do AGV.")
    serialNumber: str = Field(..., description="Número de série único do AGV.")