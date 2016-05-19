#!/usr/bin/env bash
set -e

flake8 .
import-order nirum ./nirum
