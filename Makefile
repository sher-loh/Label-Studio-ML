clean:
	rm -rf env

# LDFLAGS needed to install uwsgi package
# reference: https://stackoverflow.com/questions/70479867/install-uwsgi-on-m1-monterey-fails-with-python-3-10-0
# numpy install needed to install lap package
# reference: https://github.com/ultralytics/ultralytics/issues/1429#issuecomment-1505327138
install:
	python -m venv env 
	env/bin/pip install --upgrade pip
	env/bin/pip install numpy 
	export LDFLAGS=-L/opt/homebrew/Cellar/gettext/0.21.1/lib 
	env/bin/pip install -r requirements.txt
	env/bin/pip install -r yolov8_tracking/requirements.txt

reset_docker:
	docker compose down --remove-orphans
	docker compose build --no-cache
	docker compose up -d