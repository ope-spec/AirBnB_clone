#!/usr/bin/python3
"""
Package: models
Modules: base_model, user, ...
"""

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
