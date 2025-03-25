"""
Script to run database migrations on Railway.
This can be executed independently or as part of the deployment process.
"""
import os
import logging
import subprocess
import sys
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("migrations")

def run_migrations():
    """Run Alembic migrations to latest version"""
    logger.info("Starting database migrations...")
    
    # Make sure we're connected to the database
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Run the migrations
            result = subprocess.run(
                ["alembic", "upgrade", "head"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Migration output: {result.stdout}")
            logger.info("Database migrations completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Migration failed: {e.stderr}")
            retry_count += 1
            if retry_count < max_retries:
                wait_time = retry_count * 5  # Increasing backoff
                logger.info(f"Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                time.sleep(wait_time)
            else:
                logger.error("Maximum retry attempts reached. Migration failed.")
                return False
        except Exception as e:
            logger.error(f"Unexpected error running migrations: {str(e)}")
            return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1) 