#!/bin/bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✅ نصب کامل شد. حالا با دستور python app.py اجرا کنید."
