"""
Health service for the AI Coder Agent.

This module provides health check functionality for monitoring the
status of the application and its dependencies.
"""

import asyncio
import logging
from typing import Dict, Any

import asyncpg
from redis.asyncio import Redis

from ..config import settings
from .logging import get_logger

logger = get_logger(__name__)


class HealthService:
    """Service for checking the health of the application and its dependencies."""
    
    def __init__(self):
        self.db_pool = None
        self.redis_client = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize the health service with database and Redis connections."""
        if self._initialized:
            return
        
        try:
            # Initialize database connection pool
            self.db_pool = await asyncpg.create_pool(
                settings.DATABASE_URL,
                min_size=1,
                max_size=5,
                command_timeout=5,
            )
            
            # Initialize Redis client
            self.redis_client = Redis.from_url(settings.REDIS_URL)
            
            self._initialized = True
            logger.info("Health service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize health service: {e}")
            raise
    
    async def cleanup(self):
        """Clean up resources used by the health service."""
        if self.db_pool:
            await self.db_pool.close()
        
        if self.redis_client:
            await self.redis_client.close()
        
        self._initialized = False
        logger.info("Health service cleaned up")
    
    async def is_ready(self) -> bool:
        """Check if the application is ready to serve requests."""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Check database connection
            await self.check_database()
            
            # Check Redis connection
            await self.check_redis()
            
            return True
            
        except Exception as e:
            logger.error(f"Readiness check failed: {e}")
            return False
    
    async def check_database(self) -> Dict[str, Any]:
        """Check the health of the database connection."""
        if not self.db_pool:
            await self.initialize()
        
        try:
            async with self.db_pool.acquire() as conn:
                result = await conn.fetchval("SELECT 1")
                
            return {
                "status": "healthy",
                "details": "Database connection successful",
            }
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "details": f"Database connection failed: {str(e)}",
            }
    
    async def check_redis(self) -> Dict[str, Any]:
        """Check the health of the Redis connection."""
        if not self.redis_client:
            await self.initialize()
        
        try:
            await self.redis_client.ping()
            
            return {
                "status": "healthy",
                "details": "Redis connection successful",
            }
            
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {
                "status": "unhealthy",
                "details": f"Redis connection failed: {str(e)}",
            }
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get the overall health status of the application."""
        if not self._initialized:
            await self.initialize()
        
        health_status = {
            "status": "healthy",
            "timestamp": asyncio.get_event_loop().time(),
            "checks": {},
        }
        
        # Check database
        db_status = await self.check_database()
        health_status["checks"]["database"] = db_status
        
        # Check Redis
        redis_status = await self.check_redis()
        health_status["checks"]["redis"] = redis_status
        
        # Determine overall status
        if any(check["status"] != "healthy" for check in health_status["checks"].values()):
            health_status["status"] = "unhealthy"
        
        return health_status