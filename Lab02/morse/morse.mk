################################################################################
#
# Morse package
#
################################################################################

MORSE_VERSION = 1.0
MORSE_SITE = package/morse/src
MORSE_SITE_METHOD = local
MORSE_DEPENDENCIES = c-periphery
MORSE_LICENSE = MIT
MORSE_LICENSE_FILES = LICENSE

define MORSE_BUILD_CMDS
	$(MAKE) CC="$(TARGET_CC)" CFLAGS="$(TARGET_CFLAGS)" LDFLAGS="$(TARGET_LDFLAGS)" -C $(@D)
endef

define MORSE_INSTALL_TARGET_CMDS 
	$(INSTALL) -D -m 0755 $(@D)/morse $(TARGET_DIR)/usr/bin/morse
endef

$(eval $(generic-package))
