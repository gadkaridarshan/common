from sys import stdout
import logging


logger = logging.getLogger()
logging.getLogger("uvicorn.error").propagate = False
logging.basicConfig(
    stream=stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

