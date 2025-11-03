#!/bin/bash
source /home/raynor/Escritorio/Proyectos/backend (2)/venv/bin/activate
flask db migrate -m "increase_image_url_length"