from enum import Enum
from pydantic import BaseModel, Field


class BGSelectionValue(str, Enum):
    B = "Boy"
    G = "Girl"


class formModel(BaseModel):
    """Primitive for Google Form"""

    boy_or_girl: BGSelectionValue = Field(default="")
    Any_words_of_advice: str = Field(
        default="", description="For us first time parents!"
    )
    name_suggestions: str = Field(
        default="", description="Your favorites or whatever you think will fit!"
    )
    your_name: str = Field(
        ...,
        min_length=2,
        description="Help us know who gets bragging rights!",
        regex="^(?!\\s*$).+",  # Prevents whitespace-only strings
    )
