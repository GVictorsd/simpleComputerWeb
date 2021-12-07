	`include "programcounter.v"
	`include "GPR.v"
	`include "alu.v"
	`include "memaddreg.v"
	`include "ram.v"
	`include "instructionreg.v"
	`include "outputRegister.v"
	`include "controlunit.v"

module board;
	wire[7:0] Bus;
	reg clk,clr;
	wire hlt,marwa,ramwa,ramoa,inregoa,inregwa,awa,aoa,sumout,sub,bwa,outregwa,pcinc,pcoe,pcjmp,flagsin;
	assign Bus=8'hzz;
	
	initial 
	begin
		clk<=0;
	end
	
	always #2 if(~hlt)
		clk = ~clk;
	
	counter pc(Bus[3:0],Bus[3:0],clk,clr,pcoe,pcjmp,pcinc);

	gpr a(Bus,Bus,clk,clr,awa,aoa);

	reg boa;
	gpr b(Bus,Bus,clk,clr,bwa,boa);
	initial boa<=0;

	wire cf,zf;
	alu alunit(Bus,cf,zf,a.store,b.store,clk,sumout,sub,flagsin);

	wire[3:0] addrout;
	memaddreg mar(Bus[3:0],clk,clr,marwa,addrout);

	reg ramcs;
	ram rm(Bus,addrout,clk,ramoa,ramwa,ramcs);
	initial ramcs<=1;

	instreg instructionreg(Bus,clk,clr,inregwa,inregoa,Bus[3:0]);

	wire[7:0] display;
	outputreg out(Bus,clk,clr,outregwa,display);

	wire[2:0] cucountout;
	counter3b cucounter(cucountout,~clk,clr);
	wire[8:0] instin;
	assign instin[8:5]= instructionreg.store[7:4];
	assign instin[4:2]= cucountout;
	assign instin[1]= cf;
        assign instin[0]= zf;
	controlunit ctrlunit(instin,hlt,marwa,ramwa,ramoa,inregoa,inregwa,awa,aoa,sumout,sub,bwa,outregwa,pcinc,pcoe,pcjmp,flagsin);
	

	// printing stuff ....
	always@(negedge clk)
	begin
		$display("#");
	end

	always @(posedge clk)
	begin
		// print A-register trace data
		if(a.wa) begin
			$display("aReg r %h", a.data_in);
		end
		else if (a.oa) begin
			$display("aReg w %h", a.store);
		end
	end
	always @(posedge clk)
	begin
		// print B-register trace data
		if(b.wa) begin
			$display("bReg r %h", b.data_in);
		end
		else if (b.oa) begin
			$display("bReg w %h", b.store);
		end
	end
	always @(posedge clk)
	begin
		// print output-register trace data
		if(out.wa) begin
			$display("outReg r %h", out.busin);
		end
	end
	always @(posedge clk)
	begin
		// print PC register trace data
		if(pc.inc) begin
			$display("pc r %b", pc.store + 1'b1);
		end
		else if(pc.jmp) begin
			$display("pc r %b", pc.in);
		end
		else if (pc.oe) begin
			$display("pc w %b", pc.store);
		end
	end
	always @(posedge clk)
	begin
		// print memory address register trace data
		if(mar.wa) begin
			$display("mar r %h", mar.busin);
		end
	end
	always @(posedge clk)
	begin
		// print instruction register trace data
		if(instructionreg.wa) begin
			$display("instReg r %h", instructionreg.busin);
		end
		else if (instructionreg.oa) begin
			$display("instReg w %h", instructionreg.store);
		end
	end
	always @(posedge clk)
	begin
		// print RAM trace data
		if(rm.wa) begin
			$display("ram r [%h] %h", rm.addr, rm.bus);
		end
		else if (rm.oa) begin
			$display("ram w [%h] %h", rm.addr, rm.bus);
		end
	end
	always @(posedge clk)
	begin
		// print ALU trace data
		if(alunit.sumout) begin
			$display("alu res:%h sub:%b cf:%b zf:%b", alunit.out, alunit.sub, alunit.carryflg, alunit.zeroflg);
		end
		else if (alunit.flagsin) begin
			$display("alu res:%h sub:%b cf:%b zf:%b", alunit.out, alunit.sub, alunit.carryflg, alunit.zeroflg);
		end
	end

	endmodule

