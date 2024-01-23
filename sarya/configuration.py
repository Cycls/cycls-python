from pydantic import BaseModel


class AppNameLocale(BaseModel):
    ar: str | None = None
    en: str | None = None

class ImageUploader:
    def __inti__(self, path:str):
        pass

class AppConfiguration:
    def __init__(
        self,
        name: str | AppNameLocale = None,
        test: bool = False,
        image: str | ImageUploader = None, 
        description: str = None,
    ):
        self.name = self._process_name(name)
        self.test = test
        self.image = self._process_image(image)
        self.description = description
    
    def _process_name(self, name:str | AppNameLocale)->AppNameLocale:
        if isinstance(name, str):
            return AppNameLocale(en=name)
        elif isinstance(name, AppNameLocale):
            return name
    
    def _process_image(self, image):
        return ""
