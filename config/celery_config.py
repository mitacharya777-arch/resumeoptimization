"""
Celery Configuration - Production Queue System
Handles async processing of optimizations for scalability.
"""

import os
from celery import Celery
from kombu import Queue

# Redis connection URL
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
REDIS_BACKEND_URL = os.getenv('REDIS_BACKEND_URL', 'redis://localhost:6379/0')

# Create Celery app
celery_app = Celery(
    'resume_optimizer',
    broker=REDIS_URL,
    backend=REDIS_BACKEND_URL
)

# Celery configuration
celery_app.conf.update(
    # Serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Task execution
    task_track_started=True,
    task_time_limit=300,  # 5 minutes per task
    task_soft_time_limit=270,  # 4.5 minutes soft limit
    worker_prefetch_multiplier=1,  # Fair task distribution
    worker_max_tasks_per_child=50,  # Prevent memory leaks
    
    # Retry configuration
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Queue configuration
    task_default_queue='optimizations',
    task_default_exchange='optimizations',
    task_default_routing_key='optimizations',
    task_queues=(
        Queue('optimizations', routing_key='optimizations'),
        Queue('high_priority', routing_key='high_priority'),
        Queue('low_priority', routing_key='low_priority'),
    ),
    
    # Result backend
    result_expires=3600,  # Results expire after 1 hour
    result_backend_transport_options={
        'master_name': 'mymaster',
        'visibility_timeout': 3600,
    },
    
    # Worker configuration
    worker_pool='prefork',
    worker_concurrency=10,  # Number of concurrent workers
    worker_max_memory_per_child=200000,  # 200MB per worker
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Beat schedule (for periodic tasks)
    beat_schedule={
        'cleanup-old-results': {
            'task': 'services.optimization_tasks.cleanup_old_results',
            'schedule': 3600.0,  # Every hour
        },
    },
)

# Import tasks to register them (only if Celery is available)
try:
    from services import optimization_tasks
except ImportError:
    pass

