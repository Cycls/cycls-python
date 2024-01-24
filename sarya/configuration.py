from pydantic import BaseModel, field_validator

class AppNameLocale(BaseModel):
    ar: str | None = None
    en: str | None = None

class ImageUploader(BaseModel):
    path:str

class AppConfiguration(BaseModel):
    handler:str
    name: str | AppNameLocale| None = None,
    test: bool = False,
    image: str | ImageUploader| None = None, 
    release: str | None = None,
    description: str| None = None,
    

    @field_validator("name", mode="before")
    @classmethod
    def process_name(cls, name:str | AppNameLocale)->AppNameLocale:
        if isinstance(name, str):
            return AppNameLocale(en=name)
        elif isinstance(name, AppNameLocale):
            return name
   
    @field_validator("image", mode="before")
    @classmethod
    def process_image(cls, image:str | ImageUploader) -> str:
        return image
