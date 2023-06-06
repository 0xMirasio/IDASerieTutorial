CC = g++
CFLAGS = -std=c++11

TARGET = main

SRCS = main.cpp

OBJS = $(SRCS:.cpp=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(TARGET)
	strip $(TARGET)

.cpp.o:
	$(CC) $(CFLAGS) -c $< -o $@ -O3
	

clean:
	rm -f $(OBJS) $(TARGET)