import os
from enum import StrEnum

from iso639 import Language, LanguageNotFoundError
from pydantic import (
    DirectoryPath,
    Field,
    HttpUrl,
    PositiveFloat,
    PositiveInt,
    SecretStr,
    field_serializer,
    field_validator,
    model_serializer
    )

from pydantic_settings import BaseSettings


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ProjectSettings(BaseSettings):
    target_repo: DirectoryPath = "" 
    hierarchy_name: str = ".project_doc_record"
    markdown_docs_name: str = "markdown_docs"
    ignore_list: list[str] = []
    language: str = "English"
    max_thread_count: PositiveInt = 4
    max_document_tokens: PositiveInt = 1024
    log_level: LogLevel = LogLevel.INFO


    @model_serializer
    def serialize_ignore_list(self, ignore_list: list[str] = []):
        if ignore_list == [""]:
            self.ignore_list = []  # If the ignore_list is empty, set it to an empty list
            return [] 
        return ignore_list
    
    @field_validator("language")
    @classmethod
    def validate_language_code(cls, v: str) -> str:
        try:
            language_name = Language.match(v).name
            return language_name  # Returning the resolved language name
        except LanguageNotFoundError:
            raise ValueError(
                "Invalid language input. Please enter a valid ISO 639 code or language name."
            )
        
    @field_validator("log_level", mode="before")
    @classmethod
    def set_log_level(cls, v: str) -> LogLevel:
        if isinstance(v, str):
            v = v.upper() 
        if v in LogLevel._value2member_map_:  
            return LogLevel(v)
        raise ValueError(f"Invalid log level: {v}")

    @field_serializer("target_repo")
    def serialize_target_repo(self, target_repo: DirectoryPath):
        return str(target_repo)

class ChatCompletionSettings(BaseSettings):
    model: str = "gpt-3.5-turbo"
    temperature: PositiveFloat = 0.2
    request_timeout: PositiveFloat = 60.0
    base_url: HttpUrl
    openai_api_key: SecretStr = Field(..., exclude=True)

    @field_serializer("base_url")
    def serialize_base_url(self, base_url: HttpUrl):
        return str(base_url)

class Setting(BaseSettings):
    project: ProjectSettings = {}  # type: ignore
    chat_completion: ChatCompletionSettings = {}  # type: ignore


from settings import ChatCompletionSettings, ProjectSettings, Setting

target_repo_path = fr'{os.environ["target_repo_path"]}'
hierarchy_path = f'{os.environ["hierarchy_path"]}'
markdown_docs_path = f'{os.environ["markdown_docs_path"]}'

base_url = f'{os.environ["BASE-URL"]}'
model = f'{os.environ["MODEL"]}'
api_key = f'{os.environ["API-KEY"]}'

ignore_list = []
loglevel: LogLevel = LogLevel.INFO

projectSettings = ProjectSettings(
    target_repo=target_repo_path,
    hierarchy_name=hierarchy_path,
    markdown_docs_name=markdown_docs_path,
    ignore_list=list(ignore_list),
)

chat_completion_settings = ChatCompletionSettings(
    model= model,
    temperature=0.5,
    request_timeout=200,
    base_url=base_url,
    openai_api_key=SecretStr(api_key)
    )

setting = Setting(project=projectSettings, chat_completion=chat_completion_settings)


max_input_tokens_map = {
    "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": 4096,
    # "gpt-4": 8192,
    # "gpt-4-0613" : 8192,
    # "gpt-4-32k" : 32768
}