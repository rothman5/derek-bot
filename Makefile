TARGET = start_paul

all: $(TARGET)
	
$(TARGET): 
	python3 main.py

clean:
	rm -rf data/stores.db debug.log
