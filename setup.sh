# create virtual environment
OS="`uname`"

echo "creating virtual environment..."
case $OS in
    'Darwin')
    python3 -m venv env
    ;;
    'WindowsNT')
    python -m venv env
    ;;
    *)
    python -m venv env
esac
echo "created"

echo "activating the environment..."
case $OS in
    'Darwin')
    source env/bin/activate
    ;;
    'WindowsNT')
    env\Scripts\activate
    ;;
    *)
    source env/bin/activate
esac
echo "activated"
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata data/*.json