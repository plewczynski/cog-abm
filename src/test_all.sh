#!/bin/bash

nosetests -v --cover-erase --with-coverage --cover-package=cog_abm,steels $@
# -s will print stdout

