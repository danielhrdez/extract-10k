import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

from .core.document_processor import DocumentProcessor
from .utils.output_handler import OutputHandler

__version__ = "0.1.0"
