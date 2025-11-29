"""
Main entry point for Contract Analysis Agent
Run this to start the application with observability enabled.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.observability import logger, metrics
from src.agent import analyze_contract_file


def main():
    """Main application entry point."""
    logger.info("🚀 Contract Analysis Agent starting...")
    
    # Verify configuration
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("❌ OPENAI_API_KEY not set in environment")
        sys.exit(1)
    
    logger.info(f"✅ Configuration loaded")
    logger.info(f"   Model: {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}")
    logger.info(f"   Observability: {os.getenv('ENABLE_OBSERVABILITY', 'true')}")
    logger.info(f"   Security: {os.getenv('ENABLE_SECURITY', 'true')}")
    logger.info(f"   Metrics Port: {os.getenv('PROMETHEUS_PORT', '8000')}")
    
    # Example: Analyze a sample contract
    sample_contract = Path(__file__).parent.parent / "sample_contracts" / "nda_standard.pdf"
    
    if sample_contract.exists():
        logger.info(f"\n📄 Analyzing sample contract: {sample_contract.name}")
        
        try:
            result = analyze_contract_file(
                file_path=str(sample_contract),
                user_id="demo_user"
            )
            
            logger.info("\n✅ Analysis complete!")
            logger.info(f"   Contract Type: {result.get('contract_type')}")
            logger.info(f"   Complexity: {result.get('complexity')}")
            logger.info(f"   Key Terms Found: {len(result.get('key_terms', []))}")
            logger.info(f"   Risks Identified: {len(result.get('risks', []))}")
            
            if result.get('pii_detected'):
                logger.warning(f"   ⚠️  PII Detected: {result.get('total_pii_entities', 0)} entities")
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}", exc_info=True)
            sys.exit(1)
    
    else:
        logger.warning(f"⚠️  Sample contract not found. Generate PDFs first:")
        logger.warning(f"   cd sample_contracts && python generate_sample_pdfs.py")
    
    logger.info("\n" + "="*60)
    logger.info("📊 Metrics available at: http://localhost:8000/metrics")
    logger.info("🎯 Agent ready for requests!")
    logger.info("="*60)
    
    # Keep running for metrics server
    try:
        logger.info("\n⌨️  Press Ctrl+C to stop...")
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down...")


if __name__ == "__main__":
    main()
