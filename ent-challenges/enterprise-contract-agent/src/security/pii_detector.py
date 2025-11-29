"""
PII Detection and Redaction for Contract Analysis
Uses Presidio Analyzer to detect and redact personally identifiable information.
"""

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PIIDetector:
    """Detects and redacts PII in contract text."""
    
    def __init__(self):
        """Initialize PII detection engines."""
        try:
            self.analyzer = AnalyzerEngine()
            self.anonymizer = AnonymizerEngine()
            logger.info("✅ PII detection engines initialized")
        except Exception as e:
            logger.error(f"Failed to initialize PII detector: {e}")
            raise
    
    def detect_pii(self, text: str, language: str = "en") -> List[Dict[str, Any]]:
        """
        Detect PII entities in text.
        
        Args:
            text: Text to analyze
            language: Language code (default: "en")
            
        Returns:
            List of detected PII entities with metadata
        """
        try:
            # Analyze text for PII
            results = self.analyzer.analyze(
                text=text,
                language=language,
                entities=[
                    "PERSON",
                    "EMAIL_ADDRESS",
                    "PHONE_NUMBER",
                    "US_SSN",
                    "CREDIT_CARD",
                    "US_DRIVER_LICENSE",
                    "US_PASSPORT",
                    "LOCATION",
                    "DATE_TIME",
                    "US_BANK_NUMBER",
                    "IBAN_CODE",
                    "IP_ADDRESS"
                ]
            )
            
            # Convert to dict format
            pii_entities = []
            for result in results:
                entity = {
                    "entity_type": result.entity_type,
                    "start": result.start,
                    "end": result.end,
                    "score": result.score,
                    "text": text[result.start:result.end]
                }
                pii_entities.append(entity)
            
            logger.info(f"Detected {len(pii_entities)} PII entities")
            return pii_entities
            
        except Exception as e:
            logger.error(f"PII detection failed: {e}")
            return []
    
    def redact_pii(self, text: str, language: str = "en") -> tuple[str, List[Dict[str, Any]]]:
        """
        Redact PII from text.
        
        Args:
            text: Text to redact
            language: Language code
            
        Returns:
            Tuple of (redacted_text, detected_entities)
        """
        try:
            # Detect PII
            pii_entities = self.detect_pii(text, language)
            
            if not pii_entities:
                return text, []
            
            # Analyze for anonymization
            analyzer_results = self.analyzer.analyze(
                text=text,
                language=language
            )
            
            # Anonymize the text
            anonymized_result = self.anonymizer.anonymize(
                text=text,
                analyzer_results=analyzer_results
            )
            
            redacted_text = anonymized_result.text
            
            logger.info(f"Redacted {len(pii_entities)} PII entities")
            return redacted_text, pii_entities
            
        except Exception as e:
            logger.error(f"PII redaction failed: {e}")
            return text, []
    
    def mask_pii(self, text: str, mask_char: str = "*", language: str = "en") -> str:
        """
        Mask PII with specified character.
        
        Args:
            text: Text to mask
            mask_char: Character to use for masking
            language: Language code
            
        Returns:
            Masked text
        """
        try:
            analyzer_results = self.analyzer.analyze(text=text, language=language)
            
            if not analyzer_results:
                return text
            
            # Sort by start position (reverse) to maintain positions
            sorted_results = sorted(analyzer_results, key=lambda x: x.start, reverse=True)
            
            masked_text = text
            for result in sorted_results:
                start, end = result.start, result.end
                entity_length = end - start
                masked_text = masked_text[:start] + (mask_char * entity_length) + masked_text[end:]
            
            return masked_text
            
        except Exception as e:
            logger.error(f"PII masking failed: {e}")
            return text
    
    def check_for_sensitive_data(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive check for sensitive data.
        
        Returns:
            Dict with detection summary
        """
        pii_entities = self.detect_pii(text)
        
        # Group by entity type
        entity_counts = {}
        for entity in pii_entities:
            entity_type = entity['entity_type']
            entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
        
        has_high_risk_pii = any(
            entity_type in ["US_SSN", "CREDIT_CARD", "US_BANK_NUMBER", "US_PASSPORT"]
            for entity_type in entity_counts.keys()
        )
        
        return {
            "has_pii": len(pii_entities) > 0,
            "total_entities": len(pii_entities),
            "entity_types": list(entity_counts.keys()),
            "entity_counts": entity_counts,
            "has_high_risk_pii": has_high_risk_pii,
            "entities": pii_entities
        }


# Singleton instance
_pii_detector = None


def get_pii_detector() -> PIIDetector:
    """Get or create PII detector instance."""
    global _pii_detector
    if _pii_detector is None:
        _pii_detector = PIIDetector()
    return _pii_detector
