"""
Monitoring and Metrics - Production System
Tracks performance, errors, and system health.
"""

import time
import logging
from functools import wraps
from typing import Dict, Optional
from datetime import datetime
from prometheus_client import Counter, Histogram, Gauge
import os

# Prometheus metrics
optimization_requests = Counter(
    'optimization_requests_total',
    'Total number of optimization requests',
    ['status', 'type']
)

optimization_duration = Histogram(
    'optimization_duration_seconds',
    'Time spent processing optimizations',
    ['type']
)

optimization_queue_size = Gauge(
    'optimization_queue_size',
    'Current size of optimization queue'
)

cache_hits = Counter(
    'cache_hits_total',
    'Total number of cache hits'
)

cache_misses = Counter(
    'cache_misses_total',
    'Total number of cache misses'
)

api_errors = Counter(
    'api_errors_total',
    'Total number of API errors',
    ['error_type']
)


class PerformanceMonitor:
    """Monitor system performance and track metrics."""
    
    def __init__(self):
        self.metrics = {
            'total_optimizations': 0,
            'successful_optimizations': 0,
            'failed_optimizations': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'average_processing_time': 0.0,
            'total_processing_time': 0.0,
            'errors': []
        }
    
    def record_optimization(self, success: bool, processing_time: float, cached: bool = False):
        """Record an optimization attempt."""
        self.metrics['total_optimizations'] += 1
        if success:
            self.metrics['successful_optimizations'] += 1
            optimization_requests.labels(status='success', type='optimization').inc()
        else:
            self.metrics['failed_optimizations'] += 1
            optimization_requests.labels(status='failed', type='optimization').inc()
        
        if cached:
            self.metrics['cache_hits'] += 1
            cache_hits.inc()
        else:
            self.metrics['cache_misses'] += 1
            cache_misses.inc()
        
        # Update average processing time
        self.metrics['total_processing_time'] += processing_time
        total = self.metrics['total_optimizations']
        self.metrics['average_processing_time'] = (
            self.metrics['total_processing_time'] / total
        )
        
        optimization_duration.labels(type='optimization').observe(processing_time)
    
    def record_error(self, error_type: str, error_message: str):
        """Record an error."""
        self.metrics['errors'].append({
            'type': error_type,
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        })
        # Keep only last 100 errors
        if len(self.metrics['errors']) > 100:
            self.metrics['errors'] = self.metrics['errors'][-100:]
        
        api_errors.labels(error_type=error_type).inc()
    
    def get_stats(self) -> Dict:
        """Get current statistics."""
        return {
            **self.metrics,
            'success_rate': (
                self.metrics['successful_optimizations'] / 
                max(self.metrics['total_optimizations'], 1) * 100
            ),
            'cache_hit_rate': (
                self.metrics['cache_hits'] / 
                max(self.metrics['cache_hits'] + self.metrics['cache_misses'], 1) * 100
            )
        }
    
    def reset(self):
        """Reset all metrics."""
        self.metrics = {
            'total_optimizations': 0,
            'successful_optimizations': 0,
            'failed_optimizations': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'average_processing_time': 0.0,
            'total_processing_time': 0.0,
            'errors': []
        }


# Global monitor instance
performance_monitor = PerformanceMonitor()


def monitor_performance(func):
    """Decorator to monitor function performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        success = False
        try:
            result = func(*args, **kwargs)
            success = True
            return result
        except Exception as e:
            performance_monitor.record_error(
                error_type=type(e).__name__,
                error_message=str(e)
            )
            raise
        finally:
            processing_time = time.time() - start_time
            performance_monitor.record_optimization(
                success=success,
                processing_time=processing_time
            )
    return wrapper


# Configure logging
def setup_logging():
    """Setup structured logging."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_format = os.getenv(
        'LOG_FORMAT',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            # Add file handler in production
            # logging.FileHandler('app.log')
        ]
    )
    
    # Set specific loggers
    logging.getLogger('celery').setLevel(logging.WARNING)
    logging.getLogger('redis').setLevel(logging.WARNING)

