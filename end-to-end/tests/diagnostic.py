"""
Diagnostic script to test imports step by step.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("🔍 Diagnostic Import Test")
print("="*50)

try:
    print("1. Testing basic imports...")
    import langchain
    # Try different import paths for create_retriever_tool
    try:
        from langchain.tools import create_retriever_tool
        print("✓ Found create_retriever_tool in langchain.tools")
    except ImportError:
        try:
            from langchain.tools.retriever import create_retriever_tool
            print("✓ Found create_retriever_tool in langchain.tools.retriever")
        except ImportError:
            try:
                from langchain_community.tools import create_retriever_tool
                print("✓ Found create_retriever_tool in langchain_community.tools")
            except ImportError:
                try:
                    from langchain.agents.agent_toolkits import create_retriever_tool
                    print("✓ Found create_retriever_tool in langchain.agents.agent_toolkits")
                except ImportError:
                    print("❌ Could not find create_retriever_tool anywhere")
                    raise ImportError("create_retriever_tool not found in any known location")
    print("✓ LangChain imports successful")
except Exception as e:
    print(f"❌ LangChain import failed: {e}")
    sys.exit(1)

try:
    print("2. Testing .env loading...")
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ .env loading successful")
except Exception as e:
    print(f"❌ .env loading failed: {e}")

try:
    print("3. Testing config import...")
    from agentic_rag.config import Config
    print("✓ Config import successful")
except Exception as e:
    print(f"❌ Config import failed: {e}")
    sys.exit(1)

try:
    print("4. Testing config initialization...")
    config = Config()
    print("✓ Config initialization successful")
except Exception as e:
    print(f"❌ Config initialization failed: {e}")
    sys.exit(1)

try:
    print("5. Testing AgenticRAG import...")
    from agentic_rag import AgenticRAG
    print("✓ AgenticRAG import successful")
except Exception as e:
    print(f"❌ AgenticRAG import failed: {e}")
    sys.exit(1)

print("\n🎉 All imports successful! The package should work now.")