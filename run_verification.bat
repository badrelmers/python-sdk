@echo off
call addpython

set "PYTHONPATH=%~dp0\src;F:\_bin\_binz\_ide\_CudaText\_last64\py\cuda_ai_agents\lsp_modules;%~dp0"
@rem python verify_shim.py
@rem python tests\test_golden.py
@rem pytest -rs tests\test_golden.py

set "ACP_QWEN_CODE_CLI_BIN=F:\_bin\_binz\_ide\__AI\__CLI\__ACP\_npm"
python test_qwen_cli_agent.py

pause
