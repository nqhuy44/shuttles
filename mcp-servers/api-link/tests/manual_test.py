import asyncio
import json
from core.spec_parser import get_openapi_map, get_endpoint_schema
from core.safe_executor import safe_api_execute

async def test_spec_parser():
    print("\n--- Testing OpenAPI Spec Parser ---")
    # Using a public petstore spec as a sample
    petstore_url = "https://petstore.swagger.io/v2/swagger.json"
    
    print("Testing map...")
    api_map = await get_openapi_map(petstore_url)
    print(f"Map sample (first 200 chars): {api_map[:200]}...")
    
    print("\nTesting schema for GET /pet/findByStatus...")
    schema = await get_endpoint_schema(petstore_url, "/pet/findByStatus", "GET")
    print(f"Schema: {schema}")

async def test_safe_executor():
    print("\n--- Testing Safe API Executor ---")
    # Testing with JSONPlaceholder (returns a list of 100 items)
    url = "https://jsonplaceholder.typicode.com/posts"
    
    print(f"Executing GET {url} (expecting truncated list)...")
    result = await safe_api_execute(url, "GET")
    data = json.loads(result)
    print(f"Status: {data.get('status_code')}")
    print(f"Body sample structure: {data.get('body')}")
    
    # Testing with a long text response (Google.com)
    url_html = "https://www.google.com"
    print(f"\nExecuting GET {url_html} (expecting HTML truncation)...")
    result_html = await safe_api_execute(url_html, "GET")
    data_html = json.loads(result_html)
    print(f"HTML Preview: {data_html.get('body')}")

async def main():
    try:
        await test_spec_parser()
        await test_safe_executor()
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
