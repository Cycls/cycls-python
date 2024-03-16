from pydantic import BaseModel, field_validator



class AppConfiguration(BaseModel):
    handler:str
    name: str | None = None
    image: str | None = None
    introduction: str| None = None
    suggestions: list[str] | None = None

    @field_validator("suggestions", mode="before")
    @classmethod
    def process_suggestions(cls, suggestions:list[str] | None) -> list[str] | None:
        if not suggestions:
            return None
        elif isinstance(suggestions, list):
            if len(suggestions) <= 4:
                return suggestions
            else:
                raise Exception(f"suggestions can be at max 4")


    # @field_validator("image", mode="before")
    # @classmethod
    # def process_image(cls, image:str | None) -> str:
    #     return image
