import logging
from logging.handlers import TimedRotatingFileHandler
from rich.logging import RichHandler
from pathlib import Path

logger = logging.getLogger(__name__)

LOG_DIR = (Path('.').cwd() / 'logs')
LOG_DIR.mkdir(exist_ok=True)

# shell_handler = logging.StreamHandler()
shell_handler = RichHandler(show_path=False)
file_handler = TimedRotatingFileHandler(LOG_DIR / 'logger.log' ,  when='midnight', backupCount=30)
file_handler.suffix = r'%Y-%m-%d.log'

logger.setLevel(logging.DEBUG)

shell_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

fmt_file = '%(levelname)4s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
fmt_shell = '[%(filename)s:%(funcName)s:%(lineno)d] %(message)s'

file_formatter = logging.Formatter(fmt_file)
shell_formatter = logging.Formatter(fmt_shell)

file_handler.setFormatter(file_formatter)
shell_handler.setFormatter(shell_formatter)

logger.addHandler(file_handler)
logger.addHandler(shell_handler)