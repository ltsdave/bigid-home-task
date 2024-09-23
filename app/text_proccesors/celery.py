from celery import Celery

from app.consts import CELERY_BROKER_URL_NAME, CELERY_RESULT_BACKEND_NAME
from app.utils import get_env_var

celery = Celery(__name__)
celery.conf.broker_url = get_env_var(CELERY_BROKER_URL_NAME)
celery.conf.result_backend = get_env_var(CELERY_RESULT_BACKEND_NAME)
