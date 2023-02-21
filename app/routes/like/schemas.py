from pydantic import BaseModel


class Like(BaseModel):
    post_id: int
    action: bool  # true = add vote, false = remove vote
