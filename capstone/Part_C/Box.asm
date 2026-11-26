// Box.asm
// Capstone Project: Make the Computer Draw a Box
// Roll Number: 2501730430 (K = 30)
//
// Box Parameters for K = 30:
// - Start Row: 30
// - Height: 20 rows (rows 30 to 49)
// - Width: 16 * ((30 % 4) + 1) = 16 * 3 = 48 pixels (3 words per row from left edge)
// - Start Address: SCREEN + (32 * 30) = 16384 + 960 = 17344
//
// Logic:
// - Continuously reads keyboard register (KBD, address 24576)
// - If key is pressed (KBD != 0): color = -1 (black)
// - If no key is pressed (KBD == 0): color = 0 (white)
// - Fills 3 consecutive 16-bit words across 20 rows starting at address 17344

(MAIN_LOOP)
    // Read keyboard state
    @KBD
    D=M
    @KEY_PRESSED
    D;JNE

    // No key pressed -> set color to white (0)
    @color
    M=0
    @DRAW_INIT
    0;JMP

(KEY_PRESSED)
    // Key pressed -> set color to black (-1)
    @color
    M=-1

(DRAW_INIT)
    // Starting screen memory address: 17344 (Row 30)
    @17344
    D=A
    @addr
    M=D

    // Total rows to draw: 20
    @20
    D=A
    @rows_left
    M=D

(ROW_LOOP)
    // Exit row loop if all 20 rows are completed
    @rows_left
    D=M
    @MAIN_LOOP
    D;JEQ

    // Draw Word 0 (Column pixels 0-15)
    @color
    D=M
    @addr
    A=M
    M=D

    // Draw Word 1 (Column pixels 16-31)
    @addr
    A=M+1
    M=D

    // Draw Word 2 (Column pixels 32-47)
    @addr
    D=M
    @2
    D=D+A
    @target
    M=D
    @color
    D=M
    @target
    A=M
    M=D

    // Advance address to next screen row (32 words per row)
    @32
    D=A
    @addr
    M=D+M

    // Decrement rows counter
    @rows_left
    M=M-1

    @ROW_LOOP
    0;JMP
