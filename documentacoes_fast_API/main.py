from fastapi import HTTPException, FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserResponse(BaseModel):
    user_id: str
    name: str

class ErrorResponse(BaseModel):
    detail: str

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "ID de usuário inválido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "O ID de usuário fornecido não é válido."
                    }
                }
            }
        },
        404: {
            "model": ErrorResponse,
            "description": "Usuário não encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Usuário não encontrado."
                    }
                }
            }
        },
        500: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Erro inesperado. Tente novamente mais tarde."
                    }
                }
            }
        }
    }
)
async def get_user(user_id: str):
    if not user_id.isdigit():
        raise HTTPException(status_code=400, detail="O ID de usuário fornecido não é válido.")
    
    if user_id != "1234":
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    try:
        return {"user_id": user_id, "name": "Ivan"}
    except Exception:
        raise HTTPException(status_code=500, detail="Erro inesperado. Tente novamente mais tarde.")