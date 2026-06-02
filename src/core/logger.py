import logging
import sys
from pathlib import Path

# Setup base directory for log files
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_FILE = BASE_DIR / 'doc_suite.log'

class CustomFormatter(logging.Formatter):
    """Custom formatter providing professional visual output for console logging."""
    
    # ANSI color codes
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    cyan = "\x1b[36;20m"
    
    FORMATS = {
        logging.DEBUG: grey + "[DEBUG] %(message)s" + reset,
        logging.INFO: cyan + "[INFO] %(message)s" + reset,
        logging.WARNING: yellow + "[WARN] %(message)s" + reset,
        logging.ERROR: red + "[ERROR] %(message)s" + reset,
        logging.CRITICAL: bold_red + "[CRITICAL] %(message)s" + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, "[%(levelname)s] %(message)s")
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def get_logger(name: str = "doc-suite") -> logging.Logger:
    """Configures and returns a multi-handler standard logger instance."""
    logger = logging.getLogger(name)
    
    # If logger is already configured, return it to prevent duplicate handler output
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.DEBUG)

    # 1. Console Handler (Standard Output, Info and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    # 2. File Handler (Debug level logs written to doc_suite.log)
    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception:
        # Fallback if log directory/file cannot be created (e.g. read-only permission issue)
        pass

    return logger

# Single default importable logger instance
logger = get_logger()
