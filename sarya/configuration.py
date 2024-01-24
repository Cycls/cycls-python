from pydantic import BaseModel, field_validator

class AppNameLocale(BaseModel):
    ar: str | None = None
    en: str | None = None

class ImageUploader:
    def __inti__(self, path:str):
        pass

class AppConfiguration(BaseModel):
    handler:str
    name: str | AppNameLocale = None,
    test: bool = False,
    image: str | ImageUploader = None, 
    release: str | None = None,
    description: str = None,
    

    @field_validator("name", mode="before")
    @classmethod
    def process_name(cls, name:str | AppNameLocale)->AppNameLocale:
        if isinstance(name, str):
            return AppNameLocale(en=name)
        elif isinstance(name, AppNameLocale):
            return name
    @field_validator("image", mode="before")
    @classmethod
    def process_image(self, image):
        return image
