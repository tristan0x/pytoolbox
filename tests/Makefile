TESTS_SUITES = lnm_fortran lnm_swig lnm_boostpython

# If variable NO_TEST_<NAME> is defined, do not add <name> in
# variable SUBDIRS
define REGISTER_test
ifndef NO_TEST_$(1)
SUBDIRS += $(shell echo $(1) | tr [:upper:] [:lower:])
endif
endef

# Call function REGISTER_test on each tests-suite.
$(foreach subdir, $(shell echo $(TESTS_SUITES) | tr [:lower:] [:upper:]), \
	  $(eval $(call REGISTER_test,$(subdir))))

all clean distclean test:
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;)
