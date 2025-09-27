"""
Configuration Management Module

Handles secure loading and validation of environment variables with support
for local .env files and cloud deployment with GCP Secret Manager integration.

Author: Peyman Kh
Last Update: 27-09-2025
"""
# Import libraries
import sys
import logging
from enum import Enum
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field, ValidationError, BaseModel

# Define the path at module level to avoid function call in ConfigDict
ENV_FILE_PATH = Path(__file__).parent.parent.parent / '.env'

class LogLevel(str, Enum):
    """Standard logging levels for application logging configuration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class DatabaseConfig(BaseModel):
    """Database connection configuration."""
    uri: SecretStr = Field(..., description="Database connection URI")
    name: str = Field(..., description="Database name")

class AppConfig(BaseModel):
    """Application-specific configuration settings."""
    name: str = Field(..., description="Application identifier")
    version: str = Field(..., description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")

class LoggingConfig(BaseModel):
    """Logging-specific configuration settings."""
    level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    format: str = Field(..., description="Log message format string")

class LLMConfig(BaseModel):
    """LLM service configuration settings."""
    model_name: str = Field(..., description="LLM model identifier")
    api_key: SecretStr = Field(..., description="API key for the LLM service")
    tavily_api_key: SecretStr = Field(..., description="API key for the Tavily API")

    langsmith_api_key: SecretStr = Field(..., description="API key for LangSmith tracing")
    langsmith_project: str = Field(..., description="LangSmith project name")
    langchain_tracing_v2: bool = Field(default=True, description="Enable LangChain v2 tracing")

# Environment type literals for type checking
EnvironmentType = Literal["production", "development", "testing", "staging"]

class SystemConfig(BaseSettings):
    """
    Main application configuration with environment-based loading.

    Supports local development with .env files and cloud deployment
    with environment variables from GCP Secret Manager.

    Read .env.example for more information about Environment Variables
    """
    # Environment setting with default
    environment: str = Field(default="development", description="Deployment environment")

    # Grouped configuration sections
    app: AppConfig
    logging: LoggingConfig
    database: DatabaseConfig
    llm: LLMConfig

    def get_environment(self) -> str:
        """Return a normalized environment name."""
        return self.environment.lower()

    def is_environment(self, env_type: str) -> bool:
        """Check if running in the specified environment type."""
        return self.get_environment() == env_type.lower()

    def is_production(self) -> bool:
        """Check if running in a production environment."""
        return self.is_environment("production")

    def is_development(self) -> bool:
        """Check if running in a development environment."""
        return self.is_environment("development")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter='__'
    )

# Initialize logging with basic configuration
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=DEFAULT_LOG_FORMAT)

# Load and validate configuration on module import
try:
    config = SystemConfig()
    logging.info(f"Configuration loaded for environment: {config.environment}")
except ValidationError as e:
    logging.error(f"Configuration validation failed: {e}")
    sys.exit(1)
except Exception as e:
    logging.error(f"Failed to load configuration: {e}")
    sys.exit(1)

# Public API
__all__ = ['config', 'SystemConfig']
