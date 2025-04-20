"""Test the langchain_community API functionality with proper API key handling"""

import os
import sqlite3
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_types import AgentType

# Load environment variables
load_dotenv()

def get_api_key():
    """Get API key from environment with proper error handling"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "No API key found. Please set the OPENAI_API_KEY environment variable "
            "in your .env file or Streamlit secrets."
        )
    return api_key

def create_test_db():
    """Create a simple test database for demonstration"""
    conn = sqlite3.connect('test_db.sqlite')
    cursor = conn.cursor()
    
    # Create a simple table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_table (
        id INTEGER PRIMARY KEY,
        name TEXT,
        value INTEGER
    )
    ''')
    
    # Insert some test data
    test_data = [
        (1, 'Item A', 100),
        (2, 'Item B', 200),
        (3, 'Item C', 300),
        (4, 'Item D', 400),
        (5, 'Item E', 500)
    ]
    
    cursor.execute('DELETE FROM test_table')  # Clear existing data
    cursor.executemany('INSERT INTO test_table VALUES (?, ?, ?)', test_data)
    
    conn.commit()
    conn.close()
    
    print("Test database created successfully.")
    return 'test_db.sqlite'

def test_sql_database_api():
    """Test the SQLDatabase API from langchain_community"""
    db_path = create_test_db()
    db_uri = f"sqlite:///{db_path}"
    
    # Create SQLDatabase instance
    db = SQLDatabase.from_uri(db_uri)
    
    # Test running a simple query
    result = db.run("SELECT * FROM test_table")
    print("\nTest SQLDatabase API:")
    print("Query result:", result)
    
    # Test getting table info
    table_info = db.get_table_info()
    print("\nTable info:", table_info)
    
    return db

def test_sql_agent():
    """Test the SQL Agent API from langchain_community"""
    try:
        api_key = get_api_key()
        
        # Print masked API key for debugging (only first 4 and last 4 characters)
        if len(api_key) > 8:
            masked_key = f"{api_key[:4]}...{api_key[-4:]}"
            print(f"\nUsing API key: {masked_key}")
        
        db = test_sql_database_api()
        
        # Initialize ChatOpenAI with proper configuration
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=api_key
        )
        
        print("LLM initialized successfully")
        
        # Test simple chat completion
        print("\nTesting simple chat completion...")
        from langchain.schema import HumanMessage
        
        messages = [HumanMessage(content="What is 2+2?")]
        response = llm.invoke(messages)
        print(f"Chat response: {response.content}")
        
        # Test SQL agent
        print("\nTesting SQL Agent with a simple query...")
        agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            agent_type="openai-tools",
            verbose=True
        )
        
        result = agent_executor.invoke({"input": "What are all the items in the test_table?"})
        print("\nSQL Agent result:", result.get("output", "No output found."))
        
    except Exception as e:
        print(f"\nError: {e}")
        return False
    
    return True

def run_all_tests():
    """Run all tests and return a summary of results"""
    print("Testing langchain_community API functionality...")
    print("=" * 50)
    
    # Test SQLDatabase API
    sql_db_success = False
    try:
        test_sql_database_api()
        sql_db_success = True
        print("\n✅ SQLDatabase API test passed")
    except Exception as e:
        print(f"\n❌ SQLDatabase API test failed: {e}")
    
    # Test SQL Agent API (includes chat completion test)
    agent_success = False
    chat_success = False
    try:
        # Modify test_sql_agent to return success flags
        from io import StringIO
        import sys
        
        # Capture stdout to check for success messages
        old_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        test_sql_agent()
        
        # Restore stdout
        sys.stdout = old_stdout
        output = captured_output.getvalue()
        
        # Check for success messages in the output
        chat_success = "Chat response:" in output
        agent_success = "SQL Agent result:" in output
        
        # Print the captured output
        print(output)
        
        if chat_success:
            print("\n✅ Chat Completion test passed")
        else:
            print("\n❌ Chat Completion test failed or was skipped")
            
        if agent_success:
            print("\n✅ SQL Agent test passed")
        else:
            print("\n❌ SQL Agent test failed or was skipped")
            
    except Exception as e:
        print(f"\n❌ SQL Agent test failed: {e}")
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    print(f"SQLDatabase API: {'✅ Passed' if sql_db_success else '❌ Failed'}")
    print(f"Chat Completion: {'✅ Passed' if chat_success else '❌ Not tested or failed'}")
    print(f"SQL Agent: {'✅ Passed' if agent_success else '❌ Not tested or failed'}")
    print("=" * 50)
    
    print("\nAPI testing completed.")
    if sql_db_success and (chat_success or agent_success):
        print("The langchain_community package is installed and working correctly.")
        print("You can now use it in your projects.")
    else:
        print("Some tests failed. Please check the output above for details.")

if __name__ == "__main__":
    run_all_tests()
