### Install

- Requirements: Mac & Python 3.8 (preferably in conda environment)
- Run (command line): `git clone https://gitlab.com/Symcies/eye-dashboard`
- Run `pip3 install -r requirements.txt` (in conda environment)
- Test if working with `streamlit run src/app.py`
- if working, add `alias run="cd ~/Documents/eTAO/eye-dashboard; streamlit run src/app.py"`


### Requirements

- If no XCODE: install from App Store
- If no brew: 
  - Run `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
  - Add `export PATH="/usr/local/opt/python/libexec/bin:$PATH"`
- If no python: Run `brew install python`
- If no pip3: (Should be installed with python)