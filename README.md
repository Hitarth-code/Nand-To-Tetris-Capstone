# Nand to Tetris - Capstone Project: Make the Computer Draw a Box
**Course:** Nand to Tetris – I (ETCCNT301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student:** Hitarth Srivastava  
**Roll Number:** 2501730430  
**Personal Number (K):** 30  

---

## Project Overview

This capstone project implements an end-to-end computer system across three main phases:
1. **Part A - Computer Hardware (HDL):** Assembling the Hack computer architecture (`CPU.hdl`, `Memory.hdl`, `Computer.hdl`) and passing all official test scripts.
2. **Part B - Custom Python Assembler (`assembler.py`):** Translating Hack assembly (`.asm`) into binary machine code (`.hack`) with the required $K \pmod 3 = 0$ feature (saving all labels and variables with memory addresses to `symbols.txt`).
3. **Part C - Interactive Box Program (`Box.asm`):** A Hack assembly graphics routine that detects keyboard presses and renders a solid black box on screen while pressed, clearing it when released.

---

## Specifications for K = 30

- **Personal Number $K$:** 30 (from roll number ending in `30`)
- **Assembler Extra Feature ($K \pmod 3$):**  
  $30 \pmod 3 = 0 \implies$ Export all labels, variables, and predefined symbols to `symbols.txt`.
- **Box Start Row:** Row $K$ = **Row 30**
- **Box Height:** **20 rows** (Rows 30 to 49 inclusive)
- **Box Width:** $16 \times ((K \pmod 4) + 1) = 16 \times ((30 \pmod 4) + 1) = 16 \times 3 =$ **48 pixels** (3 words per row from left edge)
- **Screen Memory Base Address:** $\text{SCREEN} + (32 \times 30) = 16384 + 960 =$ **17344** (`0x43C0`)

---

## Repository Structure

```
├── capstone/
│   ├── Part_A/                     # Part A - Build the Computer (HDL Chips)
│   │   ├── CPU.hdl                 # Hack CPU implementation
│   │   ├── Memory.hdl              # Complete Hack memory space (RAM, Screen, Keyboard)
│   │   ├── Computer.hdl            # Top-level computer chip (CPU + Memory + ROM32K)
│   │   ├── cpu_test_result.png     # Hardware Simulator verification for CPU.hdl
│   │   ├── memory_test_result.png  # Hardware Simulator verification for Memory.hdl
│   │   └── computer_test_result.png# Hardware Simulator verification for Computer.hdl
│   ├── Part_B/                     # Part B - Python Assembler
│   │   ├── assembler.py            # Two-pass Python assembler
│   │   └── symbols.txt             # Symbol table export (Labels, Variables, Predefined)
│   ├── Part_C/                     # Part C - Box Program
│   │   ├── Box.asm                 # Interactive box application in Hack assembly
│   │   ├── Box.hack                # Assembled 16-bit binary machine code
│   │   └── box_emulator_result.png # CPU Emulator verification running Box.hack
│   └── Capstone_Report_Hitarth_2501730430.pdf
├── Capstone_Report_Hitarth_2501730430.pdf
└── README.md
```

---

## How to Run

### 1. Running the Assembler
To assemble `Box.asm` into `Box.hack` and generate `symbols.txt`:
```bash
python capstone/Part_B/assembler.py capstone/Part_C/Box.asm
```

### 2. Simulating the Box in CPU Emulator
1. Open the Nand2Tetris **CPU Emulator** (Desktop or Web IDE: `https://nand2tetris.github.io/web-ide/cpu/`).
2. Load `Box.hack` (or `Box.asm`).
3. Set animation speed to **Fast** and click **Run**.
4. Click on the keyboard input area and hold any key:
   - The solid black rectangle ($48 \times 20$ pixels) appears at Row 30.
   - Releasing the key clears the rectangle back to white.

### 3. Testing HDL Chips in Hardware Simulator
Load `Memory.hdl`, `CPU.hdl`, or `Computer.hdl` with their corresponding `.tst` scripts (`Memory.tst`, `CPU.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, `ComputerRect.tst`) in the Hardware Simulator. All tests pass with comparison ended successfully.
