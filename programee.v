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
bord.rm.mem[4'h0] <= {4'h2, 4'h0};
bord.rm.mem[4'h1] <= {4'h2, 4'hf};
bord.rm.mem[4'h2] <= {4'he, 4'h0};
bord.rm.mem[4'h3] <= {4'h1, 4'h4};
bord.rm.mem[4'h4] <= {4'he, 4'h4};
bord.rm.mem[4'h5] <= {4'h2, 4'h0};
bord.rm.mem[4'h6] <= {4'he, 4'h3};
bord.rm.mem[4'h7] <= {4'h2, 4'hd};
bord.rm.mem[4'h8] <= {4'he, 4'h4};
bord.rm.mem[4'h9] <= {4'h2, 4'h0};
bord.rm.mem[4'ha] <= {4'he, 4'h3};
bord.rm.mem[4'hb] <= {4'h2, 4'hd};
end
always@(bord.display)
begin
$display("out= %h",bord.display);
end
endmodule