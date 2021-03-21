#mkdir -p lambda_layer/python/
#sudo pip3 install -r requirements.txt -t lambda_layer/python/

sudo rm -rf lambda_layer/python/ && mkdir -p lambda_layer/python/
sudo docker run --rm -v $(pwd):/lambda_libs -w /lambda_libs lambci/lambda:build-python3.8 \
    pip install -r requirements.txt --no-deps -t lambda_layer/python/