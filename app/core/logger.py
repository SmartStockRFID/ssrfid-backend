# app/core/logging_config.py
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # mantém loggers de libs
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "logs/app.log",
            "level": "INFO",
        },
    },
    "loggers": {
        "uvicorn.error": {"level": "INFO", "handlers": ["console", "file"], "propagate": False},
        "uvicorn.access": {"level": "INFO", "handlers": ["console"], "propagate": False},
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
