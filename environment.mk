################################################################################
#
# Set ip your environment paths
#
################################################################################

##
## Prefix of the GCC ARM Cross Compiler
##
PREFIX	= arm-none-eabi

##
## Tools we use for building
##
CC	    = $(PREFIX)-gcc
LD	    = $(PREFIX)-gcc
ASM     = $(PREFIX)-as
OBJCOPY	= $(PREFIX)-objcopy
OBJDUMP	= $(PREFIX)-objdump
AR     	= $(PREFIX)-ar
GDB	    = $(PREFIX)-gdb
FLASH	= $(shell which st-flash)
MKDIR   = mkdir
RM      = rm


##
## This is the path to the root of your STM32F3 Cube Root Directory
##
STM32F3_CUBE_ROOT_DIR=/data/pace/hpc_scratch/vol1/tractp1/src/STM32Cube_FW_F3_V1.2.0/
#STM32F3_CUBE_ROOT_DIR=/home/ptracton/src/software/STM32F3/STM32Cube_FW_F3_V1.2.0/
STM32F4_CUBE_ROOT_DIR=/data/pace/hpc_scratch/vol1/tractp1/src/STM32Cube_FW_F4_V1.8.0/
