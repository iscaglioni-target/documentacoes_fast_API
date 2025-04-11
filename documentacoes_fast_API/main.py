from fastapi import HTTPException, FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserResponse(BaseModel):
    user_id: str
    name: str

class ErrorResponse(BaseModel):
    detail: str

codigos_erro = [
    {"status": 400, "mensagem": "O ID de usuário fornecido não é válido."},
    {"status": 404, "mensagem": "Usuário não encontrado"},
    {"status": 500, "mensagem": "Erro interno do servidor"}
    ]

class Examples_erros:
    def __init__(self, status: int, description: str):
        self.status = status
        self.description = description
        

    def montar_erro(self):
        return {
            self.status : {
                "model": ErrorResponse,
                "description": self.description,
                "content": {
                    "application/json": {
                    "example": {
                    "detail": self.description
                    }
                }
                }

            }

        }    
    
erro400 = Examples_erros(status=codigos_erro[0]["status"], description=codigos_erro[0]["mensagem"])
erro404 = Examples_erros(status=codigos_erro[1]["status"], description=codigos_erro[1]["mensagem"])
erro500 = Examples_erros(status=codigos_erro[2]["status"], description=codigos_erro[2]["mensagem"])

responses = {}
responses.update(erro404.montar_erro())
responses.update(erro400.montar_erro())
responses.update(erro500.montar_erro())

usuarios = [
    {"id": 1, "nome": "Ivan"},
    {"id": 2, "nome": "Rafael"},
    {"id": 1, "nome": "Sávio"},
]

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    responses= responses
)
async def get_user(user_id: str):
    if not user_id.isdigit():
        raise HTTPException(status_code=codigos_erro[0]["status"], detail=codigos_erro[0]["mensagem"])
    
    for id in user_id:
        if user_id != id:
            raise HTTPException(status_code=codigos_erro[1]["status"], detail=codigos_erro[1]["mensagem"])
    
    try:
        return {"user_id": user_id, "name": "Ivan"}
    except Exception:
        raise HTTPException(status_code=codigos_erro[2], detail=codigos_erro["mensagem"])