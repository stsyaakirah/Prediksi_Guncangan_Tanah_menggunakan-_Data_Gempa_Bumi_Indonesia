import asyncio
import sys
from streamlit.web import cli

# Menandalan Bug Python 3.14+ di mana asyncio.get_event_loop() dihapus/strikt
if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Menimpa parameter jalan CLI bawaan Streamlit
    sys.argv = ["streamlit", "run", "src/app.py"]
    
    # Jalankan Streamlit sebagai modul internal
    sys.exit(cli.main())
