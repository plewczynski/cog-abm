#!/bin/bash

nosetests -v --cover-erase --with-coverage --cover-package=cog_abm,steels,kurdej $@
# -s will print stdout

