from pydantic import BaseModel


class Prompt(BaseModel):
    ''' Prompt dataclass '''

    role: str
    content: str


__all__ = (
    'Prompt',
)
