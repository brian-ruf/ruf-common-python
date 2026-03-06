from loguru import logger
from typing import List, Dict, Optional
import sys

class DictSink:
    """Custom sink that captures log records as dictionaries."""
    
    def __init__(self):
        self.records: List[Dict] = []
    
    def write(self, message):
        record = message.record
        log_entry = {
            'timestamp': record['time'].isoformat(),
            'level': record['level'].name,
            'message': record['message'],
            'module': record['module'],
            'function': record['function'],
            'line': record['line']
        }
        if record['exception']:
            log_entry['exception'] = {
                'type': record['exception'].type.__name__,
                'value': str(record['exception'].value),
            }
        self.records.append(log_entry)
    
    def get_records(self) -> List[Dict]:
        return self.records.copy()
    
    def clear(self):
        self.records.clear()


class LoggableMixin:
    """Mixin to add flexible logging capabilities to any class."""
    
    def setup_logging(self, log_mode: str = 'console', 
                     log_file: Optional[str] = None, 
                     log_level: str = 'INFO'):
        """
        Setup logging for this instance.
        
        Args:
            log_mode: 'console', 'file', 'dict', or 'both'
            log_file: Path to log file (required if log_mode includes file)
            log_level: Minimum log level
        """
        # Remove any existing handlers for this instance
        if hasattr(self, '_handler_ids'):
            for handler_id in self._handler_ids:
                logger.remove(handler_id)
        
        self._handler_ids = []
        self._dict_sink = None
        
        if log_mode in ('console', 'both'):
            handler_id = logger.add(
                sys.stderr,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
                level=log_level,
                colorize=True
            )
            self._handler_ids.append(handler_id)
        
        if log_mode in ('file', 'both'):
            if not log_file:
                raise ValueError("log_file required when log_mode includes 'file'")
            handler_id = logger.add(
                log_file,
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
                level='DEBUG',
                rotation="10 MB",
                retention="1 week",
                compression="zip"
            )
            self._handler_ids.append(handler_id)
        
        if log_mode == 'dict':
            self._dict_sink = DictSink()
            handler_id = logger.add(self._dict_sink, format="{message}", level='DEBUG')
            self._handler_ids.append(handler_id)
    
    def get_logs(self) -> List[Dict]:
        """Get captured log records (only works in 'dict' mode)."""
        if hasattr(self, '_dict_sink') and self._dict_sink:
            return self._dict_sink.get_records()
        return []
    
    def clear_logs(self):
        """Clear captured log records."""
        if hasattr(self, '_dict_sink') and self._dict_sink:
            self._dict_sink.clear()
    
    def cleanup_logging(self):
        """Remove all handlers added by this instance."""
        if hasattr(self, '_handler_ids'):
            for handler_id in self._handler_ids:
                logger.remove(handler_id)
