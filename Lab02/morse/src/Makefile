OBJS := main.o morse.o 

morse: $(OBJS)
	$(CC) -o morse $(CFLAGS) $(LDFLAGS) $(OBJS) -l periphery

$(OBJS): %.o : %.c
	$(CC) -c $(CFLAGS) $< -o $@