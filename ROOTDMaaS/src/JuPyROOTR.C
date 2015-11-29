#include<TRInterface.h>

// auto &r=ROOT::R::TRInterface::Instance();

void LoadHandler()
{
// r.Require("evaluate");
// TString code=" require(evaluate)";
    
//     "source('plotcapture2.R')"
// r.Eval(code);
}

void JuPyROOTR(TString codein="plot(sin)")
{
// // ROOT::R::TRInterface::Instance().Require("evaluate");

TString  code="require(evaluate)\n";
code+=".JuPyROOTRstdout = function(msg){write(msg, stdout())}\n";
code+=".JuPyROOTRstdout = function(msg){write(msg, stdout())}\n";
code+=".JuPyROOTRstderr = function(msg){write(msg, stderr())}\n";
code+=".plot_files = c()\n";
code+="assign('.plot_files', c(), envir = .GlobalEnv)\n";
code+=".JuPyROOTRPlotHandler = function(obj)\n";
code+="{\n";
code+="tmpfile=tempfile(tmpdir='.',fileext='.png')\n";
code+="png(tmpfile)\n";
code+="replayPlot(obj)\n";
code+="dev.off()\n";
code+=".plot_files = get('.plot_files', envir=.GlobalEnv)\n";
code+=".plot_files = append(.plot_files,tmpfile)\n";
code+="assign('.plot_files', .plot_files, envir = .GlobalEnv)\n";
code+="}\n";
code+=".JuPyROOTROutPutHandler  = new_output_handler(text=.JuPyROOTRstdout,error=.JuPyROOTRstderr,graphics=.JuPyROOTRPlotHandler)\n";
code+=".JuPyROOTRPrintValues = function(x){\n";
code+="classes = evaluate:::classes(x)\n";
code+="len = length(x)-1\n";
code+="for(i in 1:len){\n";
code+="    if(classes[i]=='character') write(x[[i]],stdout())\n";
code+="}\n";
code+="}\n";
code+=".JuPyROOTREvaluate = function(code){\n";
code+=".a=evaluate('options(device=pdf)',new_device=0, envir = .GlobalEnv)\n";
code+=".b=evaluate(code,output_handler = .JuPyROOTROutPutHandler,envir = .GlobalEnv)\n";
code+=".JuPyROOTRPrintValues(.b)\n";
code+="}\n";


ROOT::R::TRInterface::Instance().Execute(code);

// LoadHandler();
ROOT::R::TRFunctionImport evaluate(".JuPyROOTREvaluate");
evaluate("1");

// evaluate("plot(sin)");

}