`timescale 10ns/1ns
`include "board.v"
module program;
board bord();
reg[7:0] Buss;
reg[3:0] addr;
reg clr,ramoa,ramwa;
assign bord.hlt=0;
initial
begin
bord.clr <= 1;
#4 bord.clr <= 0;
