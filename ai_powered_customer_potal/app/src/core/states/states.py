from typing import  Annotated
from pydantic import BaseModel, Field
import operator
from typing import Annotated, List, Tuple
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import  Annotated
from langchain_core.messages import AnyMessage


class PlanExecute(TypedDict):
    input: str
    Recommendation: List[str]
    messages: Annotated[list[AnyMessage], add_messages]


class Recommendation(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )