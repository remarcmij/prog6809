        ORG     2a40h           Multiply by MPY
START   CLRA                    Set PROD to 0
        STA     PROD
        LDA     MPY             Set CNT equal to MPY
        STA     CNT               and do loop MPY times
LOOP    LDA     CNT             Done if CNT = 0
        BEQ     OUT
        ADDA    #-1             Else decrement CNT
        STA     CNT
        LDA     PROD            Add MCND to PROD
        ADDA    MCND
        STA     PROD
        BRA     LOOP            Repeat the loop again.
OUT     LDA     PROD            Put PROD in A when done  
        JMP     1000H           Return to operating system
        ORG     2C00H
PROD    RMB     1               Storage for PROD
CNT     RMB     1               Storage for CNT
MPY     FCB     5               Multiplier value
MCND    FCB     23              Multiplicand value
        END     START
