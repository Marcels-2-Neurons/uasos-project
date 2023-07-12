start /d "C:\Program Files (x86)\Gazepoint\Gazepoint\bin64\" /b Gazepoint.exe
timeout 5 > NUL
call conda activate gp3lsl
call python gp3-to-lsl.py