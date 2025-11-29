"""
Audit Trail Engine for Contract Analysis Agent
Provides immutable, tamper-evident audit logging with hash chains.
"""

import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class AuditRecord:
    """Single audit record with hash chain."""
    timestamp: str
    request_id: str
    user_id: str
    action: str
    details: Dict[str, Any]
    status: str
    previous_hash: str
    record_hash: str


class AuditTrail:
    """
    Append-only audit log with hash chain for tamper detection.
    
    Features:
    - Immutable (append-only)
    - Searchable (JSON format)
    - Tamper-evident (SHA-256 hash chains)
    - Context-rich (who, what, when, why)
    """
    
    def __init__(self):
        """Initialize audit trail with genesis hash."""
        self.records: List[AuditRecord] = []
        self.last_hash = "0" * 64  # Genesis hash
        
    def add_record(
        self,
        action: str,
        request_id: str,
        user_id: str,
        details: Dict[str, Any],
        status: str = "success"
    ) -> AuditRecord:
        """
        Add audit record with hash chain.
        
        Args:
            action: Action performed (e.g., "contract.upload", "analysis.generate")
            request_id: Request identifier
            user_id: User who performed the action
            details: Additional context
            status: Status of the action (success, error, pending)
            
        Returns:
            Created AuditRecord
        """
        timestamp = datetime.utcnow().isoformat()
        
        # Build payload for hashing
        payload = {
            "timestamp": timestamp,
            "request_id": request_id,
            "user_id": user_id,
            "action": action,
            "details": details,
            "status": status,
            "previous_hash": self.last_hash
        }
        
        # Calculate hash
        record_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()
        
        payload["record_hash"] = record_hash
        
        # Create and store record
        record = AuditRecord(**payload)
        self.records.append(record)
        self.last_hash = record_hash
        
        logger.info(
            "Audit record appended",
            extra={
                "action": action,
                "request_id": request_id,
                "status": status,
                "hash": record_hash
            }
        )
        
        return record
    
    def verify_chain(self) -> tuple[bool, Optional[str]]:
        """
        Verify integrity of hash chain.
        
        Returns:
            (is_valid, error_message)
        """
        if not self.records:
            return True, None
        
        expected_hash = "0" * 64
        
        for i, record in enumerate(self.records):
            # Check previous hash matches
            if record.previous_hash != expected_hash:
                return False, f"Hash chain broken at record {i}: {record.action}"
            
            # Recalculate hash
            payload = {
                "timestamp": record.timestamp,
                "request_id": record.request_id,
                "user_id": record.user_id,
                "action": record.action,
                "details": record.details,
                "status": record.status,
                "previous_hash": record.previous_hash
            }
            
            calculated_hash = hashlib.sha256(
                json.dumps(payload, sort_keys=True).encode()
            ).hexdigest()
            
            if calculated_hash != record.record_hash:
                return False, f"Hash mismatch at record {i}: {record.action}"
            
            expected_hash = record.record_hash
        
        return True, None
    
    def get_records_by_request(self, request_id: str) -> List[AuditRecord]:
        """Get all records for a specific request."""
        return [r for r in self.records if r.request_id == request_id]
    
    def get_records_by_user(self, user_id: str) -> List[AuditRecord]:
        """Get all records for a specific user."""
        return [r for r in self.records if r.user_id == user_id]
    
    def get_records_by_action(self, action: str) -> List[AuditRecord]:
        """Get all records for a specific action type."""
        return [r for r in self.records if r.action == action]
    
    def export_json(self) -> str:
        """Export all records as JSON string."""
        return json.dumps([asdict(r) for r in self.records], indent=2)
    
    def export_records(self) -> List[Dict[str, Any]]:
        """Export all records as list of dictionaries."""
        return [asdict(r) for r in self.records]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get audit trail statistics."""
        if not self.records:
            return {
                "total_records": 0,
                "actions": {},
                "users": {},
                "status": {}
            }
        
        actions = {}
        users = {}
        statuses = {}
        
        for record in self.records:
            actions[record.action] = actions.get(record.action, 0) + 1
            users[record.user_id] = users.get(record.user_id, 0) + 1
            statuses[record.status] = statuses.get(record.status, 0) + 1
        
        return {
            "total_records": len(self.records),
            "actions": actions,
            "users": users,
            "status": statuses,
            "last_hash": self.last_hash,
            "first_record": self.records[0].timestamp if self.records else None,
            "last_record": self.records[-1].timestamp if self.records else None
        }


# Singleton instance
_audit_trail = None


def get_audit_trail() -> AuditTrail:
    """Get or create audit trail instance."""
    global _audit_trail
    if _audit_trail is None:
        _audit_trail = AuditTrail()
    return _audit_trail
