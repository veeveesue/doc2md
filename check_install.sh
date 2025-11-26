#!/bin/bash

# Installation check script

echo "=============================================="
echo "  DOCX to Markdown Converter"
echo "  Installation Check"
echo "=============================================="
echo ""

ALL_OK=true

# Check Python
echo -n "Checking Python 3... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✓ $PYTHON_VERSION"
else
    echo "✗ NOT FOUND"
    ALL_OK=false
fi

# Check python-docx
echo -n "Checking python-docx... "
python3 -c "import docx" 2>/dev/null
if [ $? -eq 0 ]; then
    DOCX_VERSION=$(python3 -c "import docx; print(docx.__version__)" 2>/dev/null)
    echo "✓ version $DOCX_VERSION"
else
    echo "✗ NOT INSTALLED"
    echo "  Install with: pip3 install python-docx"
    ALL_OK=false
fi

# Check md_trans module
echo -n "Checking md_trans module... "
cd "$(dirname "$0")"
python3 -c "
import sys
sys.path.insert(0, '../anylisppt')
from md_trans import DocxToMarkdown
" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ FOUND"
else
    echo "✗ NOT FOUND"
    echo "  Make sure md_trans.py is in /Users/vee/project/anylisppt/"
    ALL_OK=false
fi

# Check LibreOffice (optional)
echo -n "Checking LibreOffice (optional)... "
if command -v libreoffice &> /dev/null; then
    echo "✓ INSTALLED"
elif [ -f "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]; then
    echo "✓ INSTALLED"
else
    echo "⚠️  NOT INSTALLED (needed for .doc conversion)"
fi

echo ""
echo "=============================================="

if [ "$ALL_OK" = true ]; then
    echo "✓ All required components are installed!"
    echo ""
    echo "Next steps:"
    echo "  1. Load the extension in Chrome (chrome://extensions/)"
    echo "  2. Run: ./start_server.sh"
    echo "  3. Start converting!"
else
    echo "✗ Some required components are missing."
    echo "Please install the missing components above."
fi

echo "=============================================="
