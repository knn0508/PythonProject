#!/usr/bin/env python3
"""
Test script to debug component initialization
"""

def test_user_manager():
    try:
        print("🔧 Testing UserManager...")
        from models import UserManager
        user_manager = UserManager()
        print("✅ UserManager works!")
        return True
    except Exception as e:
        print(f"❌ UserManager failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_manager():
    try:
        print("🔧 Testing FileManager...")
        from file_manager import FileManager
        file_manager = FileManager()
        print("✅ FileManager works!")
        return True
    except Exception as e:
        print(f"❌ FileManager failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_knowledge_base():
    try:
        print("🔧 Testing KnowledgeBase...")
        from file_manager import FileManager
        from models import EnhancedKnowledgeBase
        
        file_manager = FileManager()
        knowledge_base = EnhancedKnowledgeBase(file_manager)
        print("✅ KnowledgeBase works!")
        return True
    except Exception as e:
        print(f"❌ KnowledgeBase failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_assistant():
    try:
        print("🔧 Testing AI Assistant...")
        from file_manager import FileManager
        from models import EnhancedKnowledgeBase, EnhancedAIAssistant
        
        file_manager = FileManager()
        knowledge_base = EnhancedKnowledgeBase(file_manager)
        ai_assistant = EnhancedAIAssistant(knowledge_base, "test_key")
        print("✅ AI Assistant works!")
        return True
    except Exception as e:
        print(f"❌ AI Assistant failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Component Testing Started")
    print("=" * 40)
    
    tests = [
        ("UserManager", test_user_manager),
        ("FileManager", test_file_manager),
        ("KnowledgeBase", test_knowledge_base),
        ("AI Assistant", test_ai_assistant)
    ]
    
    results = {}
    for name, test_func in tests:
        results[name] = test_func()
        print()
    
    print("=" * 40)
    print("📊 RESULTS:")
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name}: {status}")
    
    print("=" * 40)
