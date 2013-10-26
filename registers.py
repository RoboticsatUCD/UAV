
gyro_addr=0x68
accel_addr=0x18
compass_addr=0x1E

accel_ctrl_reg4 = 0x23
accel_ctrl_reg1 = 0x20
accel_x_low = 0x28
accel_x_high = 0x29
accel_y_low = 0x2A
accel_y_high = 0x2B
accel_z_low = 0x2C
accel_z_high = 0x2D

compass_mr_reg = 0x02
compass_x_high = 0x03
compass_x_low = 0x04
compass_y_high = 0x05
compass_y_low = 0x06
compass_z_high = 0x07
compass_z_low = 0x08

gyro_ctrl_reg1 = 0x20
gyro_ctrl_reg2 = 0x21
gyro_ctrl_reg3 = 0x22
gyro_ctrl_reg4 = 0x23
gyro_ctrl_reg5 = 0x24
gyro_status_reg = 0x27
gyro_x_low = 0x28
gyro_x_high = 0x29
gyro_y_low = 0x2A
gyro_y_high = 0x2B
gyro_z_low = 0x2C
gyro_z_high = 0x2D
gyro_fifo_ctrl_reg = 0x2E

gyro_regs=[(gyro_x_low,gyro_x_high),(gyro_y_low,gyro_y_high),(gyro_z_low,gyro_z_high)]
accel_regs=[(accel_x_low,accel_x_high),(accel_y_low,accel_y_high),(accel_z_low,accel_z_high)]
compass_regs=[(compass_x_low,compass_x_high),(compass_y_low,compass_y_high),(compass_z_low,compass_z_high)]
