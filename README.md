[[images/DIRT_logo.png]]
====
Master: [![Build Status](https://travis-ci.org/gnarph/DIRT.svg?branch=master)](https://travis-ci.org/gnarph/DIRT)

Develop: [![Build Status](https://travis-ci.org/gnarph/DIRT.svg?branch=develop)](https://travis-ci.org/gnarph/DIRT) [![Coverage Status](https://coveralls.io/repos/gnarph/DIRT/badge.png?branch=develop)](https://coveralls.io/r/gnarph/DIRT?branch=develop)

# What is DIRT?
**DIRT** (Dynamic Identification of Reused Text) aims to allow users (primarily academics) to find passages that are shared by pairs of documents within a corpus. It will allow them to view pairs of documents and their common passages, as well as show which documents within a corpus have common passages with one particular document within the same corpus, known as the focus document.

DIRT also aims to be extensible to support other languages, although ancient Chinese will be the focus for the prototype. DIRT should be able to find matches in a UTF-8 encoded corpus in any language, with a language specific module improving the permissiveness of matching.

Install Dependencies
-------------------
Dependencies can be installed with
```bash
pip install --allow-external jianfan --allow-unverified jianfan -r requirements.txt
```

Running Tests
-------------
Tests can be run from the root directory with
```bash
nosetests
```

Coverage can be checked using
```bash
./check_test_coverage.sh
```

Contributing
------------
Python code should follow PEP 8 and have tests before pull requesting or merging to develop.
