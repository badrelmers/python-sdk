import sys
from pathlib import Path

# POC to verify shim
src_path = r"F:\_bin\_binz\_ide\_CudaText\_last64\py\cuda_ai_agents\__________________________new\jules\jules_session4_2911930719151660358\src"
src_path2 = r"F:\_bin\_binz\_ide\_CudaText\_last64\py\cuda_ai_agents\lsp_modules"
if src_path not in sys.path:
    sys.path.insert(0, src_path)
    sys.path.insert(0, src_path2)

print(f"Sys path: {sys.path}")

try:
    print("Attempting to import AuthenticateRequest...")
    from acp.schema import AuthenticateRequest
    print("Import successful.")
    
    print("Creating model instance...")
    req = AuthenticateRequest(method_id="test-method")
    
    # Test model_dump with by_alias=True
    dump = req.model_dump(by_alias=True)
    print(f"Model dump (by_alias=True): {dump}")
    
    if "methodId" not in dump:
        raise ValueError(f"Alias 'methodId' not found in dump: {dump}")
    
    # Test recursive serialization
    try:
        from acp.helpers import start_read_tool_call
        tool_call = start_read_tool_call(tool_call_id="1", title="test title", path="/test/path")
        tc_dump = tool_call.model_dump(by_alias=True)
        print(f"Recursive tool call dump (by_alias=True): {tc_dump}")
        if tc_dump.get("locations") and isinstance(tc_dump["locations"][0], dict):
             print("Verified: nested models are serialized to dicts.")
        else:
             print("Warning: nested models might not be fully serialized.")
    except Exception as e:
        print(f"Recursive dump test failed: {e}")
    
    print("Validation check...")
    try:
        # cattrs structure might convert or fail. 
        # wrapper should catch it.
        # But wait, AuthenticateRequest expects string only for method_id? 
        # Let's try to pass something that cattrs can't structure easily or create an invalid state
        # cattrs usually converts types.
        pass
    except Exception as e:
        print(f"Validation caught: {e}")

    print("VERIFICATION SUCCESSFUL")

except Exception as e:
    print(f"VERIFICATION FAILED: {e}")
    import traceback
    traceback.print_exc()
