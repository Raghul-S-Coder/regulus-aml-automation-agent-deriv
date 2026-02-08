"""
Migration: Add transaction_id to alerts and cases tables

This migration adds the transaction_id column to both alerts and cases tables
to link them directly to the transaction that triggered them.

Run this migration if you have an existing database.
For new databases, the models will create the columns automatically.
"""

import sqlite3
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config.settings import settings
from loguru import logger


def run_migration():
    """Add transaction_id columns to alerts and cases tables."""
    db_path = settings.DATABASE_URL.replace("sqlite:///./", "")
    
    logger.info(f"Running migration on database: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if alerts table has transaction_id column
        cursor.execute("PRAGMA table_info(alerts)")
        alerts_columns = [col[1] for col in cursor.fetchall()]
        
        if "transaction_id" not in alerts_columns:
            logger.info("Adding transaction_id column to alerts table...")
            cursor.execute("""
                ALTER TABLE alerts 
                ADD COLUMN transaction_id TEXT 
                REFERENCES transactions(transaction_id)
            """)
            logger.info("✓ Added transaction_id to alerts table")
        else:
            logger.info("✓ alerts.transaction_id already exists")
        
        # Check if cases table has transaction_id column
        cursor.execute("PRAGMA table_info(cases)")
        cases_columns = [col[1] for col in cursor.fetchall()]
        
        if "transaction_id" not in cases_columns:
            logger.info("Adding transaction_id column to cases table...")
            cursor.execute("""
                ALTER TABLE cases 
                ADD COLUMN transaction_id TEXT 
                REFERENCES transactions(transaction_id)
            """)
            logger.info("✓ Added transaction_id to cases table")
        else:
            logger.info("✓ cases.transaction_id already exists")
        
        # Commit changes
        conn.commit()
        logger.info("Migration completed successfully!")
        
        # Optional: Backfill transaction_id for existing records
        logger.info("Checking for records to backfill...")
        
        # For alerts: We can't reliably backfill without additional logic
        # since multiple transactions could be for the same account
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE transaction_id IS NULL")
        null_alerts = cursor.fetchone()[0]
        if null_alerts > 0:
            logger.warning(f"Found {null_alerts} alerts without transaction_id")
            logger.warning("These alerts were created before the migration and cannot be automatically linked")
        
        # For cases: We can try to link via alert if alert has transaction_id
        cursor.execute("""
            UPDATE cases 
            SET transaction_id = (
                SELECT transaction_id 
                FROM alerts 
                WHERE alerts.alert_id = cases.alert_id
            )
            WHERE transaction_id IS NULL 
            AND EXISTS (
                SELECT 1 FROM alerts 
                WHERE alerts.alert_id = cases.alert_id 
                AND alerts.transaction_id IS NOT NULL
            )
        """)
        updated_cases = cursor.rowcount
        if updated_cases > 0:
            logger.info(f"✓ Backfilled transaction_id for {updated_cases} cases")
        
        conn.commit()
        
    except sqlite3.Error as e:
        logger.error(f"Migration failed: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    run_migration()

