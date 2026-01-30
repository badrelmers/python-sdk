@echo off
call addpython

set PYTHONPATH=%~dp0\src;F:\_bin\_binz\_ide\_CudaText\_last64\py\cuda_ai_agents\lsp_modules
@rem python verify_shim.py
python tests\test_golden.py
pause
