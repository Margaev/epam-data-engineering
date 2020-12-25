rm lambda.zip
#pip install -t ./package psycopg2-binary
pip install -t ./package pytz
wget https://files.pythonhosted.org/packages/f9/f4/ede7c643939c132b0692a737800747ce5ba0e8068af27730dfda936c9bf1/pandas-1.1.5-cp38-cp38-manylinux1_x86_64.whl
unzip -o pandas-1.1.5-cp38-cp38-manylinux1_x86_64.whl -d ./package
wget https://files.pythonhosted.org/packages/77/0b/41e345a4f224aa4328bf8a640eeeea1b2ad0d61517f7d0890f167c2b5deb/numpy-1.19.4-cp38-cp38-manylinux1_x86_64.whl
unzip -o numpy-1.19.4-cp38-cp38-manylinux1_x86_64.whl -d ./package
wget https://files.pythonhosted.org/packages/b5/5a/985969fb49617701ddf10b8c6b3f53a2ffd7feaaf598277a94d62401c4d9/psycopg2_binary-2.8.6-cp38-cp38-manylinux1_x86_64.whl
unzip -o psycopg2_binary-2.8.6-cp38-cp38-manylinux1_x86_64.whl -d ./package
wget https://files.pythonhosted.org/packages/c7/48/0f897eb57bd68f39bb2f54f168cc85288c8cc0b77d1d3afb93c99bfc8f58/pyarrow-2.0.0-cp38-cp38-manylinux1_x86_64.whl
unzip -o pyarrow-2.0.0-cp38-cp38-manylinux1_x86_64.whl -d ./package
rm -r *.whl *.dist-info __pycache__
cp lambda_function.py ./package
cd package && zip -r ../lambda.zip . && cd ..
aws lambda update-function-code --function-name process_data_from_s3 --zip-file fileb://lambda.zip