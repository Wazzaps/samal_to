#!/bin/sh

# easy_install3 py3-ortools

pip3 install ortools

rm -rf dist dist.zip; mkdir dist

cp -r "/opt/python3/lib/python3.6/site-packages/"* dist
find -not -name 'dist' -not -name 'Dockerfile' -not -name '__init__.py' -not -name 'package.sh' -mindepth 1 -maxdepth 1 -exec cp -r {} ./dist \;

chmod -R 755 ./dist

cd dist; zip -r ../dist.zip *