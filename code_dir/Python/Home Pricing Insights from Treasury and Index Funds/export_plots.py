"""Run the forecasting script and save generated plots to `plots/`.

Usage:
    python export_plots.py

This script sets the `SAVE_PLOTS` environment variable so `forecastingscript.py`
will save figures instead of calling `plt.show()`.
"""
import os
import subprocess
import sys

cwd = os.path.dirname(__file__)
env = os.environ.copy()
env['SAVE_PLOTS'] = '1'

proc = subprocess.run([sys.executable, 'forecastingscript.py'], cwd=cwd, env=env)
if proc.returncode == 0:
    print('Plots exported to plots/ (if any were generated).')
else:
    print('forecastingscript.py exited with code', proc.returncode)
    sys.exit(proc.returncode)
