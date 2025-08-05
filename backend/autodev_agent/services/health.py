"""
Health service for AI Coder Agent.

This module provides health monitoring functionality including:
- Database connectivity checks
- External service health checks
- Resource monitoring
- Readiness and liveness probes
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

import aiohttp
import psycopg2
from psycopg2.extras import RealDictCursor

from ..config import settings

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


@dataclass
class HealthCheck:
    """Health check result."""
    name: str
    status: HealthStatus
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class HealthService:
    """Health monitoring service."""
    
    def __init__(self):
        self.checks: List[HealthCheck] = []
        self.last_check_time: float = 0
        self.check_interval: float = 30  # seconds
    
    async def is_ready(self) -> bool:
        """Check if the application is ready to serve requests."""
        try:
            # Perform all health checks
            await self._perform_health_checks()
            
            # Check if all critical services are healthy
            critical_checks = [
                check for check in self.checks
                if check.name in ["database", "api_key", "file_system"]
            ]
            
            return all(check.status == HealthStatus.HEALTHY for check in critical_checks)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        await self._perform_health_checks()
        
        # Determine overall status
        if all(check.status == HealthStatus.HEALTHY for check in self.checks):
            overall_status = HealthStatus.HEALTHY
        elif any(check.status == HealthStatus.UNHEALTHY for check in self.checks):
            overall_status = HealthStatus.UNHEALTHY
        else:
            overall_status = HealthStatus.DEGRADED
        
        return {
            "status": overall_status.value,
            "timestamp": time.time(),
            "checks": [
                {
                    "name": check.name,
                    "status": check.status.value,
                    "message": check.message,
                    "details": check.details,
                    "timestamp": check.timestamp,
                }
                for check in self.checks
            ]
        }
    
    async def _perform_health_checks(self):
        """Perform all health checks."""
        current_time = time.time()
        
        # Skip if checks were performed recently
        if current_time - self.last_check_time < self.check_interval:
            return
        
        self.checks.clear()
        
        # Database health check
        await self._check_database()
        
        # API key health check
        await self._check_api_key()
        
        # File system health check
        await self._check_file_system()
        
        # External services health check
        await self._check_external_services()
        
        # Resource usage health check
        await self._check_resources()
        
        self.last_check_time = current_time
    
    async def _check_database(self):
        """Check database connectivity."""
        try:
            # Parse database URL
            import urllib.parse
            parsed = urllib.parse.urlparse(settings.DATABASE_URL)
            
            # Test connection
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                database=parsed.path[1:],
                user=parsed.username,
                password=parsed.password,
                cursor_factory=RealDictCursor
            )
            
            # Test query
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
            
            conn.close()
            
            self.checks.append(HealthCheck(
                name="database",
                status=HealthStatus.HEALTHY,
                message="Database connection successful",
                details={"query_result": result}
            ))
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            self.checks.append(HealthCheck(
                name="database",
                status=HealthStatus.UNHEALTHY,
                message=f"Database connection failed: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def _check_api_key(self):
        """Check API key configuration."""
        try:
            api_key = settings.OPENROUTER_API_KEY.get_secret_value()
            
            if not api_key or api_key == "your_openrouter_api_key_here":
                self.checks.append(HealthCheck(
                    name="api_key",
                    status=HealthStatus.UNHEALTHY,
                    message="OpenRouter API key not configured",
                    details={"error": "API key not set"}
                ))
            else:
                self.checks.append(HealthCheck(
                    name="api_key",
                    status=HealthStatus.HEALTHY,
                    message="API key configured",
                    details={"configured": True}
                ))
                
        except Exception as e:
            logger.error(f"API key health check failed: {e}")
            self.checks.append(HealthCheck(
                name="api_key",
                status=HealthStatus.UNHEALTHY,
                message=f"API key check failed: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def _check_file_system(self):
        """Check file system accessibility."""
        try:
            # Check if required directories exist and are writable
            directories = [
                settings.logs_path,
                settings.memory_path,
                settings.summaries_path,
                settings.artifacts_path,
                settings.temp_path,
            ]
            
            accessible_dirs = []
            for directory in directories:
                if directory.exists() and os.access(directory, os.W_OK):
                    accessible_dirs.append(str(directory))
                else:
                    directory.mkdir(parents=True, exist_ok=True)
                    accessible_dirs.append(str(directory))
            
            self.checks.append(HealthCheck(
                name="file_system",
                status=HealthStatus.HEALTHY,
                message="File system accessible",
                details={"accessible_directories": accessible_dirs}
            ))
            
        except Exception as e:
            logger.error(f"File system health check failed: {e}")
            self.checks.append(HealthCheck(
                name="file_system",
                status=HealthStatus.UNHEALTHY,
                message=f"File system check failed: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def _check_external_services(self):
        """Check external service connectivity."""
        try:
            async with aiohttp.ClientSession() as session:
                # Check OpenRouter API
                try:
                    async with session.get(
                        f"{settings.OPENROUTER_BASE_URL}/models",
                        timeout=aiohttp.ClientTimeout(total=5)
                    ) as response:
                        if response.status == 200:
                            self.checks.append(HealthCheck(
                                name="openrouter_api",
                                status=HealthStatus.HEALTHY,
                                message="OpenRouter API accessible",
                                details={"status_code": response.status}
                            ))
                        else:
                            self.checks.append(HealthCheck(
                                name="openrouter_api",
                                status=HealthStatus.DEGRADED,
                                message=f"OpenRouter API returned status {response.status}",
                                details={"status_code": response.status}
                            ))
                except Exception as e:
                    self.checks.append(HealthCheck(
                        name="openrouter_api",
                        status=HealthStatus.UNHEALTHY,
                        message=f"OpenRouter API check failed: {str(e)}",
                        details={"error": str(e)}
                    ))
                    
        except Exception as e:
            logger.error(f"External services health check failed: {e}")
            self.checks.append(HealthCheck(
                name="external_services",
                status=HealthStatus.UNHEALTHY,
                message=f"External services check failed: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def _check_resources(self):
        """Check system resource usage."""
        try:
            import psutil
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Determine status based on thresholds
            if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
                status = HealthStatus.DEGRADED
                message = "High resource usage detected"
            else:
                status = HealthStatus.HEALTHY
                message = "Resource usage normal"
            
            self.checks.append(HealthCheck(
                name="resources",
                status=status,
                message=message,
                details={
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "disk_percent": disk.percent,
                    "memory_available": memory.available,
                    "disk_free": disk.free
                }
            ))
            
        except ImportError:
            # psutil not available
            self.checks.append(HealthCheck(
                name="resources",
                status=HealthStatus.DEGRADED,
                message="Resource monitoring not available (psutil not installed)",
                details={"error": "psutil not available"}
            ))
        except Exception as e:
            logger.error(f"Resource health check failed: {e}")
            self.checks.append(HealthCheck(
                name="resources",
                status=HealthStatus.UNHEALTHY,
                message=f"Resource check failed: {str(e)}",
                details={"error": str(e)}
            ))
    
    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up health service")
        # No specific cleanup needed for now