import sys
sys.path.insert(0, '.')

from aircharts.dash_app import app

if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    app.run_server(debug=True)
else:
    app.run_server(debug=False)
