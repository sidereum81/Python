
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := VtsCiSmokeTest
VTS_CONFIG_SRC_DIR := vendor/volvocars/hardware/ci/smoketest
include test/vts/tools/build/Android.host_config.mk
