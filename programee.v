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
bord.rm.mem[4'hf] <= 8'h32;
bord.rm.mem[0] <= {4'h2, 4'hf};
bord.rm.mem[0] <= {4'he, 4'h0};
end
always@(bord.display)
begin
$display("out= %h",bord.display);
end
endmodule