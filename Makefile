# Copyright (C) 2013, 2014 Yu-Jie Lin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

PACKAGE=1to001
SCRIPT=1to001

PY3_CMD=python3
INSTALL_TEST_DIR=/tmp/$(PACKAGE)_install_test
# if version or naming isn't matched to environment, for example, Python 3.2,
# run the following to override:
#   make VENV_PY3_CMD=virtualenv-python3.2 install_test
VENV_PY3_CMD=virtualenv-python3.3

BUILD_CMD=./setup.py sdist --formats gztar,zip bdist_wheel bdist_wininst --plat-name win32

# ============================================================================

build:
	$(BUILD_CMD)

upload:
	$(BUILD_CMD) upload

# ============================================================================

test: test_isort test_pep8 test_pyflakes test_test install_test

test_%:
	@echo '========================================================================================='
	$(PY3_CMD) setup.py $(subst test_,,$@)

install_test: $(VENV_PY3_CMD)

$(VENV_PY3_CMD):
	@echo '========================================================================================='
	rm -rf $(INSTALL_TEST_DIR)
	$@ $(INSTALL_TEST_DIR)
	./setup.py sdist --dist-dir $(INSTALL_TEST_DIR)
	$(INSTALL_TEST_DIR)/bin/pip install $(INSTALL_TEST_DIR)/*.tar.gz
	. $(INSTALL_TEST_DIR)/bin/activate ; type $(SCRIPT)
	$(INSTALL_TEST_DIR)/bin/$(SCRIPT) --version

# ============================================================================

clean:
	rm -rf *.pyc build dist __pycache__

# ============================================================================

.PHONY: build upload doc install_test $(VENV_PY3_CMD) clean
