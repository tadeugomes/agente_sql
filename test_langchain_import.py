try:
    import langchain_community
    print("Success: langchain_community package is installed and can be imported.")
    print(f"Version: {langchain_community.__version__}")
except ImportError as e:
    print(f"Error: {e}")
