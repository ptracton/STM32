DIRS = leds


all:
	$(foreach c,$(DIRS),$(MAKE) -C $(c) && ) true

clean:
	rm -f *~
	$(foreach c,$(DIRS),$(MAKE) -C $(c) clean && ) true
